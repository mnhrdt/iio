// basic functions for image input/output

// read a gray-scale image into an array of floats
float *iio_read_image_float(char *fname, int *w, int *h);

// read a multi-channel image into an array of floats
float *iio_read_image_float_split(char *fname, int *w, int *h, int *pd);

// write an array of floats into an image file
void iio_write_image_float_split(char *fname, float *x, int w, int h, int pd);
