from setuptools import setup, find_packages

setup(
    name="writewise",
    version="1.0.0",
    description="Advanced grammar checker for students, teachers, and writers",
    author="WriteWise Team",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.7.0",
        "language-tool-python>=2.7.0",
        "textstat>=0.7.3",
        "nltk>=3.8.1",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.4.0",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "requests>=2.31.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "httpx>=0.25.0",
        ]
    },
    python_requires=">=3.8",
)
