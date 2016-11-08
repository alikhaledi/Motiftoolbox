#!/usr/bin/env python

import sys
sys.path.insert(0, '../Tools')
import window as win
import tools as tl

import numpy as np
import pylab as pl


class info(win.window):

	title = 'Info'
	figsize = (3, 2)

	def __init__(self, position=None):
		win.window.__init__(self, position)
		self.description = self.fig.text(0.1, 0.1, 'here comes the description')

	
	def set(self, text):
		self.description.set_text(text)
		self.fig.canvas.draw()




if __name__ == "__main__":

	net = info(position="+200+0")
	pl.show()




