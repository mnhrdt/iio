# read an image using iio
x = iio_read("lena.png");

# compute negative image
y = 255 - x;

# save an array into a png file
iio_write("neg_lena.png", y);

# save the original image using imwrite
imwrite(uint8(x), "lena_imwrite.png");
