#include <math.h>
#include "lua.h"
#include "lauxlib.h"

static int liio_sinus (lua_State *L) {
	double d = lua_tonumber(L, 1); /* get argument */
	lua_pushnumber(L, sin(d)); /* push result */
	return 1; /* number of results */
}

static const struct luaL_Reg liio_functions [] = {
	{"sinus", liio_sinus},
	{NULL, NULL}
};

int luaopen_liio (lua_State *L) {
	luaL_newlib(L, liio_functions);
	return 1;
}
