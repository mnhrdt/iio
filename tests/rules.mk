BIN    = floatrw
OBJ    = floatrw.o iio.o
$(BIN) : $(OBJ) ; $(CC) $(LDFLAGS) $? $(LDLIBS) -o $@
clean  :        ; rm -f $(BIN) $(OBJ) out.npy
test   : $(BIN) ; ./floatrw in.npy out.npy && diff in.npy out.npy
