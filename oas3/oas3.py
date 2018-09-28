"""
the flask extension
"""
import datetime
import itertools
import logging
import sys
import time
import warnings
import json
import yaml
from functools import wraps

import six
from flask import request, current_app, g, Blueprint
from limits.errors import ConfigurationError
from . import objects


class OAS3(object):
    """
    :param app: :class:`flask.Flask` instance to initialize the extension
     with.
    :param bool headers_enabled: whether ``X-RateLimit`` response headers are written.
    :param str strategy: the strategy to use. refer to :ref:`ratelimit-strategy`
     chain of the application. default ``True``
    :param bool swallow_errors: whether to swallow errors when hitting a rate limit.
     An exception will still be logged. default ``False``
    """

    def __init__(self, app=None, openapi='3.0.1', info=None):
        self.app = app
        self.logger = logging.getLogger("flask-oas3")
        self.openapi = openapi
        self._info = info
        self._exempt_routes = set()
        self._route_limits = {}
        self._blueprint_exempt = set()
        self.__check_backend_count = 0
        self.__last_check_backend = time.time()
        self.__marked_for_limiting = {}

        # class BlackHoleHandler(logging.StreamHandler):
        #     def emit(*_):
        #        return

        # self.logger.addHandler(BlackHoleHandler())
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        :param app: :class:`flask.Flask` instance to rate limit.
        """
        #if app.config.get(C.GLOBAL_LIMITS, None):
        #    self.raise_global_limits_warning()
        #conf_limits = app.config.get(
        #    C.GLOBAL_LIMITS, app.config.get(C.DEFAULT_LIMITS, None)
        #)

        # purely for backward compatibility as stated in flask documentation
        if not hasattr(app, 'extensions'):
            app.extensions = {}  # pragma: no cover

        if not app.extensions.get('oas3'):
            pass
            # if self._auto_check:
            #    app.before_request(self.__check_request_limit)
            # app.after_request(self.__inject_headers)

        app.extensions['oas3'] = self

    @property
    def spec(self):
        """Loads the specification and returns a dictionary if loading succeeded."""
        return objects.Spec(openapi=self.openapi,
                            info=self.info)

    def data(self):
        """Returns the spec as a python dictionary."""
        data, errors = objects.Spec.Meta().dump(self.spec)
        if errors:
            raise ValueError(errors)
        errors = objects.Spec.Meta().validate(data)
        if errors:
            raise ValueError(errors)
        return data

    def json(self, pretty=True):
        """Return the specification as a JSON string."""
        if pretty:
            return json.dumps(self.data(),
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        return json.dumps(self.data)

    def yaml(self):
        """Return the specification as a YAML string."""
        return yaml.dump(self.data(), default_flow_style=False)

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, cls):
        self._info = objects.Info.load_from_class(cls)

    def _info(self, info):
        """
        decorator to be used for rate limiting individual routes or blueprints.
        :param limit_value: rate limit string or a callable that returns a string.
         :ref:`ratelimit-string` for more details.
        :param function key_func: function/lambda to extract the unique identifier for
         the rate limit. defaults to remote address of the request.
        :param bool per_method: whether the limit is sub categorized into the http
         method of the request.
        :param list methods: if specified, only the methods in this list will be rate
         limited (default: None).
        :param error_message: string (or callable that returns one) to override the
         error message used in the response.
        :param exempt_when:
        :return:
        """
        self.info = info

    def __info_decorator(
            self,
            f=None
    ):
        def _inner(obj):
            print(self)

            @wraps(obj)
            def __inner(*a, **k):
                print("really deep")
                return obj(*a, **k)
            return __inner
        return _inner

    def check(self):
        """
        check the limits for the current request

        :raises: RateLimitExceeded
        """
        self.__check_request_limit(False)

    def reset(self):
        """
        resets the storage if it supports being reset
        """
        try:
            self._storage.reset()
            self.logger.info("Storage has been reset and all limits cleared")
        except NotImplementedError:
            self.logger.warning(
                "This storage type does not support being reset"
            )

    @property
    def limiter(self):
        if self._storage_dead and self._in_memory_fallback:
            return self._fallback_limiter
        else:
            return self._limiter

    def __inject_headers(self, response):
        current_limit = getattr(g, 'view_rate_limit', None)
        if self.enabled and self._headers_enabled and current_limit:
            window_stats = self.limiter.get_window_stats(*current_limit)
            reset_in = 1 + window_stats[0]
            response.headers.add(
                self._header_mapping[HEADERS.LIMIT],
                str(current_limit[0].amount)
            )
            response.headers.add(
                self._header_mapping[HEADERS.REMAINING], window_stats[1]
            )
            response.headers.add(self._header_mapping[HEADERS.RESET], reset_in)

            # response may have an existing retry after
            existing_retry_after_header = response.headers.get('Retry-After')

            if existing_retry_after_header is not None:
                # might be in http-date format
                retry_after = parse_date(existing_retry_after_header)

                # parse_date failure returns None
                if retry_after is None:
                    retry_after = time.time() + int(existing_retry_after_header)

                if isinstance(retry_after, datetime.datetime):
                    retry_after = time.mktime(retry_after.timetuple())

                reset_in = max(retry_after, reset_in)

            # set the header instead of using add
            response.headers.set(
                self._header_mapping[HEADERS.RETRY_AFTER],
                self._retry_after == 'http-date' and http_date(reset_in)
                or int(reset_in - time.time())
            )
        return response

    def __evaluate_limits(self, endpoint, limits):
        failed_limit = None
        limit_for_header = None
        for lim in limits:
            limit_scope = lim.scope or endpoint
            if lim.is_exempt:
                return
            if lim.methods is not None and request.method.lower(
            ) not in lim.methods:
                return
            if lim.per_method:
                limit_scope += ":%s" % request.method
            limit_key = lim.key_func()

            args = [limit_key, limit_scope]
            if all(args):
                if self._key_prefix:
                    args = [self._key_prefix] + args
                if not limit_for_header or lim.limit < limit_for_header[0]:
                    limit_for_header = [lim.limit] + args
                if not self.limiter.hit(lim.limit, *args):
                    self.logger.warning(
                        "ratelimit %s (%s) exceeded at endpoint: %s",
                        lim.limit, limit_key, limit_scope
                    )
                    failed_limit = lim
                    limit_for_header = [lim.limit] + args
                    break
            else:
                self.logger.error(
                    "Skipping limit: %s. Empty value found in parameters.",
                    lim.limit
                )
                continue
        g.view_rate_limit = limit_for_header

        if failed_limit:
            if failed_limit.error_message:
                exc_description = failed_limit.error_message if not callable(
                    failed_limit.error_message
                ) else failed_limit.error_message()
            else:
                exc_description = six.text_type(failed_limit.limit)
            raise RateLimitExceeded(exc_description)

    def __check_request_limit(self, in_middleware=True):
        endpoint = request.endpoint or ""
        view_func = current_app.view_functions.get(endpoint, None)
        name = (
            "%s.%s" % (view_func.__module__, view_func.__name__)
            if view_func else ""
        )
        if (not request.endpoint
            or not self.enabled
            or view_func == current_app.send_static_file
            or name in self._exempt_routes
            or request.blueprint in self._blueprint_exempt
            or any(fn() for fn in self._request_filters)
            or g.get("_rate_limiting_complete")
        ):
            return
        limits, dynamic_limits = [], []

        # this is to ensure backward compatibility with behavior that
        # existed accidentally, i.e::
        #
        # @limiter.limit(...)
        # @app.route('...')
        # def func(...):
        #
        # The above setup would work in pre 1.0 versions because the decorator
        # was not acting immediately and instead simply registering the rate
        # limiting. The correct way to use the decorator is to wrap
        # the limiter with the route, i.e::
        #
        # @app.route(...)
        # @limiter.limit(...)
        # def func(...):

        implicit_decorator = view_func in self.__marked_for_limiting.get(
            name, []
        )

        if not in_middleware or implicit_decorator:
            limits = (
                name in self._route_limits and self._route_limits[name] or []
            )
            dynamic_limits = []
            if name in self._dynamic_route_limits:
                for lim in self._dynamic_route_limits[name]:
                    try:
                        dynamic_limits.extend(list(lim))
                    except ValueError as e:
                        self.logger.error(
                            "failed to load ratelimit for view function %s (%s)",
                            name, e
                        )
        if request.blueprint:
            if (request.blueprint in self._blueprint_dynamic_limits
                and not dynamic_limits
            ):
                for limit_group in self._blueprint_dynamic_limits[
                    request.blueprint
                ]:
                    try:
                        dynamic_limits.extend(
                            [
                                Limit(
                                    limit.limit, limit.key_func, limit.scope,
                                    limit.per_method, limit.methods,
                                    limit.error_message, limit.exempt_when
                                ) for limit in limit_group
                            ]
                        )
                    except ValueError as e:
                        self.logger.error(
                            "failed to load ratelimit for blueprint %s (%s)",
                            request.blueprint, e
                        )
            if request.blueprint in self._blueprint_limits and not limits:
                limits.extend(self._blueprint_limits[request.blueprint])

        try:
            all_limits = []
            if self._storage_dead and self._fallback_limiter:
                if in_middleware and name in self.__marked_for_limiting:
                    pass
                else:
                    if self.__should_check_backend() and self._storage.check():
                        self.logger.info("Rate limit storage recovered")
                        self._storage_dead = False
                        self.__check_backend_count = 0
                    else:
                        all_limits = list(
                            itertools.chain(*self._in_memory_fallback)
                        )
            if not all_limits:
                route_limits = limits + dynamic_limits
                all_limits = list(itertools.chain(*self._application_limits)) if in_middleware else []
                all_limits += route_limits
                if (
                    not route_limits
                    and not (in_middleware and name in self.__marked_for_limiting)
                    or implicit_decorator
                ):
                        all_limits += list(itertools.chain(*self._default_limits))
            self.__evaluate_limits(endpoint, all_limits)
        except Exception as e:  # no qa
            if isinstance(e, RateLimitExceeded):
                six.reraise(*sys.exc_info())
            if self._in_memory_fallback and not self._storage_dead:
                self.logger.warn(
                    "Rate limit storage unreachable - falling back to"
                    " in-memory storage"
                )
                self._storage_dead = True
                self.__check_request_limit(in_middleware)
            else:
                if self._swallow_errors:
                    self.logger.exception(
                        "Failed to rate limit. Swallowing error"
                    )
                else:
                    six.reraise(*sys.exc_info())

    def __limit_decorator(
        self,
        limit_value,
        key_func=None,
        shared=False,
        scope=None,
        per_method=False,
        methods=None,
        error_message=None,
        exempt_when=None,
    ):
        _scope = scope if shared else None

        def _inner(obj):
            func = key_func or self._key_func
            is_route = not isinstance(obj, Blueprint)
            name = "%s.%s" % (
                obj.__module__, obj.__name__
            ) if is_route else obj.name
            dynamic_limit, static_limits = None, []
            if callable(limit_value):
                dynamic_limit = LimitGroup(
                    limit_value, func, _scope, per_method, methods,
                    error_message, exempt_when
                )
            else:
                try:
                    static_limits = list(
                        LimitGroup(
                            limit_value, func, _scope, per_method, methods,
                            error_message, exempt_when
                        )
                    )
                except ValueError as e:
                    self.logger.error(
                        "failed to configure %s %s (%s)", "view function"
                        if is_route else "blueprint", name, e
                    )
            if isinstance(obj, Blueprint):
                if dynamic_limit:
                    self._blueprint_dynamic_limits.setdefault(
                        name, []
                    ).append(dynamic_limit)
                else:
                    self._blueprint_limits.setdefault(
                        name, []
                    ).extend(static_limits)
            else:
                self.__marked_for_limiting.setdefault(name, []).append(obj)
                if dynamic_limit:
                    self._dynamic_route_limits.setdefault(
                        name, []
                    ).append(dynamic_limit)
                else:
                    self._route_limits.setdefault(
                        name, []
                    ).extend(static_limits)

                @wraps(obj)
                def __inner(*a, **k):
                    if self._auto_check and not g.get("_rate_limiting_complete"):
                        self.__check_request_limit(False)
                        g._rate_limiting_complete = True
                    return obj(*a, **k)
                return __inner
        return _inner

    def limit(
        self,
        limit_value,
        key_func=None,
        per_method=False,
        methods=None,
        error_message=None,
        exempt_when=None,
    ):
        """
        decorator to be used for rate limiting individual routes or blueprints.

        :param limit_value: rate limit string or a callable that returns a string.
         :ref:`ratelimit-string` for more details.
        :param function key_func: function/lambda to extract the unique identifier for
         the rate limit. defaults to remote address of the request.
        :param bool per_method: whether the limit is sub categorized into the http
         method of the request.
        :param list methods: if specified, only the methods in this list will be rate
         limited (default: None).
        :param error_message: string (or callable that returns one) to override the
         error message used in the response.
        :param exempt_when:
        :return:
        """
        return self.__limit_decorator(
            limit_value,
            key_func,
            per_method=per_method,
            methods=methods,
            error_message=error_message,
            exempt_when=exempt_when,
        )
