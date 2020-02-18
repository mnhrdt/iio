local iio = require("imgiio")

local y = iio.read("/tmp/n.png")

local t = os.clock()
print("TIME")

-- the algorithm
y.boundary = 1
for j = 0, y.h - 1 do
for i = 0, y.w - 2 do
for l = 0, y.pd - 1 do
	idx = (j * y.w + i) * y.pd + l
	--y.x[idx] = y(i+1,j,l) - y(i,j,l)
	y.x[idx] = y.x[idx + y.pd] - y.x[idx];
end
end
end

print(os.clock() - t)

iio.write("kuza.tiff", y)
