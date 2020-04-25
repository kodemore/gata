import os
from typing import Any, Dict

PACKAGE_NAME = "gata"


def build(setup_kwargs: Dict[str, Any]):
    try:
        from Cython.Build import cythonize
        os.environ["CFLAGS"] = "-O3"
        ext_modules = cythonize(
            [f"{PACKAGE_NAME}/*.py"],
            nthreads=int(os.getenv("CYTHON_NTHREADS", 0)),
            language_level=3,
        )
        for ext in ext_modules:
            ext.name = f"{PACKAGE_NAME}." + ext.name

        setup_kwargs.update({
            "ext_modules": ext_modules,
            "zip_safe": False,
        })
    except ImportError:
        pass
