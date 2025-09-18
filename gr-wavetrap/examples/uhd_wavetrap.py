#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WAVETRAP PUSH-BUTTON RF RECORDER
# Author: Muad'Dib
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio import wavetrap
import gnuradio.wavetrap as wavetrap
import os
import sip
import threading
import uhd_wavetrap_epy_block_0 as epy_block_0  # embedded python block



class uhd_wavetrap(gr.top_block, Qt.QWidget):

    def __init__(self, rf_freq=1575.42e6, rf_gain=70, samp_rate=4e6):
        gr.top_block.__init__(self, "WAVETRAP PUSH-BUTTON RF RECORDER", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("WAVETRAP PUSH-BUTTON RF RECORDER")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "uhd_wavetrap")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.rootdir = rootdir = str(os.path.expanduser("~")+"/")
        self.record_file_path = record_file_path = "data/"
        self.note = note = 'RECORDING_NOTE'
        self.gui_samp_rate = gui_samp_rate = samp_rate
        self.freq = freq = 1575.42e6
        self.duration = duration = 1
        self.timestamp = timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        self.samples = samples = int(duration * gui_samp_rate)
        self.rec_button = rec_button = 0
        self.gui_gain = gui_gain = rf_gain
        self.filename = filename = rootdir+record_file_path+note+"_"+str(int(freq))+"Hz_"+str(int(gui_samp_rate))+"sps_"

        ##################################################
        # Blocks
        ##################################################

        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'RF Settings')
        self.top_grid_layout.addWidget(self.tabs, 0, 0, 7, 4)
        for r in range(0, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        if bool == bool:
        	self._rec_button_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif bool == str:
        	self._rec_button_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._rec_button_choices = {'Pressed': 1, 'Released': 0}

        _rec_button_ctl_toggle_btn = wavetrap.CtlToggleButton(self.set_rec_button, 'rec_button', self._rec_button_choices, False,"'value'".replace("'",""))
        _rec_button_ctl_toggle_btn.setColors("default","default","default","default")
        self.rec_button = _rec_button_ctl_toggle_btn

        self.tabs_grid_layout_0.addWidget(_rec_button_ctl_toggle_btn, 1, 3, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._gui_samp_rate_range = qtgui.Range(200e3, 56e6, 1e6, samp_rate, 10)
        self._gui_samp_rate_win = qtgui.RangeWidget(self._gui_samp_rate_range, self.set_gui_samp_rate, "Sample Rate", "eng", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gui_samp_rate_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._gui_gain_range = qtgui.Range(0, 76, 1, rf_gain, 200)
        self._gui_gain_win = qtgui.RangeWidget(self._gui_gain_range, self.set_gui_gain, "RX Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gui_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._freq_range = qtgui.Range(50e6, 6e9, 10e3, 1575.42e6, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "Center Frequency", "eng_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._freq_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.wavetrap_head_w_rst_0 = wavetrap.head_w_rst(gr.sizeof_gr_complex*2, samples)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('internal', 0)
        self.uhd_usrp_source_0.set_samp_rate(gui_samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(gui_samp_rate, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(gui_gain, 0)

        self.uhd_usrp_source_0.set_center_freq(0, 1)
        self.uhd_usrp_source_0.set_antenna("RX2", 1)
        self.uhd_usrp_source_0.set_bandwidth(gui_samp_rate, 1)
        self.uhd_usrp_source_0.set_rx_agc(False, 1)
        self.uhd_usrp_source_0.set_gain(gui_gain, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            gui_samp_rate, #bw
            "RF 1", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/20)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_0_0_win, 2, 2, 2, 2)
        for r in range(2, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            gui_samp_rate, #bw
            "RF 0", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/20)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_0_win, 2, 0, 2, 2)
        for r in range(2, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("RED=RECORDING", "red", "green", False, 40, 2, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.tabs_grid_layout_0.addWidget(self._qtgui_ledindicator_0_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._note_tool_bar = Qt.QToolBar(self)
        self._note_tool_bar.addWidget(Qt.QLabel("RECORDING NOTE (press enter to update)" + ": "))
        self._note_line_edit = Qt.QLineEdit(str(self.note))
        self._note_tool_bar.addWidget(self._note_line_edit)
        self._note_line_edit.editingFinished.connect(
            lambda: self.set_note(str(str(self._note_line_edit.text()))))
        self.tabs_grid_layout_0.addWidget(self._note_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.blk()
        self._duration_tool_bar = Qt.QToolBar(self)
        self._duration_tool_bar.addWidget(Qt.QLabel("Duration [s]" + ": "))
        self._duration_line_edit = Qt.QLineEdit(str(self.duration))
        self._duration_tool_bar.addWidget(self._duration_line_edit)
        self._duration_line_edit.editingFinished.connect(
            lambda: self.set_duration(eng_notation.str_to_num(str(self._duration_line_edit.text()))))
        self.tabs_grid_layout_0.addWidget(self._duration_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*1, 2)
        self.blocks_var_to_msg_0 = blocks.var_to_msg_pair('freq')
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 2)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF1.raw" if rec_button == 1 else "/dev/null", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF0.raw" if rec_button == 1 else "/dev/null", False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_var_to_msg_0, 'msgout'), (self.qtgui_sink_x_0, 'freq'))
        self.msg_connect((self.blocks_var_to_msg_0, 'msgout'), (self.qtgui_sink_x_0_0, 'freq'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.rec_button, 'set_state'))
        self.msg_connect((self.rec_button, 'state'), (self.qtgui_ledindicator_0, 'state'))
        self.msg_connect((self.rec_button, 'state'), (self.wavetrap_head_w_rst_0, 'reset'))
        self.msg_connect((self.wavetrap_head_w_rst_0, 'status'), (self.epy_block_0, 'msg_in'))
        self.connect((self.blocks_streams_to_vector_0, 0), (self.wavetrap_head_w_rst_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_file_sink_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_streams_to_vector_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_streams_to_vector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.wavetrap_head_w_rst_0, 0), (self.blocks_vector_to_streams_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "uhd_wavetrap")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_gui_gain(self.rf_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_gui_samp_rate(self.samp_rate)

    def get_rootdir(self):
        return self.rootdir

    def set_rootdir(self, rootdir):
        self.rootdir = rootdir
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_")

    def get_record_file_path(self):
        return self.record_file_path

    def set_record_file_path(self, record_file_path):
        self.record_file_path = record_file_path
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_")

    def get_note(self):
        return self.note

    def set_note(self, note):
        self.note = note
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_")
        Qt.QMetaObject.invokeMethod(self._note_line_edit, "setText", Qt.Q_ARG("QString", str(self.note)))

    def get_gui_samp_rate(self):
        return self.gui_samp_rate

    def set_gui_samp_rate(self, gui_samp_rate):
        self.gui_samp_rate = gui_samp_rate
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_")
        self.set_samples(int(self.duration * self.gui_samp_rate))
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.gui_samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.gui_samp_rate, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.gui_samp_rate, 1)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_")
        self.blocks_var_to_msg_0.variable_changed(self.freq)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration
        Qt.QMetaObject.invokeMethod(self._duration_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.duration)))
        self.set_samples(int(self.duration * self.gui_samp_rate))

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_samples(self):
        return self.samples

    def set_samples(self, samples):
        self.samples = samples
        self.wavetrap_head_w_rst_0.set_length(self.samples)

    def get_rec_button(self):
        return self.rec_button

    def set_rec_button(self, rec_button):
        self.rec_button = rec_button
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF0.raw" if self.rec_button == 1 else "/dev/null")
        self.blocks_file_sink_0_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF1.raw" if self.rec_button == 1 else "/dev/null")

    def get_gui_gain(self):
        return self.gui_gain

    def set_gui_gain(self, gui_gain):
        self.gui_gain = gui_gain
        self.uhd_usrp_source_0.set_gain(self.gui_gain, 0)
        self.uhd_usrp_source_0.set_gain(self.gui_gain, 1)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF0.raw" if self.rec_button == 1 else "/dev/null")
        self.blocks_file_sink_0_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+"_RF1.raw" if self.rec_button == 1 else "/dev/null")



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--rf-freq", dest="rf_freq", type=eng_float, default=eng_notation.num_to_str(float(1575.42e6)),
        help="Set RF FREQUENCY [default=%(default)r]")
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(70)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(4e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    return parser


def main(top_block_cls=uhd_wavetrap, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate)

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
