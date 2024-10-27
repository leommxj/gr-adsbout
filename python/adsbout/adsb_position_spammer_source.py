#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gabe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from .adsb_encoder import gen_position
import sys

class adsb_position_spammer_source(gr.sync_block):
    """
    docstring for block adsb_position_spammer_source
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
            self.icao = numpy.random.randint(16777215)
            self.altitude = numpy.random.randint(8000,40000)
            self.latitude = numpy.random.uniform(-90,90)
            self.longitde = numpy.random.uniform(-180,180)
            self.data = self.data + gen_position(self)

        return len(out[:])
