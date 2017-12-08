// octave/iio interface

#include <mex.h>
#include "iio.h"

// x = iio_read("lena.tiff");
// [x,y,z] = iio_read("lena.tiff", "barbara.tiff", "baboon.png");
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
	if (nlhs != nrhs)
		return;

	for (int i = 0; i < nrhs; i++)
	{
		char *f = mxArrayToString(prhs[i]);
		int s[3];
		double *x = iio_read_image_double_vec(f, s, s+1, s+2);
		mxFree(f);
		if (!x) continue;
		mwSize S[3] = {s[0], s[1], s[2]};
		plhs[i] = mxCreateNumericArray(3, S, mxDOUBLE_CLASS, mxREAL);
		double *X = mxGetPr(plhs[i]);
		for (int j = 0; j < s[0]*s[1]*s[2]; j++)
			X[j] = x[j];
		iio_free(x);
	}
}
