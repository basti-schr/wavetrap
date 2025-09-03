#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 gr-wavetrap author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gnuradio import gr
from gnuradio import qtgui
import pmt



class CtlToggleButton(gr.basic_block, qtgui.ToggleButton):
    """
    docstring for block CtlToggleButton
    """
    def __init__(self, callback, lbl,  pressedReleasedDict, initPressed, outputmsgname='value'):
        gr.basic_block.__init__(self,
            name="CtlToggleButton", in_sig=None, out_sig=None)

            
        qtgui.ToggleButton.__init__(self, callback, lbl, pressedReleasedDict, initPressed, outputmsgname)

        self.message_port_register_in(pmt.intern('set_state'))
        self.set_msg_handler(pmt.intern("set_state"), self.msgHandler)

    def msgHandler(self, msg):
        try:
            new_val = pmt.to_python(pmt.cdr(msg))

            if type(new_val) == bool or type(new_val) == int:
                if type(new_val) == bool:
                    super().onToggleClicked(new_val)
                    super().setChecked(new_val)
                else:
                    if new_val == 1:
                        super().onToggleClicked(new_val)
                        super().setChecked(new_val)
                    else:
                        super().onToggleClicked(new_val)
                        super().setChecked(new_val)
            else:
                gr.log.error(
                    "Value received was not an int or a bool: %s" % str(type(new_val)))

        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))

