#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 leommxj.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
from .adsb_encoder import gen_ident

class adsb_ident_source(gr.sync_block):
    """
    docstring for block adsb_ident_source
    """
    def __init__(self, ec, icao, callsign):
        gr.sync_block.__init__(self,
            name="adsb_ident_source",
            in_sig=None,
            out_sig=[numpy.int8])
        self.ec = ec
        self.icao = icao
        self.callsign = callsign
        self.data = gen_ident(self)


    def work(self, input_items, output_items):
        out = output_items[0]
        try:
            self.data[out.shape[0]]
            out[:] = self.data[:out.shape[0]]
            self.data = self.data[out.shape[0]:]
        except IndexError:
            self.data = self.data + gen_ident(self)
        return len(output_items[0])

