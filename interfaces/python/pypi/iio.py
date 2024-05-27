
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
	if __libc_free != 0: return

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

# internal function to find a variable up the call stack
def __upvar(s):
	import inspect
	f = inspect.currentframe().f_back
	while hasattr(f, 'f_back'):
		if s in f.f_locals:
			return f.f_locals[s]
		f = f.f_back
	return None

# internal function to do some notebook magic (only for gray images, by now)
def __heuristic_reshape(s):
	try:
		w = __upvar("w")
		h = __upvar("h")
		if s[0] == w*h:
			return (h,w)
		else:
			return s
	except (NameError, KeyError, TypeError):
		return s

# internal function to urlencode a numpy array into html
def __img_tag_with_b64(x, p=False):
	if (x.shape[0] > 4000):
		s = __heuristic_reshape(x.shape)
		if s == x.shape:
			return f'<b>cannot display image of size {x.shape}</b>'
		else:
			x = x.reshape(*s,-1)

	from tempfile import NamedTemporaryFile
	from base64 import b64encode
	from os import unlink
	from numpy import unique

	t = "png" if p or len(unique(x)) < 8 else "jpeg"
	f = NamedTemporaryFile(prefix="iioshow_", suffix=f".{t}", delete=False)
	write(f.name, x)
	b = b64encode(open(f.name, "rb").read()).decode()
	unlink(f.name)
	return f"<img src=\"data:image/{t};base64,{b}&#10;\"/>"


# encode the floating-point numbers of the array into a dataurl
def __raw_dataurl(x):
	from numpy import ascontiguousarray
	from base64 import b64encode
	p = ascontiguousarray(x, dtype='float32')
	b = b64encode(p).decode()
	return f"data:;base64,{b}&#10;"

# API
def display(x):
	"""Display the image inline (notebook or sixel terminal)"""
	if not __notebookP():
		write("-", x)
		return

	from IPython.display import display, HTML
	display(HTML(__img_tag_with_b64(x)))


# internal function to get the variable names of the "gallery" function
def __upnames():
	from inspect import currentframe, getframeinfo
	import re
	f = currentframe().f_back.f_back           # frame of caller's caller
	s = getframeinfo(f).code_context[0]        # extract call string
	t = s.split('[',1)[-1].rsplit(']',1)[0]    # get contents of call list
	z = re.split(r",\s*(?![^][()]*[\)\]])", t) # split at non-bracket commas
	return z

