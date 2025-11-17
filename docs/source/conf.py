import os
import sys
from datetime import datetime

print('=== TEMPLATE PATHS ===')
print(os.listdir(os.path.join(os.path.dirname(__file__), '_templates')))
print('======================')

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

print('=== DEBUG CONF.PY ===')
print('CWD:', os.getcwd())
print('sys.path[0]:', sys.path[0])
print('sys.path:', sys.path)
print('======================')


# ------------------------------------------------------------
# Project information
# ------------------------------------------------------------
project = 'SmartBot IRL'
author = 'Nathaniel Pearson'
release = '0.1'
copyright = f'{datetime.now().year}, {author}'

# ------------------------------------------------------------
# Path setup
# ------------------------------------------------------------
# Add project root so autodoc can import smartbot_irl

# ------------------------------------------------------------
# Extensions
# ------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc.typehints',
]

# ------------------------------------------------------------
# Markdown (MyST)
# ------------------------------------------------------------
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    # "linkify",
    'html_image',
]


autodoc_mock_imports = [
    'matplotlib',
    'numpy',
    'pandas',
]

# ------------------------------------------------------------
# Autodoc & Autosummary
# ------------------------------------------------------------
autosummary_generate = True
# autosummary_ignore_module_all = False
autosummary_ignore_module_all = False
autosummary_imported_members = False

autodoc_default_options = {
    # 'members': True,
    'no-undoc-members': True,
    'member-order': 'groupwise',
    # 'show-inheritance': False,
    # 'recursive': True,
    # 'special-members': '',  # don't expand magic methods
    # 'inherited-members': False,  # < Fix pandas autodoc problem?
    # 'exclude-members': '__weakref__',
}
autodoc_inherit_docstrings = False

# Show type hints in description, PyTorch style
autodoc_typehints = 'description'

# ------------------------------------------------------------
# Intersphinx links (optional but useful)
# ------------------------------------------------------------


# ------------------------------------------------------------
# Theme
# ------------------------------------------------------------
# html_theme = "furo"
html_theme = 'pydata_sphinx_theme'
html_title = 'SmartBot IRL'

html_logo = '_static/logos/irl_logo_big.png'  # fallback for both modes

html_theme_options = {
    # 'navbar_align': 'content',
    'show_toc_level': 2,  # Show 2 levels of headings in the sidebar
    'navigation_depth': 2,
    'collapse_navigation': False,
    'sidebar': {
        'navigation_with_keys': True,
    },
    'logo': {
        'image_light': '_static/logos/irl_logo_big.png',
        'image_dark': '_static/logos/irl_logo_big.png',
        'text': 'SmartBot IRL',  # optional if you want to show title
        'alt_text': 'SmartBot IRL - Home',
        'link': 'index',  # optional; default goes to root_doc
    },
}
# ------------------------------------------------------------
# HTML static files
# ------------------------------------------------------------
templates_path = ['_templates']
html_static_path = ['_static']
html_css_files = ['css/custom.css']

html_additional_pages = {
    'index': 'index.html',
}

exclude_patterns = []
autosummary_imported_members = True
# ------------------------------------------------------------
# Sitemap (if publishing)
# ------------------------------------------------------------
html_baseurl = 'https://smartbots.wvirl.com'
sitemap_locales = [None]
sitemap_excludes = ['search.html', 'genindex.html']


print('=== IMPORT TEST ===')
try:
    import smartbot_irl

    print('OK: smartbot_irl imported')
except Exception as e:
    print('FAIL:', type(e).__name__, e)
print('===================')
