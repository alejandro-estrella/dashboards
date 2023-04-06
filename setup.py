import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'optimize': 1,  # 0=none, 1=bytecode, 2=docstrings
    'packages': ["click", "colorama", "contourpy", "cycler", "dash", "dash_core_components", "dash_html_components", "dash_renderer", "dash_table", "dash_extensions", "dash_bootstrap_components", "flask", "flask_sqlalchemy", "fontTools", "future", "greenlet", "itsdangerous", "jinja2", "kiwisolver", "markupsafe", "matplotlib", "MsSql", "numpy", "packaging", "pandas", "pefile", "PIL", "plotly", "pymssql", "pyodbc", "pyparsing", "pytz", "seaborn", "scipy", "six", "sqlalchemy", "tenacity", "typing_extensions", "werkzeug", "nbformat", "traitlets", "attrs", "fastjsonschema", "jsonschema", "nbformat", "platformdirs", "pyrsistent"],
    'includes': ["jsonschema","attrs","platformdirs","pyrsistent", "platformdirs", "traitlets", "scipy"],
    'include_files': ['assets/','pages/'],
    'zip_includes': [],
    'zip_include_packages': [],
    'excludes': ["altair", "altgraph", "asttokens", "backcall", "blinker", "cachetools","charset-normalizer", "comm", "cx-Freeze", "cx-Logging", "debugpy", "decorator", "entrypoints", "executing", "fitter", "gitdb", "gitpython", "importlib-metadata", "ipykernel", "ipython", "jedi", "joblib", "jupyter-client", "jupyter-core", "lief", "markdown-it-py", "matplotlib-inline", "mdurl", "nest-asyncio", "parso", "pickleshare", "pip", "pipdeptree", "prompt-toolkit", "protobuf", "psutil", "pure-eval", "pyarrow", "pydeck", "pygments", "pygments", "pyinstaller-hooks-contrib", "pympler", "pytz-deprecation-shim", "pyzmq", "rich", "semver", "setuptools", "smmap", "stack-data", "streamlit", "toml", "toolz", "tornado", "tqdm", "tzdata", "tzlocal", "validators", "watchdog", "wcwidth", "zipp"]
}

setup(
    name="tickets_test",
    version="0.1",
    description="Proof of concept for Dash distributable apps.",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py")],
)
