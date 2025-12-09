from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wigo",
    version="0.1.0",
    author="Ajay Patil",
    author_email="ajay.patil.a01@gmail.com",
    description="A web automation framework built on Playwright with middleware support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Neolatika/wigo.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "playwright>=1.56.0",
        "playwright-stealth>=2.0.0",
        "pyee>=13.0.0",
        "typing-extensions>=4.15.0"
    ],
    entry_points={
        'console_scripts': [
            'wigo=wigo.cli:main',
        ],
    },
)
