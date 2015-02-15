#!/usr/bin/env python


import system as sys
import network3N as netw
import traces as tra
import info as nf
import torus as tor
import pylab as pl

pos_info = '+0+600'
pos_tra = '+300+600'
pos_net = '+300+0'
pos_sys = '+0+0'
pos_torus = '+800+0'

info = nf.info(position=pos_info)
net = netw.network(g_inh=0.015, info=info, position=pos_net)
system = sys.system(info=info, position=pos_sys, network=net)
traces = tra.traces(system, net, info=info, position=pos_tra)
torus = tor.torus(system, net, traces, info=info, position=pos_torus)

net.system = system
system.traces = traces

if pl.get_backend() == 'TkAgg':
	system.fig.tight_layout()
	traces.fig.tight_layout()
	torus.fig.tight_layout()

pl.show()
