CFLAGS += -fPIC
LIBS = -lpng -ljpeg -ltiff

libiio.so: iio.o freemem.o
	$(CXX) -shared $^ -o $@ $(LIBS)

clean:
	$(RM) *.o libiio.so
