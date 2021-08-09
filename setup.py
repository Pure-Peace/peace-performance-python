from setuptools import setup
from setuptools_rust import RustExtension


setup(
    name="peace-performance-python",
    version="0.3.1",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 0 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["peace_performance_python"],
    rust_extensions=[
        RustExtension(
            "peace_performance_python._peace_performance",
            debug=False,
        ),
    ],
    include_package_data=True,
    zip_safe=False,
)
