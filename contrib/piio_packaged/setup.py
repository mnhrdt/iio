from distutils.core import setup, Extension

import os.path

def getmodulesetup():
   if os.path.exists('/usr/local/include/libraw') or os.path.exists('/usr/include/libraw'):
      print('LIBRAW detected')
      iiomodule = Extension('piio.libiio',  
          libraries = ['png','jpeg','tiff','raw'],
          language=['c99'],
   #       extra_compile_args = ['-std=c99','-DNDEBUG','-O3'], 
          sources = ['piio/iio.c','piio/freemem.c', 'piio/libraw_interface.cpp']
         )
   else: 
      iiomodule = Extension('piio.libiio',  
          libraries = ['png','jpeg','tiff'],
          language=['c99'],
   #       extra_compile_args = ['-std=c99','-DNDEBUG','-O3'], 
          sources = ['piio/iio.c','piio/freemem.c']
         )
   return [iiomodule]



setup(
    name="piio",
    version="0.1.0",
    description="python iio wrapper",
    author="Gabriele Facciolo",
    author_email="contact@example.com",
    license='BSD',
    url='http://github.com//',
    packages=['piio'],
#    ext_package='piio',
    ext_modules = getmodulesetup()
   )
