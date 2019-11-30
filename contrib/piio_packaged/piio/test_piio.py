#!/usr/bin/env python3
import piio

d = piio.read('testimg.tif')
print(d.shape)
print(d[:,:,0] )
piio.write('testimg2.png',d)

