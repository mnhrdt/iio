/* -*- C++ -*-
 * File: libraw_interface.cpp
 * Copyright 2016 Gabriele Facciolo (gfacciol@gmail.com)
 *
 * Based on LibRaw sample: unprocessed_raw.cpp
 * Copyright 2009-2015 LibRaw LLC (info@libraw.org)
 *
 * libraw_interface
 * Reads an unprocessed raw image and interfaces with iio 
 *

 LibRaw is free software; you can redistribute it and/or modify
 it under the terms of the one of three licenses as you choose:

 1. GNU LESSER GENERAL PUBLIC LICENSE version 2.1
 (See file LICENSE.LGPL provided in LibRaw distribution archive for details).

 2. COMMON DEVELOPMENT AND DISTRIBUTION LICENSE (CDDL) Version 1.0
 (See file LICENSE.CDDL provided in LibRaw distribution archive for details).

 3. LibRaw Software License 27032010
 (See file LICENSE.LibRaw.pdf provided in LibRaw distribution archive for details).

*/
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#ifndef WIN32
#include <netinet/in.h>
#else
#include <sys/utime.h>
#include <winsock2.h>
#endif

#include "libraw/libraw.h"

extern "C" {
#include "iio.h"
   struct iio_image {
      int dimension;        // 1, 2, 3 or 4, typically
      int sizes[IIO_MAX_DIMENSION];
      int pixel_dimension;
      int type;             // IIO_TYPE_*

      int meta;             // IIO_META_*
      int format;           // IIO_FORMAT_*

      bool contiguous_data;
      bool caca[3];
      void *data;
   };
}

#if !(LIBRAW_COMPILE_CHECK_VERSION_NOTLESS(0,14))
#error This code is for LibRaw 0.14+ only
#endif

extern "C" {
   int try_reading_file_with_libraw(const char *fname, struct iio_image *x);
   int try_reading_file_with_libraw_4channels(const char *fname, struct iio_image *x);
}



// reads the RAW as it is
int try_reading_file_with_libraw(const char *fname, struct iio_image *x)
{
   int ret;
   int verbose=0;
   int shot_select = 0;

   LibRaw RawProcessor;

#define S RawProcessor.imgdata.sizes
#define OUT RawProcessor.imgdata.params

   //
   //OUT.shot_select=shot_selected;

   if(verbose) fprintf(stderr,"LIBRAW: Processing file %s\n",fname);
   if( (ret = RawProcessor.open_file(fname)) != LIBRAW_SUCCESS)
   {
      if(verbose) fprintf(stderr,"LIBRAW: Cannot open %s: %s\n",fname,libraw_strerror(ret));
      return 0; // no recycle b/c open file will recycle itself
   }
   if(verbose)
   {
      fprintf(stderr,"LIBRAW: Image size: %dx%d\nRaw size: %dx%d\n",S.width,S.height,S.raw_width,S.raw_height);
      fprintf(stderr,"LIBRAW: Margins: top=%d, left=%d\n",
            S.top_margin,S.left_margin);
   }

   if( (ret = RawProcessor.unpack() ) != LIBRAW_SUCCESS)
   {
      if(verbose) fprintf(stderr,"LIBRAW: Cannot unpack %s: %s\n",fname,libraw_strerror(ret));
      return 0;
   }

   if(verbose)
      fprintf(stderr,"LIBRAW: Unpacked....\n");

   if(!(RawProcessor.imgdata.idata.filters || RawProcessor.imgdata.idata.colors == 1))
   {
      if(verbose) fprintf(stderr,"LIBRAW: Only Bayer-pattern RAW files supported, sorry....\n");
      return 0;
   }






   x->type = 3; //IIO_TYPE_INT16;
   x->pixel_dimension=1;
   x->dimension = 2;
   x->format = 0; //IIO_FORMAT_WHATEVER;
   x->contiguous_data = false;
   //bool caca[3];
   x->sizes[0] = S.raw_width;
   x->sizes[1] = S.raw_height;
   x->data = (void*) malloc(sizeof(char)*2*S.raw_width*S.raw_height);
   memcpy(x->data, RawProcessor.imgdata.rawdata.raw_image, sizeof(char)*2*S.raw_width*S.raw_height);

   if(verbose) fprintf(stderr,"LIBRAW: Sent to IIO\n");
   return 1;
}




// reads the RAW and builds a 4 channel image
int try_reading_file_with_libraw_4channels(const char *fname, struct iio_image *x)
{
   int ret;
   int verbose=0;
   int shot_select = 0;

   LibRaw RawProcessor;

#define S RawProcessor.imgdata.sizes
#define OUT RawProcessor.imgdata.params

   //
   //OUT.shot_select=shot_selected;

   if(verbose) fprintf(stderr,"LIBRAW: Processing file %s\n",fname);
   if( (ret = RawProcessor.open_file(fname)) != LIBRAW_SUCCESS)
   {
      if(verbose) fprintf(stderr,"LIBRAW: Cannot open %s: %s\n",fname,libraw_strerror(ret));
      return 0; // no recycle b/c open file will recycle itself
   }
   if(RawProcessor.imgdata.idata.is_foveon)
   {
      if(verbose) fprintf(stderr,"LIBRAW: Cannot process Foveon image %s\n",fname);
      return 0;
   }
   if(verbose)
   {
      fprintf(stderr,"LIBRAW: Image size: %dx%d\nRaw size: %dx%d\n",S.width,S.height,S.raw_width,S.raw_height);
      fprintf(stderr,"LIBRAW: Margins: top=%d, left=%d\n",
            S.top_margin,S.left_margin);
   }

   if( (ret = RawProcessor.unpack() ) != LIBRAW_SUCCESS)
   {
      if(verbose) fprintf(stderr,"LIBRAW: Cannot unpack %s: %s\n",fname,libraw_strerror(ret));
      return 0;
   }

   if(verbose)
      fprintf(stderr,"LIBRAW: Unpacked....\n");

   if(!(RawProcessor.imgdata.idata.filters || RawProcessor.imgdata.idata.colors == 1))
   {
      if(verbose) fprintf(stderr,"LIBRAW: Only Bayer-pattern RAW files supported, sorry....\n");
      return 0;
   }
   RawProcessor.raw2image();

   RawProcessor.imgdata.idata.colors = 1;
   S.width = S.iwidth;
   S.height = S.iheight;






   x->type = 3; //IIO_TYPE_INT16;
   x->pixel_dimension = 4;
   x->dimension = 2;
   x->format = 0; //IIO_FORMAT_WHATEVER;
   x->contiguous_data = false;
   //bool caca[3];
   x->sizes[0] = S.iwidth/2;
   x->sizes[1] = S.iheight/2;
   x->data = (void*) malloc(sizeof(uint16_t)*S.iwidth/2 * S.iheight/2 * 4);
   uint16_t * odata = (uint16_t*)x->data;
   int ncout = S.iwidth/2;

   int color[] = {0,1,3,2};
   for (int j=0; j<2; j++)
      for (int i=0; i<2; i++)
         for (int rr = 0; rr < S.iheight/2; rr++)
            for (int rc = 0; rc < S.iwidth/2;  rc++) {
               odata[(rr*S.iwidth/2 + rc)*4 +color[i+2*j]] = 
                  RawProcessor.imgdata.image[(2*rr+j)*S.iwidth + 2*rc+i][color[i+2*j]];
            }


   if(verbose) fprintf(stderr,"LIBRAW: Sent to IIO\n");
   return 1;
}

