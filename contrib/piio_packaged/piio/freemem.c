#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void freemem(void *ptr){
   free(ptr);
}

void minmax(float *p, int N, float *vmin, float *vmax) {
   float imin = +INFINITY;
   float imax = -INFINITY;
   for ( int i=0;i<N;i++ ) {
      float pp = p[i];
      if ( isfinite(pp) ) {
         imin = fmin(imin, pp); 
         imax = fmax(imax, pp); 
      }
   }
   *vmin = imin;
   *vmax = imax;
}

void copy_tile(float *src, int nc, int nr, int nch, float *dst, int x0, int y0, int w, int h, int dst_nch) {
   for (int j=0;j<h;j++) {
   for (int i=0;i<w;i++) {
   for (int c=0;c<dst_nch;c++) {
      float v=0;
      int ii = x0+i;
      int jj = y0+j;
      if(ii>=0 && jj>=0 && ii < nc && jj < nr && c < nch) {
         v = src[ nch*(ii + jj*nc)+c ];
      }
      dst[ dst_nch*(i + j*w)+c ] = v;
   }
   }
   }
}
