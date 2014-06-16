from distutils.core import setup

setup(
    name='custom_filer',
    version='0.140616',
    author='Hamish Downer',
    author_email='support+custom_filer@aptivate.org',
    packages=['custom_filer'],
    url='http://github.com/aptivate/custom_filer',
    license='LICENSE.txt',
    description='Extensions for Django filer',
    install_requires=[
        "django >= 1.5",
    ],
)
