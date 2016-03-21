local ffi = require("ffi")

-- image container (a simple C struct)
ffi.cdef[[
struct image { int w, h, pd, boundary; float x[?]; };
]]

-- metatable of the image container
local image
local mt = {
	-- constructor
	__new = function(ctype,w,h,pd)
		local x = ffi.new("struct image", w*h*pd)
		x.w = w;
		x.h = h
		x.pd = pd
		x.boundary = 0;
		return x
	end,

	-- length operator
	__len = function(x) return x.w * x.h * x.pd end,

	-- pixel-wise access with boundary condition
	__call = function(x,i,j,l)
		if (x.boundary == 0) then -- extrapolate by 0
			if (l < 0 or l >= x.pd) then return 0 end
			if (j < 0 or j >= x.h) then return 0 end
			if (i < 0 or i >= x.w) then return 0 end
			return x.x[x.pd*(j*x.w+i)+l]
		elseif (x.boundary == 1) then -- nearest neighbor extrapolation
			if (l < 0)     then l = 0        end
			if (j < 0)     then j = 0        end
			if (i < 0)     then i = 0        end
			if (l >= x.pd) then l = x.pd - 1 end
			if (j >= x.h)  then j = x.h - 1  end
			if (i >= x.w)  then i = x.w - 1  end
			return x.x[x.pd*(j*x.w+i)+l]
		elseif (x.boundary == 2) then -- periodic extrapolation
			i = i % x.w
			j = j % x.h
			l = l % x.pd
			return x.x[x.pd*(j*x.w+i)+l]
		else
			local idx = x.pd * (x.w * j + i) + l
			if (idx >= 0 and idx < #x) then
				return x.x[idx]
			else
				return 0
			end
		end
	end,

	-- pixel-wise access with square brackets
	__newindex = function(x, k, v)
		-- not yet implemented
		print("newindex")
		print(x)
		print(k)
		print(v)
	end,

	-- everything else
	__index = {
		setsample = function(x, i, j, l, v)
			if (l < 0 or l >= x.pd) then return end
			if (j < 0 or j >= x.h ) then return end
			if (i < 0 or i >= x.w ) then return end
			x.x[x.pd*(j*x.w+i)+l] = v
		end
	},
}
image = ffi.metatype("struct image", mt)

return image
