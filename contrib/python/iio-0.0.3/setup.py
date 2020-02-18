from setuptools import setup, Extension

extensions = [Extension("libiio",
                        ["iio/iio.c"],
                        include_dirs=['iio'],
                        libraries=['png', 'jpeg', 'tiff'],
                        depends=["iio/iio.h"])]


# from https://stackoverflow.com/a/38525461
from distutils.command.install_lib import install_lib as _install_lib
import os
import re
def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    '''Same as os.rename, but returns the renaming result.'''
    os.rename(src, dst,
              src_dir_fd=src_dir_fd,
              dst_dir_fd=dst_dir_fd)
    return dst

class _CommandInstall(_install_lib):
    def __init__(self, *args, **kwargs):
        _install_lib.__init__(self, *args, **kwargs)

    def install(self):
        # let the distutils' install_lib do the hard work
        outfiles = _install_lib.install(self)
        # batch rename the outfiles:
        # for each file, match string between
        # second last and last dot and trim it
        matcher = re.compile('\.([^.]+)\.so$')
        return [batch_rename(file, re.sub(matcher, '.so', file))
                for file in outfiles]

setup(name="iio",
      version='0.0.3',
      author="Jérémy Anger, Gabriele Facciolo",
      author_email="angerj.dev@gmail.com",
      description="Python wrapper to iio",
      url='https://github.com/mnhrdt/iio',
      classifiers=[
          "Operating System :: OS Independent",
      ],
      py_modules=['iio'],
      ext_modules=extensions,
      cmdclass={
          'install_lib': _CommandInstall,
      },
)

