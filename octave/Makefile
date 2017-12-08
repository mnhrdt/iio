MEX    = mkoctfile --mex

LDLIBS = -lpng -ltiff -ljpeg
CFLAGS = -fPIC

BIN = iio_read.mex iio_write.mex

all: $(BIN)

%.mex : %.c iio.o ; $(MEX) $< iio.o $(LDLIBS)

clean :           ; $(RM) *.o *.mex neg_lena.png

test : $(BIN)     ; octave example_iio.m
