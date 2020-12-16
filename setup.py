import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='releaser',
    version='0.0.1',
    description='releaser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jlnwlf/releaser',
    author='Julien Wolflisberg',
    author_email='julien.wolflisberg@gmail.com',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',

        'Environment :: Console',
    ],

    keywords='release-management',

    packages=find_packages(),

    install_requires=[
        'configargparse',
        'dateparser',
        'gitdb',
        'gitpython',
        'humanize',
        'jinja2',
        'markdown',
        'markupsafe',
        'maya',
        'pendulum',
        'python-dateutil',
        'pytz',
        'pytzdata',
        'regex',
        'semver',
        'six',
        'smmap',
        'snaptime',
        'tzlocal',
    ],

    package_data={'releaser': ['templates/*.j2']},

    python_requires='>=3.3, <4',
    entry_points={
        'console_scripts': [
            'releaser=releaser.__main__:main',
        ],
    },
)
