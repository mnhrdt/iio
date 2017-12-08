// octave/iio interface

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
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
	fprintf(stderr, "ndims = %d\n", ndims);

	int s[3] = {1, 1, 1};
	for (int i = 0; i < ndims; i++)
		s[i] = dims[i];


	for (int i = 0; i < ndims; i++)
		fprintf(stderr, "s[%d] = %d\n", i, s[i]);


	double *x = mxGetPr(prhs[1]);
	char *f = mxArrayToString(prhs[0]);
	iio_write_image_double_vec(f, x, s[0], s[1], s[2]);
	mxFree(f);
}
