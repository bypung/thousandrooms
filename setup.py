import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thousandrooms",
    version="0.1.8",
    author="Ben Pung",
    author_email="ben@houseofpung.net",
    description="A simple roguelike RPG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bypung/thousandrooms",
    packages=setuptools.find_packages(),
    install_requires=[
        'colored',
        'colorama'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'thousandrooms = thousandrooms.__main__:main'
        ]
    },
    include_package_data=True,
)