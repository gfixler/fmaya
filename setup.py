from distutils.core import setup

setup(
    name = 'fmaya',
    packages = ['fmaya'],
    version = '0.3-alpha',
    description = 'Functional expressions for Autodesk Maya.',
    author = 'Gary Fixler',
    author_email = 'gfixler@gmail.com',
    url = 'https://github.com/gfixler/fmaya',
    download_url = 'https://github.com/gfixler/fmaya/archive/v0.2-alpha.tar.gz',
    license = 'GNU GPLv3',
    test_suite='nose.collector',
    tests_require['nose','rednose'],
)

