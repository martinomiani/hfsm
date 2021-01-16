import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hfsm",
    version="0.0.1",
    author="Debby Nirwan",
    author_email="debby_nirwan@yahoo.com",
    description="Hierarchical Finite State Machine Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debbynirwan/hfsm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="Apache License, Version 2.0",
    platforms="Python 3",
)
