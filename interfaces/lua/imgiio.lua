local ffi = require("ffi")
local image = require("image")

--ffi.load("./iio.so", true)
--ffi.cdef[[
--float *iio_read_image_float_vec(const char *s, int *w, int *h, int *d);
--void iio_save_image_float_vec(const char *, float *x, int w, int h, int d);
--]]

local iio = {}

iio.read = function(fname)
	ffi.load("./iio.so", true)
	ffi.cdef[[
		float *iio_read_image_float_vec(const char*,int*,int*,int*);
	]]
	local w = ffi.new('int [1]')
	local h = ffi.new('int [1]')
	local pd = ffi.new('int [1]')
	local t = ffi.C.iio_read_image_float_vec(fname, w, h, pd)
	local x = image(w[0], h[0], pd[0])
	for i=0,#x do
		x.x[i] = t[i]
	end
	return x
end

iio.write = function(fname, x)
	ffi.load("./iio.so", true)
	ffi.cdef[[
		void iio_save_image_float_vec(const char*,float*,int,int,int);
	]]
	ffi.C.iio_save_image_float_vec(fname, x.x, x.w, x.h, x.pd)
end

return iio
