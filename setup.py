from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools

setup(
    name='puissance4',
    packages=['puissance4'],
    install_requires=[
    ],
    version='0.1',
    description='Artificial Intelligence for the game Connect Four on PyPI',
    long_description='Artificial Intelligence for Puissance-4/Connect-4, based on "Upper Confidence bounds for Trees".',
    long_description_content_type='text/x-rst',
    author='Wok',
    author_email='wok@tuta.io',
    url='https://github.com/woctezuma/puissance4',
    download_url='https://github.com/woctezuma/puissance4/archive/0.1.tar.gz',
    keywords=['puissance4', 'puissance-4', 'connect4', 'connect-4', 'connect-four', 'artificial intelligence', 'UCT'],
    classifiers=[
        'Topic :: Games/Entertainment',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: French',
    ],
)
