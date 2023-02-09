
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

def __img_tag_with_b64jpg(x):
	from tempfile import NamedTemporaryFile
	from base64 import b64encode
	from os import unlink

	f = NamedTemporaryFile(prefix="iioshow_", suffix=".jpg", delete=False)
	write(f.name, x)
	b = b64encode(open(f.name, "rb").read()).decode()
	unlink(f.name)
	return f"<img src=\"data:image/jpeg;base64,{b}&#10;\"/>"

# TODO: detect if we are outside a notebook, and then do otherwise
def display(x):
	from IPython.display import display, HTML
	display(HTML(__img_tag_with_b64jpg(x)))

def gallery(images, image_labels=None):
	from  IPython.display import display, HTML

	L = ""  # html list of gallery items
	h = 0   # height of the gallery (height of the tallest image)
	i = 0   # loop counter
	for x in images:
		h = max(h, x.shape[0])
		j = __img_tag_with_b64jpg(x)
		L = f'{L}<li><a href="#">{i}<span>{j}</span></a></li>'
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



version = 6

__all__ = [ "read", "write", "display", "gallery", "version" ]

