% read an image using iio
x = iio_read('lena.png');

% compute negative image
y = 255 - x;

% save an array into a png file
iio_write('neg_lena.png', y);
iio_write('neg_lena_double.tiff',       y );
iio_write('neg_lena_single.tiff',single(y));
iio_write('neg_lena_uint16.tiff',uint16(y));
iio_write('neg_lena_int8.tiff'  ,int8(  y/2));
iio_write('neg_lena_int16.tiff' ,int16( y));
iio_write('neg_lena_int32.tiff' ,int32( y));
% iio_write('neg_lena_int64.tiff' ,uint32(y));
iio_write('neg_lena_uint8.tiff' ,uint8( y));

% save the original image using imwrite
imwrite(uint8(x), 'lena_imwrite.png');
