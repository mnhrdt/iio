#!/usr/bin/env python3

import iio

d = iio.read('testimg.tif')
print(d.shape)
print(d[:,:,0])
iio.write('kk2.tif',d+1000)

