#!/usr/bin/env python

import time
import sys
sys.path.insert(0, '../Tools')
import leech as model
import tools as tl

import numpy as np
import pylab as pl

class traces:

	def __init__(self, phase_potrait, network, info=None, position=None):
		self.system = phase_potrait
		self.network = network
		self.CYCLES = 10
		self.info = info
		self.initial_condition = self.system.load_initial_condition(pl.rand(), pl.rand(), pl.rand())

		self.fig = pl.figure('Voltage Traces', figsize=(6, 2), facecolor='#EEEEEE')
		self.ax = self.fig.add_subplot(111, frameon=False, yticks=[])

		self.li_b, = self.ax.plot([], [], 'b-', lw=2.)
		self.li_g, = self.ax.plot([], [], 'g-', lw=2.)
		self.li_r, = self.ax.plot([], [], 'r-', lw=2.)
		self.li_y, = self.ax.plot([], [], 'y-', lw=2.)

		self.ax.set_xlabel(r'time (sec.)', fontsize=20)

		self.ax.set_xticklabels(np.arange(0., 1., 0.1), fontsize=15)
		self.ax.set_yticklabels(np.arange(0., 1., 0.1), fontsize=15)
		
		self.ax.set_xlim(0., 100.)
		self.ax.set_ylim(-0.06-0.18, 0.04)

		self.fig.tight_layout()

		self.key_func_dict = dict(u=traces.increase_cycles, i=traces.decrease_cycles)
		self.fig.canvas.mpl_connect('key_press_event', self.on_key)
		self.fig.canvas.mpl_connect('axes_enter_event', self.focus_in)

		if not position == None:
			try:
				self.fig.canvas.manager.window.wm_geometry(position)
			except:
				pass


	def adjust_cycles(self, adjustment):
		self.CYCLES = adjustment.value
		self.compute_traces()

	
	def increase_cycles(self):
		self.CYCLES += 1
		self.compute_traces()
		self.focus_in()

	def decrease_cycles(self):
		self.CYCLES -= 1*(self.CYCLES > 0)
		self.compute_traces()
		self.focus_in()


	def focus_in(self, event=None):
		descriptor = "CYCLES : "+str(self.CYCLES)+" ('u' > 'i')"

		if self.info == None:
			print descriptor

		else:
			self.info.set(descriptor)


	def on_key(self, event):

		try:
			self.key_func_dict[event.key](self)

		except:
			self.key_func_dict[event.key] = lambda x: None


	def compute_traces(self, initial_condition=None):

		if initial_condition == None:
			initial_condition = self.initial_condition

		V_i = model.integrate_four_rk4(
				initial_condition,
				self.network.get_coupling(),
				self.system.dt/float(self.system.stride),
				self.system.N_output(self.CYCLES),
				self.system.stride)

		t = self.system.dt*np.arange(V_i.shape[0])
		ticks = np.asarray(t[::t.size/10], dtype=int)

		self.li_b.set_data(t, V_i[:, 0])
		self.li_g.set_data(t, V_i[:, 1]-0.06)
		self.li_r.set_data(t, V_i[:, 2]-0.12)
		self.li_y.set_data(t, V_i[:, 3]-0.18)
		self.ax.set_xticks(ticks)
		self.ax.set_xticklabels(ticks)
		self.ax.set_xlim(t[0], t[-1])

		self.fig.canvas.draw()
		return t, V_i






	



if __name__ == "__main__":

	import system as sys
	import network as netw
		
	s = sys.system()
	n = netw.network()
	

	tra = traces(s, n)


	pl.show()



