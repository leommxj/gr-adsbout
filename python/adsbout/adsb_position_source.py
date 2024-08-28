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
from .adsb_encoder import gen_position
import sys

class adsb_position_source(gr.sync_block):
    """
    docstring for block adsb_position_source
    """
    def __init__(self,capability,icao,typecode,surveillancestatus,nicsupplementb,altitude,time,latitude,longitude,surface,intermessagegap):
        gr.sync_block.__init__(self,
            name="adsb_position_source",
            in_sig=None,
            out_sig=[numpy.int8])
        self.capability = capability
        self.icao = icao
        self.typecode = typecode
        self.surveillancestatus = surveillancestatus
        self.nicsupplementb = nicsupplementb
        self.altitude = altitude
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.surface = surface
        self.intermessagegap = intermessagegap
        self.data = gen_position(self)

    def work(self, input_items, output_items):
        out = output_items[0]
        try:
            self.data[out.shape[0]]
            out[:] = self.data[:out.shape[0]]
            self.data = self.data[out.shape[0]:]
        except IndexError:
            self.data = self.data + gen_position(self)

        return len(out[:])

