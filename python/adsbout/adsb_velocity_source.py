import numpy
from gnuradio import gr
from .adsb_encoder import gen_velocity

class adsb_velocity_source(gr.sync_block):
    """
    """
    #TODO the direction may have some issue
    def __init__(self,icao,subtype,ic,nac,w2e,n2s,vrsrc,vr,dif):
        gr.sync_block.__init__(self,
            name="adsb_velocity_source",
            in_sig=None,
            out_sig=[numpy.int8])
        self.icao = icao
        self.st = subtype
        self.ic = ic
        self.nac = nac
        self.s_we = 0 if w2e<0 else 1
        self.v_we = abs(w2e)+1
        self.s_ns = 0 if n2s<0 else 1
        self.v_ns = abs(n2s)+1
        self.vrsrc = vrsrc
        self.s_vr = 0 if vr<0 else 1
        self.vr = int(abs(vr)/64)+1
        self.s_dif = 0 if dif<0 else 1
        self.dif = abs(dif)

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

