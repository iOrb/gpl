import os
import subprocess

from setuptools import setup, find_packages
from distutils.command.install import install
from setuptools.command.develop import develop

from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))


def get_description():
    from codecs import open
    # Get the long description from the README file
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


def get_version():
    import sys
    sys.path.insert(0, os.path.join(here, "src", "gpl"))
    import version
    v = version.get_version()
    sys.path = sys.path[1:]
    return v


def main():
    setup(
        name='gpl',
        python_requires='>=3.6.9',
        version=get_version(),
        description='The SLTP Generalized Planning Framework: Sample, Learn, Transform & Plan',
        long_description=get_description(),
        url='https://github.com/iOrb/gpl',
        author='Jordi Moreno',
        author_email='-',

        keywords='generalized planning',
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',

            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],

        packages=find_packages('src'),  # include all packages under src
        package_dir={'': 'src'},  # tell distutils packages are under src

        install_requires=[
            'wheel',
            'gym',
            'matplotlib',
            'imageio',
            'tqdm',

            # 'generalization_grid_games@git+git://github.com/iOrb/generalization_grid_games_2#egg==generalization_grid_games',
            # git clone git://github.com/iOrb/generalization_grid_games_2 && cd generalization_grid_games_2 && pip install -e .

            # 'generalization_grid_games@git+git://github.com/tomsilver/generalization_grid_games#egg==generalization_grid_games',
            # git clone git://github.com/tomsilver/generalization_grid_games && cd generalization_grid_games && pip install -e .
        ],

        extras_require={
            'dev': ['pytest', 'tox'],
        },
    )


if __name__ == '__main__':
    main()
