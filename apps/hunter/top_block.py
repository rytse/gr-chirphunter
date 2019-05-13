#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: top_block
# GNU Radio version: 3.8tech-preview-362-g72aa97da

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import chirphunter
import numpy as np
from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "top_block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("top_block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 50e6
        self.decim = decim = 500
        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, samp_rate / decim, samp_rate / decim / 2,0.1e3, firdes.WIN_HAMMING, 6.76)
        self.fn = fn = '/media/rytse/Seagate Backup Plus Drive/Flash Drive/cubesat/new sh recordings/will not copy/IQREC-02-03-19-14h02m40s879.iq'
        self.f0 = f0 = 6043612
        self.chirp_rate = chirp_rate = 9.9951e4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_f(
            8192, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.fir_filter_xxx_1 = filter.fir_filter_ccc(decim, lpf_taps)
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.chirphunter_chirpgen_1 = chirphunter.chirpgen(f0  * 1.005 * 1.5 * 2, chirp_rate, samp_rate)
        self.chirphunter_chirpgen_0 = chirphunter.chirpgen(f0 , chirp_rate, samp_rate)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(100000000)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/rytse/Documents/cubesat/gr-chirphunter/data/out/sim_real_raw.out', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                6e6,
                7e6,
                0.1e6,
                firdes.WIN_HAMMING,
                6.76))

        tmp = firdes.band_pass(
                1,
                samp_rate,
                6e6,
                7e6,
                0.1e6,
                firdes.WIN_HAMMING,
                6.76)
        print(f'\n\n\n\nBPF LENGTH: {len(tmp)}\n\n\n\n')



        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.chirphunter_chirpgen_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.chirphunter_chirpgen_1, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_file_sink_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 6e6, 7e6, 0.1e6, firdes.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.fir_filter_xxx_1.set_taps(self.lpf_taps)

    def get_fn(self):
        return self.fn

    def set_fn(self, fn):
        self.fn = fn

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0

    def get_chirp_rate(self):
        return self.chirp_rate

    def set_chirp_rate(self, chirp_rate):
        self.chirp_rate = chirp_rate



def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
