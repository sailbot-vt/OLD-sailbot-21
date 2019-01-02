from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

source_files = ["subscriber.c",
                "relay.c",
                "circular_buffer.c",
                "subscriber_list.c",
                "channel_list.c",
                "channel.c",
                "publisher.c"]

dirs = ["pthread.h", "types.h"]

extensions = [
        Extension(name="cython_subscriber",
                  sources=["cython_subscriber.pyx"] + source_files,
                  include_dirs=dirs,
                  compiler_directives={'language_level': 3},
                  extra_compile_args=['-std=gnu11']),
        Extension(name="cython_publisher",
                  sources=["cython_publisher.pyx"] + source_files,
                  include_dirs=dirs,
                  compiler_directives={'language_level': 3},
                  extra_compile_args=['-std=gnu11']),
        Extension(name="cython_relay",
                  sources=["cython_relay.pyx"] + source_files,
                  include_dirs=dirs,
                  compiler_directives={'language_level': 3},
                  extra_compile_args=['-std=gnu11'])
]

setup(ext_modules=cythonize(extensions))
