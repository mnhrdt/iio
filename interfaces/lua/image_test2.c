#include "iio.h"
int main()
{
	int w, h, pd;
	float *y = iio_read_image_float_vec("/tmp/n.png", &w, &h, &pd);
	for (int j = 0; j < h; j++)
	for (int i = 0; i < w-1; i++)
	for (int l = 0; l < pd; l++)
	{
		int idx = ( j*w + i ) * pd + l;
		y[idx] = y[idx+pd] - y[idx];
	}
	iio_save_image_float_vec("ckuza.tiff", y, w, h, pd);
	return 0;
}
