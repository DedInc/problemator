from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="problemator",
    version="1.1.0",
    author="Maehdakvan",
    author_email="visitanimation@google.com",
    description="WolframAlpha's Unlimited AI-generated practice problems and answers API wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DedInc/problemator",
    project_urls={
        "Bug Tracker": "https://github.com/DedInc/problemator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['requests', 'user_agent'],
    python_requires='>=3.0'
)
