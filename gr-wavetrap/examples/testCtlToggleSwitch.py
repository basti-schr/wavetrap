#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test CtlToggleSwitch
# Author: Sebastian Schröder
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks, gr
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import wavetrap
import threading



class testCtlToggleSwitch(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test CtlToggleSwitch", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test CtlToggleSwitch")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "testCtlToggleSwitch")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.wavetrap_CtlToggleButton_0 = wavetrap_CtlToggleButton_0 = 0
        self.variable_qtgui_toggle_switch_0 = variable_qtgui_toggle_switch_0 = 0

        ##################################################
        # Blocks
        ##################################################

        if int == bool:
        	self._wavetrap_CtlToggleButton_0_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif int == str:
        	self._wavetrap_CtlToggleButton_0_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._wavetrap_CtlToggleButton_0_choices = {'Pressed': 1, 'Released': 0}

        _wavetrap_CtlToggleButton_0_ctl_toggle_btn = wavetrap.CtlToggleButton(self.set_wavetrap_CtlToggleButton_0, 'wavetrap_CtlToggleButton_0', self._wavetrap_CtlToggleButton_0_choices, False,"'value'".replace("'",""))
        _wavetrap_CtlToggleButton_0_ctl_toggle_btn.setColors("default","default","default","default")
        self.wavetrap_CtlToggleButton_0 = _wavetrap_CtlToggleButton_0_ctl_toggle_btn

        self.top_layout.addWidget(_wavetrap_CtlToggleButton_0_ctl_toggle_btn)
        self._variable_qtgui_toggle_switch_0_choices = {'Pressed': 1, 'Released': 0}

        _variable_qtgui_toggle_switch_0_toggle_switch = qtgui.GrToggleSwitch(self.set_variable_qtgui_toggle_switch_0, '', self._variable_qtgui_toggle_switch_0_choices, False, "green", "gray", 4, 50, 1, 1, self, 'value')
        self.variable_qtgui_toggle_switch_0 = _variable_qtgui_toggle_switch_0_toggle_switch

        self.top_layout.addWidget(_variable_qtgui_toggle_switch_0_toggle_switch)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("", "green", "red", False, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_layout.addWidget(self._qtgui_ledindicator_0_win)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.variable_qtgui_toggle_switch_0, 'state'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.variable_qtgui_toggle_switch_0, 'state'), (self.wavetrap_CtlToggleButton_0, 'set_state'))
        self.msg_connect((self.wavetrap_CtlToggleButton_0, 'state'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.wavetrap_CtlToggleButton_0, 'state'), (self.qtgui_ledindicator_0, 'state'))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "testCtlToggleSwitch")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wavetrap_CtlToggleButton_0(self):
        return self.wavetrap_CtlToggleButton_0

    def set_wavetrap_CtlToggleButton_0(self, wavetrap_CtlToggleButton_0):
        self.wavetrap_CtlToggleButton_0 = wavetrap_CtlToggleButton_0

    def get_variable_qtgui_toggle_switch_0(self):
        return self.variable_qtgui_toggle_switch_0

    def set_variable_qtgui_toggle_switch_0(self, variable_qtgui_toggle_switch_0):
        self.variable_qtgui_toggle_switch_0 = variable_qtgui_toggle_switch_0




def main(top_block_cls=testCtlToggleSwitch, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
