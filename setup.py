from setuptools import setup

try:
    from setuptools_rust import RustExtension
except ImportError:
    from textwrap import dedent

    raise ImportError(
        dedent(
            '''
            `setuptools-rust` is a required dependency to run `setup.py`.
            This should not happen if you're using `pip>=10` as it honors `pyproject.toml`.
            This usually (at least on our workflows) might happen while
            building source-distribution.
            '''
        )
    )


setup(
    name="peace-performance-python",
    version="2.0.0",
    description="Rust binding for python. To calculate star ratings and performance points for all osu! gamemodes, and quickly parse Beatmap into python objects.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="rust peace osu pp beatmap parse rosu-pp peace-performance",
    author="Pure-Peace",
    author_email="abner666666@foxmail.com",
    maintainer="Pure-Peace",
    maintainer_email="abner666666@foxmail.com",
    python_requires=">=3.7",
    url="https://github.com/Pure-Peace/peace-performance-python",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        "typing_extensions"
    ],
    packages=["peace_performance_python", "peace_performance_python.objects",
              "peace_performance_python.functions"],
    package_data={"peace_performance_python": ["*.pyi", "**/*.pyi"]},
    rust_extensions=[
        RustExtension(
            "peace_performance_python._peace_performance",
            debug=False,
        ),
    ],
    include_package_data=True,
    zip_safe=False,
)
