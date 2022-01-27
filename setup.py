from pathlib    import Path
import setuptools
import sys

min_version = (3, 8)

if sys.version_info < min_version:
    error = """
Beginning with pyrodsCLI 0.1.0, Python {0} or above is required.
This may be due to an out of date pip.
Make sure you have pip >= 9.0.1.
""".format('.'.join(str(n) for n in min_version)),
    sys.exit(error)

base_dir = Path(__file__).parent.resolve()
version_file = base_dir / "pyrodsCLI/__version__.py"
readme_file = base_dir / "README.md"

# Eval the version file to get __version__; avoids importing our own package
with version_file.open() as f:
    exec(f.read())

# Get the long description from the README file
with readme_file.open(encoding = "utf-8") as f:
    long_description = f.read()



setuptools.setup(
    name = "LMIB-pyrodsCLI",
    version = __version__,
    author = "LMIB",
    author_email = "david.wouters@kuleuven.be",
    description = "Collection of python powered iRODS commands.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = "database",
    url = "https://github.com/nextstrain/augur",
    project_urls = {
        "Bug Reports": "https://github.com/sifrimlab/pyrodsCLI/issues",
        "Source": "https://github.com/sifrimlab/pyrodsCLI",
    },
    packages = setuptools.find_packages(),
    python_requires = '>={}'.format('.'.join(str(n) for n in min_version)),
    install_requires = [
        "numpy",
        "python_irodsclient",
        "tqdm",
        "glob2"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU Affero General Public License v3",

        # Python 3 only
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # Install a "pyrodsCLI" program which calls pyrodsCLI.__main__.main()
    #   https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
    entry_points = {
        "console_scripts": [
            "pyrodsCLI = pyrodsCLI.__main__:main",
        ]
    }
)
