#include "iio.h"
int main(int c, char *v[])
{
	char *filename_in  = c > 1 ? v[1] : "-";
	char *filename_out = c > 2 ? v[2] : "-";
	int w, h, pd;
	float *x = iio_read_image_float_vec(filename_in, &w, &h, &pd);
	iio_write_image_float_vec(filename_out, x, w, h, pd);
	return 0;
}
