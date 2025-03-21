from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agenticSeek",
    version="0.1.0",
    author="Fosowl",
    author_email="mlg.fcu@gmail.com",
    description="A Python project for agentic search and processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fosowl/agenticSeek",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "openai",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "playsound>=1.3.0",
        "soundfile>=0.13.1",
        "transformers>=4.46.3",
        "torch>=2.4.1",
        "ollama>=0.4.7",
        "scipy>=1.15.1",
        "kokoro>=0.7.12",
        "flask>=3.1.0",
        "protobuf>=3.20.3",
        "termcolor>=2.5.0",
        "gliclass>=0.1.8",
        "ipython>=8.34.0",
        "librosa>=0.10.2.post1",
        "selenium>=4.29.0",
        "markdownify>=1.1.0",
        "text2emotion>=0.0.5",
        "python-dotenv>=1.0.0",
        "langid>=1.1.6",
        "httpx>=0.27,<0.29",
        "anyio>=3.5.0,<5",
        "distro>=1.7.0,<2",
        "jiter>=0.4.0,<1",
        "sniffio",
        "tqdm>4"
    ],
    extras_require={
        "chinese": [
            "ordered_set",
            "pypinyin",
            "cn2an",
            "jieba",
        ],
    },
    entry_points={
        "console_scripts": [
            "agenticseek=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
