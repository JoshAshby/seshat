from distutils.core import setup
import seshat

setup(
    name='Seshat',
    version=seshat.__version__,
    author='Joshua P Ashby',
    author_email='joshuaashby@joshashby.com',
    packages=['seshat'],
    url='https://github.com/JoshAshby/seshat',
    license='GPL v3 (See LICENSE.txt for more info)',
    description='Fairly opinionated pet web framework.',
    long_description=open('README.rst').read(),
    install_requires=[
        "nose >= 1.3.0",
        "greenlet==0.4.2",
        "wsgiref==0.1.2"
    ],
)
