from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import os.path


def getmodulesetup():
   if os.path.exists('/usr/local/include/libraw') or os.path.exists('/usr/include/libraw'):
      print('LIBRAW detected')
      iiomodule = Extension('piio.libiio',  
          libraries = ['png','jpeg','tiff','raw'],
          #language=['c'],
          extra_compile_args = ['-DNDEBUG','-O3', '-DI_USE_LIBRAW'], 
          sources = ['piio/iio.c','piio/freemem.c','piio/libraw_interface.cpp']
         )
   else: 
      iiomodule = Extension('piio.libiio',  
          libraries = ['png','jpeg','tiff'],
          #language=['c'],
          extra_compile_args = ['-std=gnu99','-DNDEBUG','-O3'], 
          sources = ['piio/iio.c','piio/freemem.c']
         )
   return [iiomodule]



# custom build extends build_ext that and then copies the built 
# library to the current directory
class post_build_ext(build_ext):
   def run(self):

      # Call parent build_ext
      build_ext.run(self)

      print "running post_build_ext (copy libiio.so to piio)"
      # Recover the produced library and copy it to the piio directory
      files = self.get_outputs()
      # the current dir
      import shutil
      current_dir = os.path.dirname(os.path.abspath(__file__))
      for fname in files:
         shutil.copy(fname, os.path.join(current_dir,'piio'))


setup(
    name="piio",
    version="0.2.0",
    description="python iio wrapper",
    author="Gabriele Facciolo",
    author_email="contact@example.com",
    license='BSD',
    url='http://github.com//',
    packages=['piio'],
#    ext_package='piio',
    ext_modules = getmodulesetup(),
    cmdclass={"build_ext": post_build_ext}
   )


