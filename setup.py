from setuptools import find_packages, setup 
import os

with open(os.path.join(os.path.dirname(__file__),'README.md'), "r", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name="asosoft",
    version="0.1.0",
    description="AsoSoft's Library for Kurdish language processing tasks",
    keywords='natural-language-processing, normalization, unicode-normalization, central-kurdish, kurdish, sorani',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={'': ['resources/*.csv']},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AsoSoft/AsoSoft-Library-py",
    author="Aso Mahmudi",
    author_email="aso.mehmudi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["regex >= 2023.0.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.11"
)