local ffi = require("ffi")

-- raw storage container
ffi.cdef[[
struct storage { int n; float x[?]; };
]]

-- metatable of the storage container
local storage
local mt = {
	__new = function(ctype,n)
		local x = ffi.new("struct storage", n)
		x.n = n;
		return x
	end,

	__len = function(x) return x.n end,

	--__newindex = function(x,i,v) x.x[i] = v end,
	--__index = function(x,i) return x.x[i] end,
}
storage = ffi.metatype("struct storage", mt)

-- storage tests
--print("STORAGE TESTS")
--x = storage(1000)
--print(x)
--print(#x)
--x[10] = 20
--x[20] = 30
--for i=0,6 do
--	print(x[10*i])
--end


-- tensor class

local image = {}
local mti = {}

image.nova = function(w,h)
	print(string.format("NOVA %d %d\n", w, h))
	local jo = {}
	print("novada")
	setmetatable(jo, mti)
	print("novada2")
	local sss = storage(w*h)
	print("novada3")
	jo.s = sss
	print("novada3")
	jo.w = w
	print("novada4")
	jo.h = h
	print("novada5")
	jo.offset = 0
	print("novada6")
	jo.stride = 1
	print("novada7")
	jo.nelems = w*h
	print("novada8")
	return jo
end

image.getfila = function(x,j)
	print("FILA")
	print(x)
	print(x.s)
	print(j)
	print(x.h)
	print(x.w)
	if (x.h > 1) then
		local fila = {}
		setmetatable(fila, mti)
		fila.s = x.s
		fila.w = x.w
		fila.h = 1
		fila.offset = j * x.w
		fila.stride = 1
		fila.nelems = x.w
		return fila
	else
		return x.s.x[x.offset + x.stride*j]
	end
end

image.assigna = function(x,i,v)
	print("assigna")
	print(x)
	print(i)
	print(v)
	if (x.h == 1) then
		print("som aqui")
		x.s.x[x.offset+x.stride*i] = v
		print("et voila")
	else
		print("ugly assignement")
	end
	print("assignat!")
end

mti.__index = image.getfila
mti.__newindex = image.assigna


print("a")
y = image.nova(800,600)
print("b")
print(y)
print(#y)
print(y.s)
print(#y.s)
--local caca = image.getfila(y, 3)
local f = y[10]
print("aqui")
print(f)
print(#f)
print(f.offset)
print(f.stride)
print(f.w)
print(f.h)
print("\n")
y[10][20] = 42
print(y[10][20])
