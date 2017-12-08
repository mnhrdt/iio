// octave/iio interface

#include <mex.h>
#include "iio.h"

// iio_write("lena.tiff", x)
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
	if (nlhs != 0 || nrhs != 2)
		return;

	const mwSize *dims = mxGetDimensions(prhs[1]);
	int ndims = mxGetNumberOfDimensions(prhs[1]);
	if (ndims >= 3) ndims = 3;

	int s[3] = {1, 1, 1};
	for (int i = 0; i < ndims; i++)
		s[i] = dims[i];

	double *x = mxGetPr(prhs[1]);
	char *f = mxArrayToString(prhs[0]);
	iio_write_image_double_vec(f, x, s[0], s[1], s[2]);
	mxFree(f);
}
