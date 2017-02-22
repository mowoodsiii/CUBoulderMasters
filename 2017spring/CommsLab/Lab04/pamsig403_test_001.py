#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: PAM Signal Test 1
# Author: Maurice Woods
# Description: Lab 04
# Generated: Tue Feb 21 18:01:41 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
from scipy.signal import butter
import sip
import sys
from gnuradio import qtgui


class pamsig403_test_001(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PAM Signal Test 1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PAM Signal Test 1")
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

        self.settings = Qt.QSettings("GNU Radio", "pamsig403_test_001")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.fL = fL = 100
        self.N = N = 5

        ##################################################
        # Blocks
        ##################################################
        self._fL_range = Range(20, 1000, 1, 100, 200)
        self._fL_win = RangeWidget(self._fL_range, self.set_fL, 'Initial Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fL_win, 1,0,1,1)
        self._N_range = Range(1, 10, 1, 5, 200)
        self._N_win = RangeWidget(self._N_range, self.set_N, 'N', "counter_slider", float)
        self.top_grid_layout.addWidget(self._N_win, 0,0,1,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	8192, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2,0,1,1)
        self.iir_filter_xxx_0 = filter.iir_filter_ffd((butter(N,2*fL/float(samp_rate))[0]), (butter(N,2*fL/float(samp_rate))[1]), False)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/maurice/Documents/Git/CUBoulderMasters/2017spring/CommsLab/Lab04/pamsig403.wav', True)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('pamsig403_rcvr.wav', 1, samp_rate, 16)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.8, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pamsig403_test_001")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.iir_filter_xxx_0.set_taps((butter(self.N,2*self.fL/float(self.samp_rate))[0]), (butter(self.N,2*self.fL/float(self.samp_rate))[1]))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_fL(self):
        return self.fL

    def set_fL(self, fL):
        self.fL = fL
        self.iir_filter_xxx_0.set_taps((butter(self.N,2*self.fL/float(self.samp_rate))[0]), (butter(self.N,2*self.fL/float(self.samp_rate))[1]))

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.iir_filter_xxx_0.set_taps((butter(self.N,2*self.fL/float(self.samp_rate))[0]), (butter(self.N,2*self.fL/float(self.samp_rate))[1]))


def main(top_block_cls=pamsig403_test_001, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
