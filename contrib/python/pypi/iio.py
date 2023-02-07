
# TODO : 1. rewrite using cffi and keeping the same funcionality
# TODO : 2. create numpy array of the same sample type as the given file
#           (for that, use "iio_read_image_numbers_as_they_are_stored")


from os.path import abspath, dirname
from ctypes import CDLL, POINTER, c_float, c_int, c_char_p, c_void_p
from ctypes.util import find_library
import numpy

libiio = CDLL(f"{abspath(dirname(__file__))}/libiio.so")

libc = CDLL(find_library('c'))
libc.free.argtypes = [c_void_p]
libc.free.restype = c_void_p

iioread = libiio.iio_read_image_float_vec
iioread.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
iioread.restype = POINTER(c_float)

iiosave = libiio.iio_write_image_float_vec
iiosave.argtypes = [c_char_p, numpy.ctypeslib.ndpointer(c_float),c_int,c_int,c_int]
iiosave.restype = None

def read(filename):
	w = c_int()
	h = c_int()
	nch = c_int()

	ptr = iioread(filename.encode('utf-8'), w, h, nch)
	data = numpy.ctypeslib.as_array(ptr, (h.value, w.value, nch.value)).copy()
	libc.free(ptr)
	return data

def write(filename, data):
	h = data.shape[0]
	w = len(data.shape) <= 1 and 1 or data.shape[1]
	nch = len(data.shape) <= 2 and 1 or data.shape[2]

	data = numpy.ascontiguousarray(data, dtype='float32')
	iiosave(filename.encode('utf-8'), data, w, h, nch)

# TODO: detect if we are outside a notebook, and then do otherwise
def display(x):
	from tempfile import NamedTemporaryFile
	from base64 import b64encode
	from IPython.display import display, HTML
	from os import unlink

	f = NamedTemporaryFile(prefix="iioshow_", suffix=".jpg", delete=False)
	write(f.name, x)
	b = b64encode(open(f.name, "rb").read()).decode()
	unlink(f.name)
	display(HTML(f"<img src=\"data:image/jpeg;base64,{b}&#10;\"/>"))


# TODO: write a "gallery" function to display images in a css flip gallery


version = 5

__all__ = [ "read", "write", "display", "version" ]

