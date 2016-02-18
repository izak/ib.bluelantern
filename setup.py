from setuptools import setup, find_packages

setup(
    name='ib.bluelantern',
    version='0.1',
    description="A framework for integrating information from charge controllers and inverters",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    keywords='python renewable energy',
    author='Izak Burger',
    author_email='isburger@gmail.com',
    url='https://github.com/izak/ib.bluelantern',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir = {'' : 'src'},
    namespace_packages=['ib'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'paho-mqtt',
        'pyramid >= 1.6.1',
        'waitress'
    ],
    extras_require = {
        'mk2': ['ib.victron'],
        'bluesolar': ['pyserial']
    },
    entry_points="""\
        [paste.app_factory]
        main = ib.bluelantern:main
    """,
)
