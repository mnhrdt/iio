#!/usr/bin/env python3

import numpy
import tkinter
import iio

x = iio.read("x.png").squeeze()
x = numpy.uint8(x)
x_bytes = x.data.tobytes()

WIDTH  = x.shape[1]
HEIGHT = x.shape[0]

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()
xdata = b"P5 %d %d 255\n" % (WIDTH, HEIGHT) + x_bytes + x_bytes + x_bytes
image = tkinter.PhotoImage(data=xdata, format="PPM")
canvas.create_image(1, 1, image=image, anchor=tkinter.NW)

posx = 100
posy = 100

def helloworld(x):
	global posx
	global posy
	image.put("#ff0000", (posx,posy))
	posx = posx + 1
	print("hello world! \"%s\"" % x)

def do_quit(x):
	print("do_quit \"%s\"" % x)
	window.quit()

canvas.focus_set()
canvas.bind("<h>", helloworld)
canvas.bind("<q>", do_quit)

window.mainloop()
