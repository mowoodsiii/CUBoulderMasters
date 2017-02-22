#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Sampling Theorem
# Author: Maurice Woods
# Description: Lab 04
# Generated: Tue Feb 21 17:30:58 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy as np
import ptfun as pt
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Sampling Theorem")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Sampling Theorem")
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
        self.Fs3 = Fs3 = 64000
        self.Fs2 = Fs2 = 4000
        self.waveform = waveform = 102
        self.k = k = 5
        self.fc = fc = Fs2
        self.f0 = f0 = 200
        self.Usamp = Usamp = 16
        self.Fs4 = Fs4 = Fs3
        self.Fs1 = Fs1 = 32000
        self.Dsamp = Dsamp = 8

        ##################################################
        # Blocks
        ##################################################
        self._waveform_options = (102, 103, 104, )
        self._waveform_labels = ('Cosine', 'Rectangular', 'Triangular', )
        self._waveform_group_box = Qt.QGroupBox("waveform")
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
        self.top_grid_layout.addWidget(self._waveform_group_box, 0,2,1,2)
        self._fc_range = Range(-16000, 16000, 1, Fs2, 200)
        self._fc_win = RangeWidget(self._fc_range, self.set_fc, 'Center Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fc_win, 0,0,1,2)
        self._f0_range = Range(-5000, 5000, 1, 200, 200)
        self._f0_win = RangeWidget(self._f0_range, self.set_f0, 'Initial Frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._f0_win, 1,0,1,2)
        self._Fs4_range = Range(Fs1, Fs3*10, 0.01, Fs3, 200)
        self._Fs4_win = RangeWidget(self._Fs4_range, self.set_Fs4, 'Fs4', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Fs4_win, 1,2,1,2)
        self.qtgui_time_sink_x_3 = qtgui.time_sink_f(
        	1024, #size
        	Fs3, #samp_rate
        	"Reconstructed Waveform (at Fs3)", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_3.enable_tags(-1, True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_3.enable_autoscale(True)
        self.qtgui_time_sink_x_3.enable_grid(True)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_3.disable_legend()

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
                self.qtgui_time_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_3_win, 3,2,1,2)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
        	1024, #size
        	Fs3, #samp_rate
        	"DT Waveform (at Fs3)", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(-1, True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(True)
        self.qtgui_time_sink_x_2.enable_grid(True)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_2.disable_legend()

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
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_win, 3,0,1,2)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	1024, #size
        	Fs2, #samp_rate
        	"DT Waveform (at Fs2)", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(True)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_1.disable_legend()

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
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 2,2,1,2)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	Fs1, #samp_rate
        	"Original Waveform (at Fs1)", #name
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2,0,1,2)
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_fff(1, (2*np.cos(2*np.pi*fc/Fs3*np.arange(-2*k*Usamp,2*k*Usamp))*pt.pampt(Usamp,'sinc',[k,2.6,Fs3])))
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(Usamp, (1, ))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(Dsamp, (1, ))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, Fs1,True)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(Fs4, waveform, f0, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(Fs1, waveform, f0, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.qtgui_time_sink_x_3, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_Fs3(self):
        return self.Fs3

    def set_Fs3(self, Fs3):
        self.Fs3 = Fs3
        self.set_Fs4(self.Fs3)
        self.qtgui_time_sink_x_3.set_samp_rate(self.Fs3)
        self.qtgui_time_sink_x_2.set_samp_rate(self.Fs3)
        self.interp_fir_filter_xxx_0_0.set_taps((2*np.cos(2*np.pi*self.fc/self.Fs3*np.arange(-2*self.k*self.Usamp,2*self.k*self.Usamp))*pt.pampt(self.Usamp,'sinc',[self.k,2.6,self.Fs3])))

    def get_Fs2(self):
        return self.Fs2

    def set_Fs2(self, Fs2):
        self.Fs2 = Fs2
        self.set_fc(self.Fs2)
        self.qtgui_time_sink_x_1.set_samp_rate(self.Fs2)

    def get_waveform(self):
        return self.waveform

    def set_waveform(self, waveform):
        self.waveform = waveform
        self._waveform_callback(self.waveform)
        self.analog_sig_source_x_0_0.set_waveform(self.waveform)
        self.analog_sig_source_x_0.set_waveform(self.waveform)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k
        self.interp_fir_filter_xxx_0_0.set_taps((2*np.cos(2*np.pi*self.fc/self.Fs3*np.arange(-2*self.k*self.Usamp,2*self.k*self.Usamp))*pt.pampt(self.Usamp,'sinc',[self.k,2.6,self.Fs3])))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.interp_fir_filter_xxx_0_0.set_taps((2*np.cos(2*np.pi*self.fc/self.Fs3*np.arange(-2*self.k*self.Usamp,2*self.k*self.Usamp))*pt.pampt(self.Usamp,'sinc',[self.k,2.6,self.Fs3])))

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.analog_sig_source_x_0_0.set_frequency(self.f0)
        self.analog_sig_source_x_0.set_frequency(self.f0)

    def get_Usamp(self):
        return self.Usamp

    def set_Usamp(self, Usamp):
        self.Usamp = Usamp
        self.interp_fir_filter_xxx_0_0.set_taps((2*np.cos(2*np.pi*self.fc/self.Fs3*np.arange(-2*self.k*self.Usamp,2*self.k*self.Usamp))*pt.pampt(self.Usamp,'sinc',[self.k,2.6,self.Fs3])))

    def get_Fs4(self):
        return self.Fs4

    def set_Fs4(self, Fs4):
        self.Fs4 = Fs4
        self.analog_sig_source_x_0_0.set_sampling_freq(self.Fs4)

    def get_Fs1(self):
        return self.Fs1

    def set_Fs1(self, Fs1):
        self.Fs1 = Fs1
        self.qtgui_time_sink_x_0.set_samp_rate(self.Fs1)
        self.blocks_throttle_0.set_sample_rate(self.Fs1)
        self.analog_sig_source_x_0.set_sampling_freq(self.Fs1)

    def get_Dsamp(self):
        return self.Dsamp

    def set_Dsamp(self, Dsamp):
        self.Dsamp = Dsamp


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
