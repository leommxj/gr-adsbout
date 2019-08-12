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
from adsb_encoder import singlePlane
import sys

class ADSB_SOURCE(gr.sync_block):
    """
    docstring for block ADSB_SOURCE
    """
    def __init__(self,capability,icao,typecode,surveillancestatus,nicsupplementb,altitude,time,latitude,longitude,surface,repeats,intermessagegap):
        gr.sync_block.__init__(self,
            name="ADSB_SOURCE",
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
        self.repeats = repeats
        self.intermessagegap = intermessagegap
        self.data = singlePlane(self)

    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        try:
            self.data[out.shape[0]]
            #sys.stderr.write('dat:%s\n' % str(dat.shape))
            #sys.stderr.write('out:%s\n' % str(out.shape))
            out[:] = self.data[:out.shape[0]]
            self.data = self.data[out.shape[0]:]
        except IndexError:
            self.data = self.data + singlePlane(self)

        return len(out[:])

