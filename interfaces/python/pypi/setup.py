



def extensions():
	from sysconfig import get_config_var
	from setuptools import Extension
	import sys

	extra_compile_args = get_config_var('CFLAGS').split()
	extra_compile_args += ["-DI_CAN_HAS_LIBWEBP"]
	#extra_compile_args += ["-DI_CAN_HAS_LIBHDF5"]
# NOTE: by now, "hdf5" is *not* a requirement, as it poses problems with colab
# (that uses an outdated version, apparently).  In the future we may propose
# pip options that enable or disable a few library combinations.

	extra_link_args = []
	if sys.platform == "darwin":
		extra_link_args = ["-L /usr/local/lib"]

	return [Extension("libiio",
			["iio/iio.c"],
			include_dirs=['iio', "/usr/local/include"],
			libraries=['png', 'jpeg', 'tiff', 'webp'], #, "hdf5"],
			library_dirs=["/usr/local/lib"],
			extra_compile_args=extra_compile_args,
			extra_link_args=extra_link_args
			)]
                        #depends=["iio/iio.h"])]


# from https://stackoverflow.com/a/38525461
from distutils.command.install_lib import install_lib as _install_lib

def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
	'''Same as os.rename, but returns the renaming result.'''
	import os
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
		import re
		matcher = re.compile('\.([^.]+)\.so$')
		return [batch_rename(file, re.sub(matcher, '.so', file))
			for file in outfiles]


from setuptools import setup
setup(name="iio",
	version='29',
	author="Jérémy Anger, Gabriele Facciolo, Enric Meinhardt-Llopis",
	author_email="enric.meinhardt@fastmail.com",
	description="Python wrapper to iio",
	url='https://github.com/mnhrdt/iio',
	classifiers=[
		"Operating System :: OS Independent",
	],
	py_modules=['iio'],
	ext_modules=extensions(),
	cmdclass={
		'install_lib': _CommandInstall,
	},
)

