local ffi = require("ffi")
ffi.load("./iio.so", true)
ffi.cdef[[
float *iio_read_image_float_vec(const char *s, int *w, int *h, int *d);
void iio_save_image_float_vec(const char *, float *x, int w, int h, int d);
]]

--print("at the beginning!")

iio_read_image_float_vec = function(fname)
	w = ffi.new('int [1]')
	h = ffi.new('int [1]')
	pd = ffi.new('int [1]')
	--print("before calling read")
	x = ffi.C.iio_read_image_float_vec(fname, w, h, pd)
	--print("after calling read")
	return x, w[0], h[0], pd[0]
end

iio_save_image_float_vec = function(fname, x, w, h, pd)
	ffi.C.iio_save_image_float_vec(fname, x, w, h, pd)
end

-- FROM NOW ON, THE CODE IS FFI-AGNOSTIC


x,w,h,pd = iio_read_image_float_vec("/tmp/lenak.png")

--print(w)
--print(h)
--print(pd)
--print(x)
--print(x[(100*w + 100)*pd + 0])
--print(x[(100*w + 100)*pd + 1])
--print(x[(100*w + 100)*pd + 2])

x[(100*w + 50)*pd + 0] = 0
x[(100*w + 50)*pd + 1] = 255
x[(100*w + 50)*pd + 2] = 0

for j = 0,h-1 do
for i = 0,w-2 do
for l = 0,pd-1 do
	x[(j*w+i)*pd+l] = x[(j*w+i+1)*pd+l] - x[(j*w+i)*pd+l]
end
end
end

iio_save_image_float_vec("oo.tiff", x, w, h, pd)
