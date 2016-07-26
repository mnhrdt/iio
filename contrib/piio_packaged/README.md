# Installation

> python setup.py install 


# Local Installation

> python setup.py install  --prefix=$HOME/local

Remember to set:
export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python2.6/site-packages


# Known issues

* If the compiler complains about "declarations that are only allowed in C99 mode" then use the following call to force the c99 dialect

    CC='gcc -std=c99' python setup.py install


# ./setup.py and piio/setup.py  Why so many setup? 

The key for piio is to have library file in piio/libiio.so.

Building piio using either of the two setup.py would create piio/libiio.so. 
This allows to use piio as a module without installing it on the system. 
The first setup.py have a more standard distutils structure, while the 
second (piio/setup.py) is used to build piio during its first import 
(which is used by https://github.com/gfacciol/pvflip).

The distutil setup scripts have limited capailities when it comes to detecting 
the system libraries. A library with more functionalities (ie OpenEXR) can be 
built using the CMakeList.txt located in the piio directory.

The above scripts are only tested to Unix systems. For Windows installations a
precompiled WIN32 library could be downloaded from:
https://github.com/gfacciol/pvflip/tree/master/piio/WIN32

