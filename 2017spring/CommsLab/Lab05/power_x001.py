#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Power/PSD Example 1
# Author: Maurice Woods
# Description: Lab 05
# Generated: Thu Mar  9 02:34:54 2017
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
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ptfun
import sip
import sys
from gnuradio import qtgui


class power_x001(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Power/PSD Example 1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Power/PSD Example 1")
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

        self.settings = Qt.QSettings("GNU Radio", "power_x001")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.waveform = waveform = 'rect'
        self.Fs = Fs = 512000
        self.FB = FB = 32000
        self.sps = sps = Fs/FB
        self.ptype = ptype = waveform
        self.pparms = pparms = [10,0.2]
        self.fL_div_by_FB = fL_div_by_FB = 2
        self.band = band = 1

        ##################################################
        # Blocks
        ##################################################
        self._fL_div_by_FB_range = Range(0, 8, 0.5, 2, 200)
        self._fL_div_by_FB_win = RangeWidget(self._fL_div_by_FB_range, self.set_fL_div_by_FB, 'fL/FB', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fL_div_by_FB_win, 0,0,1,1)
        self._band_range = Range(0, 2, 0.25, 1, 200)
        self._band_win = RangeWidget(self._band_range, self.set_band, 'Bandwidth fL (FB*2)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._band_win, 1,0,1,1)
        self._waveform_options = ('rect', 'tri', 'sinc', 'rcf', 'man', )
        self._waveform_labels = ('Rectangular', 'Triangular', 'Sinc', 'RCf', 'Manchester', )
        self._waveform_group_box = Qt.QGroupBox('Waveform')
        self._waveform_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._waveform_button_group = variable_chooser_button_group()
        self._waveform_group_box.setLayout(self._waveform_box)
        for i, label in enumerate(self._waveform_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._waveform_box.addWidget(radio_button)
        	self._waveform_button_group.addButton(radio_button, i)
        self._waveform_callback = lambda i: Qt.QMetaObject.invokeMethod(self._waveform_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._waveform_options.index(i)))
        self._waveform_callback(self.waveform)
        self._waveform_button_group.buttonClicked[int].connect(
        	lambda i: self.set_waveform(self._waveform_options[i]))
        self.top_grid_layout.addWidget(self._waveform_group_box, 0,1,2,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	Fs, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
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
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	Fs, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2,1,1,1)
        self.low_pass_filter_0_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, Fs, band*FB, 100, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0 = filter.fir_filter_fff(64, firdes.low_pass(
        	1, Fs, 10, 10, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_fff(64, firdes.low_pass(
        	1, Fs, 10, 10, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, Fs, fL_div_by_FB*FB, 3200, firdes.WIN_HAMMING, 6.76))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(16, (ptfun.pampt(sps,ptype,pparms)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_f(22, True, 0, 1)
        self.contribution = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.contribution.set_update_time(0.10)
        self.contribution.set_title("Bandwidth Contribution")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['%', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.contribution.set_min(i, 0)
            self.contribution.set_max(i, 100)
            self.contribution.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.contribution.set_label(i, "Data {0}".format(i))
            else:
                self.contribution.set_label(i, labels[i])
            self.contribution.set_unit(i, units[i])
            self.contribution.set_factor(i, factor[i])

        self.contribution.enable_autoscale(False)
        self._contribution_win = sip.wrapinstance(self.contribution.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._contribution_win, 4,0,1,2)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, FB,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((100, ))
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.avg_pwr = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.avg_pwr.set_update_time(0.10)
        self.avg_pwr.set_title("Avg. Power")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.avg_pwr.set_min(i, 0)
            self.avg_pwr.set_max(i, 2)
            self.avg_pwr.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.avg_pwr.set_label(i, "Data {0}".format(i))
            else:
                self.avg_pwr.set_label(i, labels[i])
            self.avg_pwr.set_unit(i, units[i])
            self.avg_pwr.set_factor(i, factor[i])

        self.avg_pwr.enable_autoscale(False)
        self._avg_pwr_win = sip.wrapinstance(self.avg_pwr.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._avg_pwr_win, 3,0,1,2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.contribution, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.avg_pwr, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.blocks_multiply_xx_0_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "power_x001")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_waveform(self):
        return self.waveform

    def set_waveform(self, waveform):
        self.waveform = waveform
        self.set_ptype(self.waveform)
        self._waveform_callback(self.waveform)

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs
        self.set_sps(self.Fs/self.FB)
        self.qtgui_time_sink_x_0.set_samp_rate(self.Fs)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.Fs)
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.Fs, self.band*self.FB, 100, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.Fs, 10, 10, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.Fs, 10, 10, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.Fs, self.fL_div_by_FB*self.FB, 3200, firdes.WIN_HAMMING, 6.76))

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB
        self.set_sps(self.Fs/self.FB)
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.Fs, self.band*self.FB, 100, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.Fs, self.fL_div_by_FB*self.FB, 3200, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.FB)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.ptype,self.pparms)))

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.ptype,self.pparms)))

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.ptype,self.pparms)))

    def get_fL_div_by_FB(self):
        return self.fL_div_by_FB

    def set_fL_div_by_FB(self, fL_div_by_FB):
        self.fL_div_by_FB = fL_div_by_FB
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.Fs, self.fL_div_by_FB*self.FB, 3200, firdes.WIN_HAMMING, 6.76))

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.Fs, self.band*self.FB, 100, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=power_x001, options=None):

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
