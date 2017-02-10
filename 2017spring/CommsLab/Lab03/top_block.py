#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lab 03
# Author: Maurice Woods
# Generated: Fri Feb 10 00:37:40 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 03")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 03")
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
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.f0 = f0 = 1000

        ##################################################
        # Blocks
        ##################################################
        self._f0_range = Range(-5000, 5000, 1, 1000, 200)
        self._f0_win = RangeWidget(self._f0_range, self.set_f0, "f0", "counter_slider", float)
        self.top_grid_layout.addWidget(self._f0_win, 0,0,1,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
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

        for i in xrange(3):
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1,0,1,1)
        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_magphase_to_complex_0_1 = blocks.magphase_to_complex(1)
        self.blocks_magphase_to_complex_0_0 = blocks.magphase_to_complex(1)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.blocks_complex_to_magphase_0_1 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_float_0_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_0_1 = blocks.add_const_vff((2*120*3.14159/180, ))
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vff((120*3.14159/180, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0, ))
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f0, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f0, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f0, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_complex_to_magphase_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_complex_to_magphase_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_magphase_to_complex_0, 1))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_magphase_to_complex_0_0, 1))
        self.connect((self.blocks_add_const_vxx_0_1, 0), (self.blocks_magphase_to_complex_0_1, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 2))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_null_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.blocks_magphase_to_complex_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 1), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.blocks_magphase_to_complex_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_1, 1), (self.blocks_add_const_vxx_0_1, 0))
        self.connect((self.blocks_complex_to_magphase_0_1, 0), (self.blocks_magphase_to_complex_0_1, 0))
        self.connect((self.blocks_magphase_to_complex_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_magphase_to_complex_0_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_magphase_to_complex_0_1, 0), (self.blocks_complex_to_float_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_throttle_0_1, 0), (self.qtgui_time_sink_x_0, 2))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.analog_sig_source_x_0_1.set_frequency(self.f0)
        self.analog_sig_source_x_0_0.set_frequency(self.f0)
        self.analog_sig_source_x_0.set_frequency(self.f0)


def main(top_block_cls=top_block, options=None):

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
