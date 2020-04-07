from setuptools import setup, Extension
from sysconfig import get_config_var
from subprocess import check_output

h5_f = str(check_output(["pkg-config", "--cflags", "hdf5"]), "utf8").split()
h5_l = str(check_output(["pkg-config", "--libs"  , "hdf5"]), "utf8").split()

extra_compile_args = get_config_var('CFLAGS').split()
extra_compile_args += ["-DI_CAN_HAS_LIBHDF5"]
extra_compile_args += h5_f
extra_link_args = h5_l

extensions = [Extension("libiio",
                        ["iio/iio.c"],
                        include_dirs=['iio'],
                        libraries=['png', 'jpeg', 'tiff', "hdf5"],
                        extra_compile_args=extra_compile_args,
                        extra_link_args=extra_link_args,
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
      version='0.0.4a2',
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

