from setuptools import setup

setup(
    name="pre-commit-hook-mypy",
    version="0.1.0",
    description="A pre-commit hook that runs mypy only on files that are being committed",
    author="Joost Hart",
    author_email="hartjoost@gmail.com",
    url="https://github.com/joosthart/pre-commit-hook-mypy",
    py_modules=["mypy_committed"],
    entry_points={
        "console_scripts": ["mypy-committed=mypy_committed:main"],
    },
    install_requires=["mypy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
) 