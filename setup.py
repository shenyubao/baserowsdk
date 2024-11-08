from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="baserowsdk",
    version="0.0.1",
    author="shenyubao",
    author_email="ssybb1988@gmail.com",
    description="Baserow Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["requests>=2.31.0"],
)