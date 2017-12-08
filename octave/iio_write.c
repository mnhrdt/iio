// octave/iio interface

#include <mex.h>
#include <stdlib.h>
#include "iio.h"

// iio_write("lena.tiff", x)
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
	if (nlhs != 0 || nrhs != 2)
		return;

	const mwSize *dims = mxGetDimensions(prhs[1]);
	int ndims = mxGetNumberOfDimensions(prhs[1]);
	if (ndims >= 3) ndims = 3;

	int h = dims[0];
	int w = ndims > 1 ? dims[1] : 1;
	int d = ndims > 2 ? dims[2] : 1;

	double *X = mxGetPr(prhs[1]);
	double *x = malloc(w*h*d*sizeof*x);
	for (int j = 0; j < h; j++)
	for (int i = 0; i < w; i++)
	for (int k = 0; k < d; k++)
		x[(j*w+i)*d + k] = X[w*h*k + (i*h+j)];
	char *f = mxArrayToString(prhs[0]);
	iio_write_image_double_vec(f, x, w, h, d);
	mxFree(f);
	free(x);
}
