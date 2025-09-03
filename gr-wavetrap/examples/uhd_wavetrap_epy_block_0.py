"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time
from datetime import datetime

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Control logic',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        self.message_port_register_out(pmt.intern('msg_out'))
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
 
    def handle_msg(self, msg):
        val =  pmt.to_python(msg)
        print(val)
        if val=='FINISHED':
            self.message_port_pub(pmt.intern("msg_out"), pmt.cons(pmt.intern("value"), pmt.from_bool(False)))
        elif val=='IN PROGRESS':
            pass
        elif val=='RESET':
            pass
        




