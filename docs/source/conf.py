# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Smartbot IRL"
copyright = "2025, Nathaniel Pearson"
author = "Nathaniel Pearson"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # for Google/Numpy docstrings
    "sphinx.ext.viewcode",
    "myst_parser",  # to support Markdown
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.autosectionlabel",
    "sphinxcontrib.katex",
    "sphinx_copybutton",
    "sphinx_design",
    # "myst_nb",
    # "sphinx.ext.linkcode",
    "sphinxcontrib.mermaid",
    "sphinx_sitemap",
]


myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]

autosummary_generate = True
autodoc_default_options = {"members": True, "undoc-members": False, "show-inheritance": False}
html_theme = "pydata_sphinx_theme"
html_title = "SmartBot IRL"

html_theme = "furo"
html_theme_options = {
    "logo": {"text": "SmartBot IRL"},
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "show_prev_next": False,
}

html_baseurl = "https://smartbots.wvirl.com"  # needed for sphinx-sitemap
sitemap_locales = [None]
sitemap_excludes = [
    "search.html",
    "genindex.html",
]
sitemap_url_scheme = "{link}"

# html_additional_pages = {
#     "404": "404.html",
# }

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
