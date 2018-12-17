from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(ext_modules=cythonize([
        Extension("cython_subscriber", ["cython_subscriber.pyx"], extra_compile_args=['-std=c11']),
        Extension("cython_publisher", ["cython_publisher.pyx"], extra_compile_args=['-std=c11'])
]))
