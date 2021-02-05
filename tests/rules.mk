BIN    = floatrw
OBJ    = iio.o

$(BIN) : $(OBJ)
clean  :        ; $(RM) $(BIN) $(OBJ) out.npy
test   : $(BIN) ; ./floatrw in.npy out.npy && diff in.npy out.npy
