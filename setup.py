from setuptools import setup, find_packages

setup(
    name="pre-commit-hook-mypy",
    version="0.1.1",
    description="A pre-commit hook that runs mypy only on files that are being committed",
    author="Joost 't Hart",
    author_email="hartjoost@gmail.com",
    url="https://github.com/joosthart/pre-commit-hook-mypy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ["mypy-committed=pre_commit_hook_mypy.cli:cli"],
    },
    install_requires=["mypy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
)
