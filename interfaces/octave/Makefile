MEX     = mex                # for matlab
MEX     = mkoctfile --mex    # for octave

LDLIBS  = -lpng -ltiff -ljpeg
CFLAGS  = -fPIC -march=native -O3

BIN     = iio_read.mex iio_write.mex

default : $(BIN)

%.mex   : %.c iio.o ; $(MEX) $< iio.o $(LDLIBS)

clean   :           ; $(RM) *.o *.mex neg_lena*.png lena_imwrite.png

test    : $(BIN)    ; octave --no-gui example_iio.m
