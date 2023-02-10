// basic functions for image input/output


#include <stdio.h>  // fprintf, fscanf, fgetc
#include <stdlib.h> // fopen, fclose, malloc, free

// auxiliary function to open a file or a standard stream
static FILE *xfopen(char *n, char *m)
{
	if (n[0] == '-' && !n[1] &&  m[0] == 'r')
		return stdin;
	if (n[0] == '-' && !n[1] &&  m[0] == 'w')
		return stdout;
	FILE *f = fopen(n, m);
	if (!f)
		exit(fprintf(stderr, "ERROR: cannot open file \"%s\"\n", n));
	return f;
}

// read a multi-channel image into an array of floats
float *iio_read_image_float_split(char *n, int *w, int *h, int *pd)
{
	FILE *f = xfopen(n, "r");
	int c, r = fscanf(f, "P%lc\n%d %d\n255", &c, w, h);
	float *x = 0;
	if (r != 3) goto end;
	if ('\n' != fgetc(f)) goto end;
	if (0) ;
	else if (c == '2') *pd = 1; // ascii PGM
	else if (c == '3') *pd = 3; // ascii PPM
	else goto end;
	//fprintf(stderr, "reading c=%c w=%d h=%d pd=%d\n", c, *w, *h, *pd);
	x = malloc(*w * *h * *pd * sizeof*x);
	if (!x) goto end;
	for (int j = 0; j < *h; j++)
	for (int i = 0; i < *w; i++)
	for (int l = 0; l < *pd; l++)
		if (1 != fscanf(f, "%g ", x + l*(*w * *h) + *w*j + i ))
		{
			free(x);
			x = 0;
			goto end;
		}
end:
	//fprintf(stderr, "\t[0]=%g\n", *x);
	fclose(f);
	return x;
}

// read a gray-scale image into an array of floats
float *iio_read_image_float(char *n, int *w, int *h)
{
	int pd;
	return iio_read_image_float_split(n, w, h, &pd);
}


// write an array of floats into an image file
void iio_write_image_float_split(char *n, float *x, int w, int h, int pd)
{
	FILE *f = xfopen(n, "w");
	if (pd == 3)
		fprintf(f, "P3\n%d %d 255\n", w, h);
	else if (pd == 1)
		fprintf(f, "P2\n%d %d 255\n", w, h);
	else
		exit(fprintf(stderr, "ERROR: cannot use pd=%d\n", pd));
	//fprintf(stderr, "writing w=%d h=%d pd=%d [0]=%g\n",w,h,pd,*x);
	for (int j = 0; j < h; j++)
	for (int i = 0; i < w; i++)
	for (int l = 0; l < pd; l++)
		fprintf(f, "%d\n", (int)x[l*w*h + w*j + i]);
	fclose(f);
}
