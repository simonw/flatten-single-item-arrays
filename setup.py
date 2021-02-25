from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="flatten-single-item-arrays",
    description="Given a JSON list of objects, flatten any keys which always contain single item arrays to just a single value",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/flatten-single-item-arrays",
    project_urls={
        "Issues": "https://github.com/simonw/flatten-single-item-arrays/issues",
        "CI": "https://github.com/simonw/flatten-single-item-arrays/actions",
        "Changelog": "https://github.com/simonw/flatten-single-item-arrays/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["flatten_single_item_arrays"],
    entry_points="""
        [console_scripts]
        flatten-single-item-arrays=flatten_single_item_arrays.cli:cli
    """,
    install_requires=["click"],
    extras_require={"test": ["pytest"]},
    tests_require=["flatten-single-item-arrays[test]"],
    python_requires=">=3.6",
)
