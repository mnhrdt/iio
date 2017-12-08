LDLIBS="-lpng -ltiff -ljpeg"
cc -c -fPIC iio.c
mkoctfile --mex iio_read.c iio.o $LDLIBS
mkoctfile --mex iio_write.c iio.o $LDLIBS
