import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Boris MAURICETTE", # Replace with your own username
    version="0.0.1",
    author="Boris MAURICETTE",
    author_email="teddy_boomer@yahoo.fr",
    description="a bunch of classes to generate MPM graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeddyBoomer/grapheMPM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved ::GPL-3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
