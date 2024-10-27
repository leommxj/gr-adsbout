#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Gabe.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from .adsb_encoder import gen_velocity
import sys

class adsb_velocity_source(gr.sync_block):
    """
    docstring for block adsb_velocity_source
    """
    def __init__(self,icao,groundspeed,heading,vertical_rate):
        gr.sync_block.__init__(self,
            name="adsb_velocity_source",
            in_sig=None,
            out_sig=([numpy.int8]))
        state = {
            "groundspeed": groundspeed,
            "heading": heading,
            "vertical_rate": vertical_rate
            }
        self.icao = icao
        self.state = state
        self.data = gen_velocity(self)


    def work(self, input_items, output_items):
        out = output_items[0]
        try:
            self.data[out.shape[0]]
            out[:] = self.data[:out.shape[0]]
            self.data = self.data[out.shape[0]:]
        except IndexError:
            self.data = self.data + gen_velocity(self)

        return len(out[:])