# API
def gallery(images):
	"""Display an array of images inline (notebook or sixel terminal)"""
	if not __notebookP():
		for x in images:
			write("-", x)
		return

	n = __upnames()  # list of variable names upon call
	L = ""           # html list of gallery items
	H = 0            # height of the gallery (height of the tallest image)
	i = 0            # loop counter
	for x in images:
		z = __heuristic_reshape(x.shape)
		H = max(H, z[0])
		j = __img_tag_with_b64(x)
		s = n[i] if len(n) == len(images) else f"{i}"
		L = f'{L}<li><a href="#">{s}<span>{j}</span></a>\n'
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
		height: {H+20}px; }}    /* <- here is the f-format */
	.gallery2 .index {{
		padding: 0;
		padding-left: 0;
		margin: 0;
		width: 12.5em;
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
		width: 12.5em;
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
		left: 12.5em;
		z-index: 99; }}
	.gallery2 .index a:hover {{
		border: 1px solid #888888; }}
	.gallery2 .index a:hover span {{
		left: 12.5em;
		z-index: 100; }}
	</style>
	"""

	html = html.replace("gallery2", f"gallery{H}")
	css  = css .replace("gallery2", f"gallery{H}")
	# TODO: widen the gallery legend so that the longest item name fits

	from  IPython.display import display, HTML
	display(HTML( html ))
	display(HTML( css  ))


# internal function with the CSS styling for the cpu html viewer
def __cpucss(x):
	return """
	.cpu {
		width: 600px;
		height: 400px;
		overflow: hidden;
		border: 1px solid #000;
		background: #ccc;
	}

	.cpu > img {
		image-rendering: crisp-edges;
	}
	""".replace("cpuX", x)

# internal function with the Javascript code of the cpu html viewer
def __cpujs(x):
	return """
	// get unique cpu element
	const cpuX = document.getElementById("cpuX");

	// initialize state of this cpu element
	for (const c of [cpuX])
	{
		c.tabIndex = 0;
		c.dataset.active = "false";
		c.dataset.isPanning = "false";
		viewport_reset_cpuX();
	}

	function viewport_reset_cpuX() {
		const c = cpuX;
		c.dataset.offsetX = 0;
		c.dataset.offsetY = 0;
		c.dataset.scale = 1;
		c.dataset.brightness = 1;
		c.dataset.contrast = 100;
	}

	function viewport_offset_cpuX(dx, dy) {
		const c = cpuX;
		c.dataset.offsetX = Number(c.dataset.offsetX) + Number(dx);
		c.dataset.offsetY = Number(c.dataset.offsetY) + Number(dy);
	}

	function viewport_scale_cpuX(x, y, lds) {
		const c = cpuX;
		const cx = (x - Number(c.dataset.offsetX))/Number(c.dataset.scale);
		const cy = (y - Number(c.dataset.offsetY))/Number(c.dataset.scale);
		c.dataset.scale = lds * Number(c.dataset.scale);
		c.dataset.offsetX = x - cx * Number(c.dataset.scale);
		c.dataset.offsetY = y - cy * Number(c.dataset.scale);
	}

	function brightness_change_cpuX(d) {
		const c = cpuX;
		let b = Number(c.dataset.brightness);
		if (d < 0)
			b = b - 0.05;
		else
			b = b + 0.05;
		if (b < 0)
			b = 0;
		if (b > 9)
			b = 9;
		c.dataset.brightness = b;
	}

	function contrast_change_cpuX(d) {
		const c = cpuX;
		let b = Number(c.dataset.contrast);
		if (d < 0)
			b = b - 5;
		else
			b = b + 5;
		if (b < 0)
			b = 0;
		if (b > 900)
			b = 900;
		c.dataset.contrast = b;
	}

	function apply_transforms_cpuX() {
		const c = cpuX;
		const x = Number(c.dataset.offsetX);
		const y = Number(c.dataset.offsetY);
		const s = Number(c.dataset.scale);
		const z = Number(c.dataset.brightness);
		const t = Number(c.dataset.contrast);
		for (const i of c.getElementsByTagName("img")) {
			i.style.transformOrigin = `left top`;
			i.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
			i.style.filter = `brightness(${z}) saturate(${t}%)`;
		}
	}

	function cpu_xy_cpuX(e) {
		const c = cpuX;
		const r = c.getBoundingClientRect();
		const x = e.clientX - r.x;
		const y = e.clientY - r.y;
		return [x,y];
	}

	for (const c of [cpuX])
	c.addEventListener("wheel", function(e) {
		if (c.dataset.active == "false") return;
		e.preventDefault();
		if (e.shiftKey) { // brightness change
			brightness_change_cpuX(e.deltaY);
		} else if (e.ctrlKey) { // contrast change
			contrast_change_cpuX(e.deltaY);
		} else { // zoom
			const factor = e.deltaY > 0 ? 2 : 0.5;
			const [x,y]= cpu_xy_cpuX(e);
			viewport_scale_cpuX(x, y, factor)
		}
		apply_transforms_cpuX();
	});


	for (const c of [cpuX])
	c.addEventListener("mousedown", function(e) {
		e.preventDefault();
		if (e.which == 3) {
			viewport_reset_cpuX();
			apply_transforms_cpuX();
		} else {
			c.dataset.active = "true";
			c.focus();
			c.dataset.isPanning = "true";
			const [x,y] = cpu_xy_cpuX(e);
			c.dataset.startX = x;
			c.dataset.startY = y;
			c.style.cursor = "grabbing";
		}
	});

	for (const c of [cpuX])
	c.addEventListener("mousemove", function(e) {
		if (c.dataset.isPanning == "true") {
			e.preventDefault();
			const [x,y]= cpu_xy_cpuX(e);
			const dx = x - Number(c.dataset.startX);
			const dy = y - Number(c.dataset.startY);
			viewport_offset_cpuX(dx, dy);
			apply_transforms_cpuX();
			c.dataset.startX = x;
			c.dataset.startY = y;
		}
	});

	for (const c of [cpuX])
	c.addEventListener("mouseup", function(e) {
		if (c.dataset.isPanning == "true") {
			c.dataset.isPanning = "false";
			c.style.cursor = "grab";
		}
	});

	for (const c of [cpuX])
	c.addEventListener("mouseleave", function(e) {
		c.dataset.isPanning = "false";
	});

	for (const c of [cpuX])
	c.addEventListener("keyup", function(e) {
		if (e.key == "q" || e.key == "Escape") {
			c.dataset.active = "false";
			document.activeElement.blur();
		}
		if (e.key == "r") {
			viewport_reset_cpuX();
			apply_transforms_cpuX();
		}
	});
	""".replace("cpuX", x)


# API: access to the interactive viewer
# NOTE: maybe rename to "cpu" ?
def explore(x):
	"""Display the image inline (notebook or sixel terminal)"""
	if not __notebookP():
		# should run the acutal "cpu" here, if available
		write("-", x)
		return

	explore.cx = getattr(explore, "cx", 0) + 1  # static counter

	from IPython.display import display, HTML, Javascript
	i = f"cpu{explore.cx}"
	h = f"<div class=\"cpu\" id=\"{i}\">{__img_tag_with_b64(x,True)}</div>"
	c = f"<style>{__cpucss(i)}</style>"
	j = __cpujs(i)
	display(HTML(h))
	display(HTML(c))
	display(Javascript(j));


# API
version = 21

__all__ = [ "read", "write", "display", "gallery", "explore", "version" ]
