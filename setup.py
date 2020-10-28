import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='puissance4',
    version='0.6.1',
    author='Wok',
    author_email='wok@tuta.io',
    description='Artificial Intelligence for the game Connect Four on PyPI',
    keywords=['puissance4', 'puissance-4', 'connect4', 'connect-4', 'connect-four', 'artificial intelligence', 'UCT'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/woctezuma/puissance4',
    download_url='https://github.com/woctezuma/puissance4/archive/0.6.1.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Games/Entertainment',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: French',
    ],
    python_requires='>=3',
)
