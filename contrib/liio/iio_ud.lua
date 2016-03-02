local iio = require "liio"

x,w,h,pd = iio.read_image_float_vec("/tmp/lenak.png")

a = iio.getsample(x, w, h, pd, 50, 100, 0)
b = iio.getsample(x, w, h, pd, 50, 100, 1)
c = iio.getsample(x, w, h, pd, 50, 100, 2)
print(a,b,c)
iio.setsample(x, w, h, pd, 50, 100, 0, 0)
iio.setsample(x, w, h, pd, 50, 100, 1, 255)
iio.setsample(x, w, h, pd, 50, 100, 2, 0)

--x[(100*w + 50)*pd + 0] = 0
--x[(100*w + 50)*pd + 1] = 255
--x[(100*w + 50)*pd + 2] = 0
--
--for j = 0,h-1 do
--for i = 0,w-2 do
--for l = 0,pd-1 do
--	x[(j*w+i)*pd+l] = x[(j*w+i+1)*pd+l] - x[(j*w+i)*pd+l]
--end
--end
--end

iio.save_image_float_vec("oo.tiff", x, w, h, pd)
