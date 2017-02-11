#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lab 03
# Author: Maurice Woods
# Generated: Fri Feb 10 21:12:24 2017
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
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy as np
import ptfun  # embedded python module
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
        self.sps = sps = 5
        self.samp_rate = samp_rate = 10000
        self.ptype = ptype = 'tri'
        self.k = k = 5
        self.beta = beta = 2.5
        self.PTYPE = PTYPE = 'sinc'

        ##################################################
        # Blocks
        ##################################################
        self._PTYPE_options = ('rect', 'tri', 'sinc', )
        self._PTYPE_labels = ('Rectangular', 'Triangular', 'Sinc', )
        self._PTYPE_group_box = Qt.QGroupBox("PTYPE")
        self._PTYPE_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._PTYPE_button_group = variable_chooser_button_group()
        self._PTYPE_group_box.setLayout(self._PTYPE_box)
        for i, label in enumerate(self._PTYPE_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._PTYPE_box.addWidget(radio_button)
        	self._PTYPE_button_group.addButton(radio_button, i)
        self._PTYPE_callback = lambda i: Qt.QMetaObject.invokeMethod(self._PTYPE_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._PTYPE_options.index(i)))
        self._PTYPE_callback(self.PTYPE)
        self._PTYPE_button_group.buttonClicked[int].connect(
        	lambda i: self.set_PTYPE(self._PTYPE_options[i]))
        self.top_grid_layout.addWidget(self._PTYPE_group_box, 1,1,2,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, False)
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1,0,1,1)
        self.qtgui_sink_x_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 0,2,2,1)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, (ptfun.pampt(sps,PTYPE,[k,beta,samp_rate])))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_f(np.hstack((np.zeros(k),1,np.zeros(k))), True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.PTYPE,[self.k,self.beta,self.samp_rate])))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.PTYPE,[self.k,self.beta,self.samp_rate])))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.PTYPE,[self.k,self.beta,self.samp_rate])))
        self.blocks_vector_source_x_0.set_data(np.hstack((np.zeros(self.k),1,np.zeros(self.k))), [])

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.PTYPE,[self.k,self.beta,self.samp_rate])))

    def get_PTYPE(self):
        return self.PTYPE

    def set_PTYPE(self, PTYPE):
        self.PTYPE = PTYPE
        self._PTYPE_callback(self.PTYPE)
        self.interp_fir_filter_xxx_0.set_taps((ptfun.pampt(self.sps,self.PTYPE,[self.k,self.beta,self.samp_rate])))


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
