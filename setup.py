from setuptools import setup, find_packages

setup(
    name="friendly-fox",
    version="0.1.0",
    description="Argentine ant model for cooperative agent fleets",
    long_description=open("THEORY.md").read(),
    long_description_content_type="text/markdown",
    author="Cocapn Fleet",
    url="https://github.com/SuperInstance/friendly-fox",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    extras_require={
        "test": ["pytest"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: AI :: Agents",
        "License :: OSI Approved :: MIT License",
    ],
)
