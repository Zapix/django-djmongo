import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-djmongo',
    version='0.0.1',
    author='Aleksandr Aibulatov',
    author_email='zap.aibulatov@gmail.com',
    description=('Django application for adding to Model mongo document'),
    license="BSD",
    keywords="django, application, model, mongodb, mongo",
    url='https://github.com/Zapix/django-djmongo',
    long_description=read('README'),
    packages = ['djmongo', 'testdjmongo'],
    install_requires = ['pymongo==2.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
