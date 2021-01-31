import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrape",
    version="0.0.1",
    author="Griffin Walker",
    author_email="griffin.walker@mac.com",
    description="CLI for pulling nba stats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "scrape = scrape.core:main",
        ],
    },
    python_requires=">=3.8",
)
