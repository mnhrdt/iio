floatrw : floatrw.o iio.o ; $(CC) $(LDFLAGS) $? $(LDLIBS) -o $@
clean   :                 ; rm -f floatrw *.o out.npy
test    : floatrw         ; ./floatrw in.npy out.npy && diff in.npy out.npy
