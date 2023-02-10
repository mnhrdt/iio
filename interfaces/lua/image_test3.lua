local image = require("image")
--local iio = require("imgiio")

--first, image without metatables
local n = 800
local x = image(n, n, 1)
local y = image(n, n, 1)
local z = image(n, n, 1)

for i = 0, n*n - 1 do
	x.x[i] = math.random()
	y.x[i] = math.random()
end

print("construction started!\n")

for i = 0, n-1 do
for j = 0, n-1 do
	local a = 0
	for k = 0, n-1 do
		a = a + x.x[j*n+k] * y.x[k*n+i]
	end
	z.x[j*n+i] = a
end
end

print("construction constructed!\n")


--iio.write("cosetax.tiff", x)
--iio.write("cosetay.tiff", y)
--iio.write("cosetaz.tiff", z)
