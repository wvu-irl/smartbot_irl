import os
import sys
from datetime import datetime

# print('=== DEBUG: smartbot_irl import ===')
# try:
#     import smartbot_irl

#     print('smartbot_irl imported:', smartbot_irl)
#     print('type(smartbot_irl):', type(smartbot_irl))
#     if hasattr(smartbot_irl, '__version__'):
#         print('smartbot_irl.__version__ =', smartbot_irl.__version__)
#         print('type =', type(smartbot_irl.__version__))
# except Exception as e:
#     print('Import failed:', e)
# print('==================================')

# print('=== TEMPLATE PATHS ===')
# print(os.listdir(os.path.join(os.path.dirname(__file__), '_templates')))
# print('======================')

# PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
# sys.path.insert(0, PROJECT_ROOT)

# print('=== DEBUG CONF.PY ===')
# print('CWD:', os.getcwd())
# print('sys.path[0]:', sys.path[0])
# print('sys.path:', sys.path)
# print('======================')
import smartbot_irl

# ------------------------------------------------------------
# Project information
# ------------------------------------------------------------
project = 'smartbot-irl'
author = 'Nathaniel Pearson'
release = '0.1'
copyright = f'{datetime.now().year}, {author}'


# ------------------------------------------------------------
# Extensions
# ------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc.typehints',
    'numpydoc',
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
# LaTeX (PDF) Output Configuration
# ------------------------------------------------------------
latex_engine = 'pdflatex'  # or 'xelatex' or 'lualatex' for better unicode/font support

latex_elements = {
    'latexmkopts': '-interaction=nonstopmode -f',
    'papersize': 'letterpaper',  # or 'a4paper'
    'pointsize': '11pt',
    'preamble': r"""
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{enumitem}
\setlistdepth{10}
\renewlist{itemize}{itemize}{10}
\renewlist{enumerate}{enumerate}{10}
""",
    'figure_align': 'H',
}


# ------------------------------------------------------------
# Autodoc
# ------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autoclass_content = 'class'
autodoc_member_order = 'groupwise'

autodoc_default_options = {
    # 'members': True, # Generate autodoc for all all members of target
    # 'member-order': 'groupwise',
    # 'private-members': False,
    # 'special-members': False,
    # 'no-value': True,
    # 'show-inheritance': False,
    # 'recursive': True,
    # 'special-members': '',  # dunders
    # 'class-doc-from': 'class',  # critical
    # 'inherited-members': False,  # < Fix pandas autodoc problem?
}
autodoc_inherit_docstrings = True

# Show type hints in description, PyTorch style
autodoc_typehints = 'description'
# autodoc_class_signature = 'none'
# autodoc_typehints = 'none'
autodoc_typehints_format = 'short'
autodoc_class_signature = 'mixed'

# ------------------------------------------------------------
# Autosummary
# ------------------------------------------------------------
# Create stub files automatically.
autosummary_generate = True

# Only look at what is in modules __all__.
autosummary_ignore_module_all = False

# Also summary modules that are imported
autosummary_imported_members = False


# ------------------------------------------------------------
# Config napoleon
# ------------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_param = False

# Numpydoc
numpydoc_show_class_members = False
numpydoc_attributes_as_param_list = True
numpydoc_show_inherited_class_members = False


# ------------------------------------------------------------
# Sphinx Design
# ------------------------------------------------------------
# sd_custom_directives = {
#     'dropdown-syntax': {
#         'inherit': 'dropdown',
#         'argument': 'Syntax',
#         'options': {
#             'color': 'primary',
#             'icon': 'code',
#         },
#     }
# }

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
# ------------------------------------------------------------
# Sitemap (if publishing)
# ------------------------------------------------------------
html_baseurl = 'https://mobilerobotics.wvirl.com'
sitemap_locales = [None]
sitemap_excludes = ['search.html', 'genindex.html']


# print('=== IMPORT TEST ===')
# try:
#     import smartbot_irl

#     print('OK: smartbot_irl imported')
# except Exception as e:
#     print('FAIL:', type(e).__name__, e)
# print('===================')
