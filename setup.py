from setuptools import setup, find_packages
from pathlib import Path

if __name__ == "__main__":
    with Path(Path(__file__).parent, "README.md").open(encoding="utf-8") as file:
        long_description = file.read()

    setup(
        name = 'firebase-data',
        packages = find_packages(),
        include_package_data = True,
        version = '1.0.0',
        license='MIT',
        description = 'Easily transfer data between firebase projects',
        long_description=long_description,
        long_description_content_type="text/markdown",
        entry_points={"console_scripts": ["fdata = firebase_data:main"]},
        author = 'Louis Beaumont',
        author_email = 'louis.beaumont@gmail.com',
        url = 'https://github.com/louis030195/firebase-data',
        data_files=[(".", ["README.md"])],
        keywords = [
            'firebase',
            'cloud'
        ],
        install_requires=[
            'tqdm',
            'firebase_admin',
            'fire',
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
        ],
    )