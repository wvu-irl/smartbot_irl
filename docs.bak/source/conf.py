extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

myst_enable_extensions = [
    "colon_fence",       # ::: fenced content
    "deflist",           # definition lists
    "linkify",           # auto-detect links
    "substitution",      # variable substitution
]

html_theme = "furo"  # or sphinx_rtd_theme, pydata_sphinx_theme
