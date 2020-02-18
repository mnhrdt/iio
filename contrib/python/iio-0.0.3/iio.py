import os.path
import ctypes
from ctypes import *
from ctypes.util import find_library
import numpy as np

libiio = CDLL(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libiio.so'))

libc = ctypes.CDLL(find_library('c'))
libc.free.argtypes = [ctypes.c_void_p]
libc.free.restype = ctypes.c_void_p

iioread = libiio.iio_read_image_float_vec
iioread.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
iioread.restype = POINTER(c_float)

iiosave = libiio.iio_write_image_float_vec
iiosave.argtypes = [c_char_p, np.ctypeslib.ndpointer(c_float),c_int,c_int,c_int]
iiosave.restype = None

def read(filename):
   w = c_int()
   h = c_int()
   nch = c_int()

   ptr = iioread(filename.encode('utf-8'), w, h, nch)
   data = np.ctypeslib.as_array(ptr, (h.value, w.value, nch.value)).copy()
   libc.free(ptr)
   return data

def write(filename, data):
   h = data.shape[0]
   w = len(data.shape) <= 1 and 1 or data.shape[1]
   nch = len(data.shape) <= 2 and 1 or data.shape[2]

   data = np.ascontiguousarray(data, dtype='float32')
   iiosave(filename.encode('utf-8'), data, w, h, nch)

__all__ = {
    'read': read,
    'write': write,
}

