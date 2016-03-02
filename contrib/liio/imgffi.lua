local ffi = require("ffi")

-- image container (a simple C struct)
ffi.cdef[[
struct image { int w, h, pd; float x[?]; };
]]

local image
local mt = {
	__new = function(ctype,w,h,pd)
		local x = ffi.new("struct image", w*h*pd)
		x.w = w;
		x.h = h
		x.pd = pd
		return x
	end,
	__len = function(x) return x.w * x.h * x.pd end,
	__call = function(x,i,j,l)
		local idx = x.pd * (x.w * j + i) + l
		if (idx >= 0 and idx < #x) then
			return x.x[idx]
		else
			return 0
		end
	end
}
image = ffi.metatype("struct image", mt)

----first, image without metatables
--local w = 800
--local h = 600
--local pd = 3
--local x = image(w, h, pd)
--
--print("construction constructed!\n")
--
--for j=0,h-1 do
--for i=0,w-1 do
--for l=0,pd-1 do
--	idx = x.pd * (j * x.w + i) + l
--	x.x[idx] = 127+127*(l*math.sin(i/10.0)+math.sin((l+1)*j/20.0))
--end
--end
--end
--
--print("computation computed!\n")



ffi.load("./iio.so", true)
ffi.cdef[[
float *iio_read_image_float_vec(const char *s, int *w, int *h, int *d);
void iio_save_image_float_vec(const char *, float *x, int w, int h, int d);
]]

iio_read = function(fname)
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

iio_write = function(fname, x)
	ffi.C.iio_save_image_float_vec(fname, x.x, x.w, x.h, x.pd)
end



--iio_write("cusa.tiff", x)


local y = iio_read("/tmp/barbara.png")
print("image has been read")
--print(y:p(10,20,0))
local w = y.w
local h = y.h
local pd = y.pd
print(w)
print(h)
print(pd)
for j = 0,h-1 do
for i = 0,w-1 do
for l = 0,pd-1 do
	--y.x[(j*w+i)*pd+l] = y.x[(j*w+i+1)*pd+l] - y.x[(j*w+i)*pd+l]
	y.x[(j*w+i)*pd+l] = y(i+1,j,l) - y(i,j,l)
end
end
end
print("computation has been computed")
iio_write("kuza.tiff", y)
print("image has been written")
