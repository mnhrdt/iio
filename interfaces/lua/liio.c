#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "iio.h"
#include "lua.h"
#include "lauxlib.h"

static int liio_sinus(lua_State *L)
{
	double d = lua_tonumber(L, 1); /* get argument */
	lua_pushnumber(L, sin(d)); /* push result */
	return 1; /* number of results */
}

static int liio_read_image_float_vec(lua_State *L)
{
	const char *filename = luaL_checkstring(L, 1);
	int w, h, pd;
	float *x = iio_read_image_float_vec(filename, &w, &h, &pd);
	void *ud = lua_newuserdata(L, w*h*pd*sizeof*x);
	fprintf(stderr, "read fname = \"%s\"\n", filename);
	fprintf(stderr, "\tw = %d\n", w);
	fprintf(stderr, "\th = %d\n", h);
	fprintf(stderr, "\tpd = %d\n", pd);
	fprintf(stderr, "\tp = %p, ud = %p\n", (void*)x, ud);
	lua_pushinteger(L, w);
	lua_pushinteger(L, h);
	lua_pushinteger(L, pd);
	memcpy(ud, x, w*h*pd*sizeof*x);
	free(x);
	return 4;
}

// (fname, x, w, h, pd)
static int liio_save_image_float_vec(lua_State *L)
{
	const char *filename = luaL_checkstring(L, 1);
	void *ud = lua_touserdata(L, 2);
	int w = luaL_checkinteger(L, 3);
	int h = luaL_checkinteger(L, 4);
	int pd = luaL_checkinteger(L, 5);
	fprintf(stderr, "write fname = \"%s\"\n", filename);
	fprintf(stderr, "\tw = %d\n", w);
	fprintf(stderr, "\th = %d\n", h);
	fprintf(stderr, "\tpd = %d\n", pd);
	fprintf(stderr, "\tud = %p\n", ud);
	iio_save_image_float_vec(filename, ud, w, h, pd);
	return 0;
}

// (x, w, h, pd, i, j, l)
static int liio_getsample(lua_State *L)
{
	float *x = lua_touserdata(L, 1);
	int w = luaL_checkinteger(L, 2);
	int h = luaL_checkinteger(L, 3);
	int pd = luaL_checkinteger(L, 4);
	int i = luaL_checkinteger(L, 5);
	int j = luaL_checkinteger(L, 6);
	int l = luaL_checkinteger(L, 7);
	float r = NAN;
	if (i >= 0 && j >= 0 && l >= 0 && i < w && j < h && l < pd)
		r = x[(j*w+i)*pd + l];
	lua_pushnumber(L, r);
	return 1;
}

// (x, w, h, pd, i, j, l, v)
static int liio_setsample(lua_State *L)
{
	float *x = lua_touserdata(L, 1);
	int w = luaL_checkinteger(L, 2);
	int h = luaL_checkinteger(L, 3);
	int pd = luaL_checkinteger(L, 4);
	int i = luaL_checkinteger(L, 5);
	int j = luaL_checkinteger(L, 6);
	int l = luaL_checkinteger(L, 7);
	float v = luaL_checknumber(L, 8);
	if (i >= 0 && j >= 0 && l >= 0 && i < w && j < h && l < pd)
		x[(j*w+i)*pd + l] = v;
	return 0;
}

static const struct luaL_Reg liio_functions[] = {
	{"sinus", liio_sinus},
	{"read_image_float_vec", liio_read_image_float_vec},
	{"save_image_float_vec", liio_save_image_float_vec},
	{"getsample", liio_getsample},
	{"setsample", liio_setsample},
	{NULL, NULL}
};

int luaopen_liio(lua_State *L)
{
	fprintf(stderr, "luaopen_liio\n");
	luaL_newlib(L, liio_functions);
	fprintf(stderr, "\t(after newlib)\n");
	return 1;
}
