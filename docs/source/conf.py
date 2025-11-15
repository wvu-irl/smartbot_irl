# Configuration file for the Sphinx documentation builder.

import os
import sys
from datetime import datetime


# # Add project root to sys.path
# sys.path.insert(0, os.path.abspath("../../smartbot_irl"))


PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

print("=== DEBUG CONF.PY ===")
print("CWD:", os.getcwd())
print("sys.path[0]:", sys.path[0])
print("sys.path:", sys.path)
print("======================")


# ------------------------------------------------------------
# Project information
# ------------------------------------------------------------
project = "SmartBot IRL"
author = "Nathaniel Pearson"
release = "0.1"
copyright = f"{datetime.now().year}, {author}"

# ------------------------------------------------------------
# Path setup
# ------------------------------------------------------------
# Add project root so autodoc can import smartbot_irl

# ------------------------------------------------------------
# Extensions
# ------------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.autosectionlabel",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc.typehints",
]

# ------------------------------------------------------------
# Markdown (MyST)
# ------------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    # "linkify",
    "html_image",
]


autodoc_mock_imports = [
    "matplotlib",
    "numpy",
]


# ------------------------------------------------------------
# Autodoc & Autosummary
# ------------------------------------------------------------
autosummary_generate = True

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "member-order": "bysource",
    "show-inheritance": False,
    "exclude-members": "__weakref__",
}

# Show type hints in description, PyTorch style
autodoc_typehints = "description"

# ------------------------------------------------------------
# Intersphinx links (optional but useful)
# ------------------------------------------------------------


# ------------------------------------------------------------
# Theme (choose ONE)
# ------------------------------------------------------------
html_theme = "furo"
html_title = "SmartBot IRL"

html_theme_options = {
    "top_of_page_buttons": [],
}

# ------------------------------------------------------------
# HTML static files
# ------------------------------------------------------------
templates_path = ["_templates"]
html_static_path = ["_static"]

exclude_patterns = []

# ------------------------------------------------------------
# Sitemap (if publishing)
# ------------------------------------------------------------
html_baseurl = "https://smartbots.wvirl.com"
sitemap_locales = [None]
sitemap_excludes = ["search.html", "genindex.html"]


print("=== IMPORT TEST ===")
try:
    import smartbot_irl

    print("OK: smartbot_irl imported")
except Exception as e:
    print("FAIL:", type(e).__name__, e)
print("===================")
