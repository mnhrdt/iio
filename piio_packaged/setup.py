from distutils.core import setup, Extension


iiomodule = Extension('piio.libiio',  
      libraries = ['png','jpeg','tiff'],
      language=['c99'],
      extra_compile_args = ['-std=c99','-DNDEBUG','-O3'], 
      sources = ['piio/iio.c','piio/freemem.c']
      )


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
    ext_modules = [iiomodule]
)
