-- BIDIMA: a bidimensional array class for Lua
----------------------------------------------
-- Requirements:
--
-- 	-- intended to store huge arrays (e.g., images)
-- 	w,h = 3000,2000
-- 	a = bidima(w,h)
--
--	-- accessible with two indices for reading and for writing
-- 	for j=0,h-1 do
-- 	for i=0,w-1 do
-- 		a[j][i] = 2 *  a[j][i]
-- 	end
-- 	end
--
--	-- numbers are contiguous and accessible
-- 	for i=0,w*h-1 do
-- 		a.buf[i] = i
-- 	end
--
--	-- no copy unless explicity requested
-- 	a[10][20] = 42
-- 	b = a
-- 	print(b[10][20]) -- prints 42
--

-- basic storage (could be replaced by SSI)
function storage_new(n)
	local s = {}
	for i=1,n do
		s[i] = i
	end
	print(string.format("STORAGE NEW %s of size %d", s, n))
	return s
end

function storage_get(s, i)
	--print(string.format("STORAGE GET %s [%d] = %g", s, i, s[i]))
	return s[i+1]
end

function storage_set(s, i, v)
	--print(string.format("STORAGE SET %s [%d] = %g", s, i, v))
	s[i+1] = v
end

-- test the storage
local x = storage_new(1000)
local v = storage_get(x, 10)
storage_set(x, 20, 42)
local w = storage_get(x, 20)
print(w)


-- metatable for image class
local mti = {}

-- create a new image with its own storage
image_new = function(w, h)
	local new = {}
	local s = storage_new(w*h)
	print(string.format("IMAGE NEW %s {%s} %d %d", new, s, w, h))
	new.s, new.w, new.h = s, w, h
	new.offset = 0
	new.stride = 1
	new.nelems = w*h
	setmetatable(new, mti)
	return new
end


-- eval one dimension of an image
image_contract = function(self, idx)
	--print(string.format("IMAGE CONTRACT %s %s", self, idx))
	--for k,v in pairs(self) do print(string.format("\t%s %s", k, v)) end
	if (self.h == 1) then
		--print("access row")
		local s = self.s
		local offset = self.offset
		local stride = self.stride
		return storage_get(s, offset + stride * idx)
	else
		--print("access column")
		local fila = {}
		fila.s = self.s
		fila.w = self.w
		fila.h = 1
		fila.offset = idx * fila.w
		fila.stride = 1
		fila.nelems = fila.w
		setmetatable(fila, mti)
		return fila
	end
end

-- set one value (only if h=1)
image_setpoint = function(self, i, v)
	--print(string.format("IMAGE SETPOINT %s %s %s", self, i, v))
	--print(self.h)
	--print(self.s)
	--print(self.offset)
	--print(self.stride)
	if (self.h == 1) then
		local s = self.s
		local offset = self.offset
		local stride = self.stride
		return storage_set(s, offset + stride * i, v)
	else
		print("")
		print("")
		print("")
		print("error BAD CACA")
		print("")
		print("")
		print("")
	end
end

-- metatable
mti.__index = image_contract
mti.__newindex = image_setpoint

-- tests without metatable
print("tests without metatable")
x = image_new(1000,1000)
print("a")
x3 = image_contract(x, 3)
print("b")
x33 = image_contract(x3, 3)
print("c")
print(x)
print(x3)
print(x33)
image_setpoint(x3, 3, 42)

-- tests of metatable
print("tests with metatable")
y3 = x[3]
print("AAA")
y33 = x[3][3]
print(y33)

x[10][10] = 42
z = x[10][10]
print(z)

for j=1,x.h do
for i=1,x.w do
	x[j][i] = i+j*x.w
end
end
acc = 0
for j=1,x.h do
for i=1,x.w do
	acc = acc + x[j][i]
end
end
print(acc)
