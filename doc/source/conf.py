# -*- coding: utf-8 -*-
#

import sys
import os

sys.path.insert(0, os.path.abspath('../../'))
sys.path.append(os.path.abspath('_themes'))
import oas3

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'OAS3'
copyright = u'2018, Pinn Technologies, Inc'

version = release = oas3.__version__
exclude_patterns = []
pygments_style = 'sphinx'
html_theme_options = {
    "index_logo": "logo.png"
}
html_theme_path = ["_themes"]
html_theme = 'flask'
html_static_path = ['_static']
#html_style = 'limiter.css'

htmlhelp_basename = 'oas3doc'
#html_logo = 'small-logo.png'
#html_favicon = 'tap-icon.png'
html_sidebars = {
    'index': ['sidebarintro.html', 'localtoc.html', 'sourcelink.html', 'searchbox.html'],
    '**': ['localtoc.html', 'relations.html',
           'sourcelink.html', 'searchbox.html']
}

latex_documents = [
    ('index', 'OAS3.tex', u'OAS3 Documentation',
     u'Pinn Technologies, Inc.', 'manual'),
]
man_pages = [
    ('index', 'OAS3.text', u'OAS3 Documentation',
     [u'Pinn Technologies, Inc.'], 1)
]

texinfo_documents = [
    ('index', 'OAS3', u'OAS3 Documentation',
     u'Pinn Technologies, Inc.', 'OAS3', 'OAS3 Python Library.',
     'Miscellaneous'),
]

intersphinx_mapping = {'python': ('http://docs.python.org/', None)
}

autodoc_default_flags = [
    "members"
    , "show-inheritance"
]
