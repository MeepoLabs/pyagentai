"""Sphinx configuration for your_package_name documentation."""

import os
import sys
from datetime import datetime

# Add your_package_name to the path so that autodoc can find it
sys.path.insert(0, os.path.abspath("../.."))

try:
    import your_package_name  # noqa: E402

    version = your_package_name.__version__
except (ImportError, AttributeError):
    version = "0.1.0"  # Fallback version

# Project information
project = "your_package_name"
copyright_str = f"{datetime.now().year}, Your Name"
author = "Your Name"
release = version

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = ["_static"]
html_title = f"your_package_name {version}"

# Intersphinx mapping
intersphinx_mapping: dict[str, tuple[str, str | None]] = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# Autodoc settings
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autoclass_content = "both"
