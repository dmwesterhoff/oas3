"""
flask_oas3.commands
~~~~~~~~~~~~~~~~~~~

Extension CLI that is bound to the `flask` base command.
"""

import click
from flask.cli import with_appcontext
from flask.cli import AppGroup
from flask import current_app

cli = AppGroup('oas3', help='Tools for working with OAS3 spec attached to your app.')


def extension_or_raise():
    """Get the OAS3 extension from Flask app for commands that require it."""
    oas3 = current_app.extensions.get('oas3')
    if oas3 is None:
        raise click.UsageError('OAS3 extension is unbound and required to run this command. \
                                Use extension init or init_app methods and then retry.')
    return oas3


@cli.command()
@with_appcontext
def json():
    """Return the spec as JSON to stdout."""
    oas3 = extension_or_raise()
    click.echo(oas3.json())


@cli.command()
@with_appcontext
def yaml():
    """Return the spec as YAML to stdout."""
    oas3 = extension_or_raise()
    click.echo(oas3.yaml())
