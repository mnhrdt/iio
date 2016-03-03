local image = require("image")
local iio = require("imgiio")

--first, image without metatables
local w = 800
local h = 600
local pd = 3
local x = image(w, h, pd)

print("construction constructed!\n")

for j=0,h-1 do
for i=0,w-1 do
for l=0,pd-1 do
	idx = x.pd * (j * x.w + i) + l
	x.x[idx] = 127+127*(l*math.sin(i/10.0)+math.sin((l+1)*j/20.0))
end
end
end

print("computation computed!\n")

iio.write("coseta.tiff", x)
