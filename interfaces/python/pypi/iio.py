
# TODO : 0. better handle the case when the image cannot be read (how?)
# TODO : 1. decide whether display and gallery should be the same function
# TODO : 2. rewrite using cffi and keeping the same funcionality
# TODO?: 3. create numpy array of the same sample type as the given file
#           (for that, use "iio_read_image_numbers_as_they_are_stored")
#           Caveat: numpy itself is not type-transparent, so this creates some
#           problems.  For example, a code may work or not depending on the
#           image file type.


# globally accessible C functions
__libc_free = 0
__iio_read  = 0
__iio_write = 0


# internal function to initialize the C interface
def __setup_functions():
	global __libc_free
	global __iio_read
	global __iio_write
	if (__libc_free != 0): return

	from os.path import abspath, dirname
	from ctypes import CDLL, POINTER, c_float, c_int, c_char_p, c_void_p
	from ctypes.util import find_library
	from numpy.ctypeslib import ndpointer

	libiio = CDLL(f"{abspath(dirname(__file__))}/libiio.so")

	libc = CDLL(find_library('c'))
	libc.free.argtypes = [c_void_p]
	libc.free.restype = c_void_p
	__libc_free = libc.free

	R = libiio.iio_read_image_float_vec
	R.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	R.restype = POINTER(c_float)
	__iio_read = R

	W = libiio.iio_write_image_float_vec
	W.argtypes = [c_char_p, ndpointer(c_float),c_int,c_int,c_int]
	W.restype = None
	__iio_write = W


# API
def read(filename):
	"""Read an image file into a numpy array of floats"""
	from ctypes import c_int
	from numpy.ctypeslib import as_array

	__setup_functions()

	w = c_int()
	h = c_int()
	d = c_int()

	p = __iio_read(filename.encode('utf-8'), w, h, d)
	x = as_array(p, (h.value, w.value, d.value)).copy()
	__libc_free(p)
	return x


# API
def write(filename, x):
	"""Write a numpy array into a named file"""
	from numpy import ascontiguousarray

	__setup_functions()

	h = x.shape[0]
	w = len(x.shape) <= 1 and 1 or x.shape[1]
	d = len(x.shape) <= 2 and 1 or x.shape[2]

	p = ascontiguousarray(x, dtype='float32')
	__iio_write(filename.encode('utf-8'), p, w, h, d)


# internal function to check if we are running inside a notebook
def __notebookP():
	try:
		x = get_ipython().config
		return True
	except NameError:
		return False

# internal function to do some notebook magic (only for gray images, by now)
def __heuristic_reshape(s):
	try:
		w = get_ipython().all_ns_refs[0]['w']
		h = get_ipython().all_ns_refs[0]['h']
		if s[0] == w*h:
			return (h,w)
		else:
			return s
	except (NameError, KeyError):
		return s

# internal function to urlencode a numpy array into html
def __img_tag_with_b64jpg(x):
	if (x.shape[0] > 4000):
		s = __heuristic_reshape(x.shape)
		if s == x.shape:
			return f'<b>cannot display image of size {x.shape}</b>'
		else:
			x = x.reshape(s)

	from tempfile import NamedTemporaryFile
	from base64 import b64encode
	from os import unlink

	f = NamedTemporaryFile(prefix="iioshow_", suffix=".jpg", delete=False)
	write(f.name, x)
	b = b64encode(open(f.name, "rb").read()).decode()
	unlink(f.name)
	return f"<img src=\"data:image/jpeg;base64,{b}&#10;\"/>"


# API
def display(x):
	"""Display the image inline (notebook or sixel terminal)"""
	if not __notebookP():
		write("-", x)
		return

	from IPython.display import display, HTML
	display(HTML(__img_tag_with_b64jpg(x)))


# API
def gallery(images):
	"""Display an array of images inline (notebook or sixel terminal)"""
	if not __notebookP():
		for x in images:
			write("-", x)
		return


	from  IPython.display import display, HTML

	L = ""  # html list of gallery items
	h = 0   # height of the gallery (height of the tallest image)
	i = 0   # loop counter
	for x in images:
		s = __heuristic_reshape(x.shape)
		h = max(h, s[0])
		j = __img_tag_with_b64jpg(x)
		L = f'{L}<li><a href="#">{i}<span>{j}</span></a>'
		i = i + 1

	html = f"""
	<div class="gallery2">
		<ul class="index">
			{L}
		</ul>
	</div>
	"""

	css = f"""
	<style>
	.gallery2 {{
		position: relative;
		width: auto;
		height: {h+20}px; }}    /* <- here is the f-format */
	.gallery2 .index {{
		padding: 0;
		margin: 0;
		width: 4.5em;
		list-style: none; }}
	.gallery2 .index li {{
		margin: 0;
		padding: 0;
		float: left;}}
	.gallery2 .index a {{ /* gallery2 item title */
		display: block;
		background-color: #EEEEEE;
		border: 1px solid #FFFFFF;
		text-decoration: none;
		width: 1.9em;
		padding: 6px; }}
	.gallery2 .index a span {{ /* gallery2 item content */
		display: block;
		position: absolute;
		left: -9999px; /* hidden */
		top: 0em;
		padding-left: 0em; }}
	.gallery2 .index a span img{{ /* gallery2 item content */
		/*height: 150px;*/
		}}
	.gallery2 .index li:first-child a span {{
		top: 0em;
		left: 4.5em;
		z-index: 99; }}
	.gallery2 .index a:hover {{
		border: 1px solid #888888; }}
	.gallery2 .index a:hover span {{
		left: 4.5em;
		z-index: 100; }}
	</style>
	"""

	display(HTML( html ))
	display(HTML( css ))


# API
version = 9

__all__ = [ "read", "write", "display", "gallery", "version" ]
