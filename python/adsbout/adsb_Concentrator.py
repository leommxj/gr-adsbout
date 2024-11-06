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

class adsb_Concentrator(gr.basic_block):
    """
    docstring for block adsb_Concentrator
    """
    def __init__(self, gap, ninputs):
        gr.basic_block.__init__(self,
            name="adsb_Concentrator",
            in_sig=[numpy.int8 for i in range(ninputs)],
            out_sig=[numpy.int8])
        self.data = []
        self.gap = gap

    def forecast(self, noutput_items, ninputs):
        ninput_items_required = [noutput_items for _ in range(ninputs)]
        return ninput_items_required

    def general_work(self, input_items, output_items):
        out = output_items[0]
        try:
            self.data[out.shape[0]]
            out[:] = self.data[:out.shape[0]]
            self.data = self.data[out.shape[0]:]
        except IndexError:
            gap_array = [0 for _ in range(self.gap)]
            for i in range(len(input_items)):
                self.data = self.data + list(input_items[i]) + gap_array
                self.consume(i,len(input_items[i]))

        return len(output_items[0])
