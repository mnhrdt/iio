# Installation

> python setup.py install 




# Local Installation

> python setup.py install  --prefix=$HOME/local

Remember to set:
export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python2.6/site-packages


# Known issues

* If the compiler complains about "declarations that are only allowed in C99 mode" then use the following call to force the c99 dialect

    CC='gcc -std=c99' python setup.py install
