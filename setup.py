from setuptools import setup, find_packages
from pathlib import Path

README = Path("README.md").read_text()

setup(
    name="cbt",
    version="0.0.2",
    author="s045pd",
    keyword="english,cli,python",
    author_email="s045pd.x@gmail.com",
    description="Auto suggestion english translations cli",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/s045pd/t",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click==7.1.2",
        "requests==2.24.0",
        "requests_html==0.10.0",
        "termcolor==1.1.0",
        "prompt-toolkit==3.0.24",
        "playsound==1.3.0",
        "PyObjC==8.1",
    ],
    entry_points="""
        [console_scripts]
        t=t.__main__:main
    """,
)
