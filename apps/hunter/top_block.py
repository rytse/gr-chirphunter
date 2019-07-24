#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: top_block
# GNU Radio version: 3.8.0.0-rc2

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

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
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
        self.lpf = lpf = firdes.low_pass(1.0, samp_rate, 50e6 / 100,50e3, firdes.WIN_HAMMING, 6.76)
        self.f0 = f0 = 6043612
        self.decim = decim = 500
        self.chirp_rate = chirp_rate = 9.9951e4

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=100,
                taps=lpf,
                fractional_bw=None)
        self.chirphunter_hough_0 = chirphunter.hough(4096, 4096, 0, np.pi / 2, 5, 5, 5)
        self.chirphunter_chirpgen_1 = chirphunter.chirpgen(f0 +29.7e6 + 49.3e6, chirp_rate, samp_rate)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 5000000)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.chirphunter_chirpgen_1, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.chirphunter_chirpgen_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.chirphunter_hough_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_lpf(self):
        return self.lpf

    def set_lpf(self, lpf):
        self.lpf = lpf
        self.rational_resampler_xxx_0.set_taps(self.lpf)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

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

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
