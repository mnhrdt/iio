x = iio_read("lena.png");
y = 255 - x;
iio_write("neg_lena.png", y);
