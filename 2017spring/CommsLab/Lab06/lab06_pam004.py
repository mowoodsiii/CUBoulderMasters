#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lab 6, PAM Example 4
# Author: Maurice Woods
# Description: ECEN 4652 :: Comms Lab
# Generated: Wed Mar 22 18:51:33 2017
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
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ptfun as pf
import sip
import sys
from gnuradio import qtgui


class lab06_pam004(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 6, PAM Example 4")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 6, PAM Example 4")
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

        self.settings = Qt.QSettings("GNU Radio", "lab06_pam004")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.Fs = Fs = 256000
        self.FB = FB = 32000
        self.timing_loop_bw = timing_loop_bw = 0.0628
        self.sym_dly = sym_dly = 0
        self.sps = sps = Fs/FB
        self.samp_dly = samp_dly = 0
        self.ptype = ptype = 'rect'
        self.pparms = pparms = [5,0.5]
        self.nfilts = nfilts = 32
        self.An = An = 0

        ##################################################
        # Blocks
        ##################################################
        self._timing_loop_bw_range = Range(0, 0.2, 0.01, 0.0628, 200)
        self._timing_loop_bw_win = RangeWidget(self._timing_loop_bw_range, self.set_timing_loop_bw, 'Timing Loop BW', "counter_slider", float)
        self.top_grid_layout.addWidget(self._timing_loop_bw_win, 1,1,1,1)
        self._sym_dly_range = Range(0, 16, 1, 0, 200)
        self._sym_dly_win = RangeWidget(self._sym_dly_range, self.set_sym_dly, 'Symbol Delay', "counter_slider", int)
        self.top_grid_layout.addWidget(self._sym_dly_win, 0,1,1,1)
        self._samp_dly_range = Range(0, 16, 1, 0, 200)
        self._samp_dly_win = RangeWidget(self._samp_dly_range, self.set_samp_dly, 'Sample Delay', "counter_slider", int)
        self.top_grid_layout.addWidget(self._samp_dly_win, 0,0,1,1)
        self._ptype_options = ('rect', 'man', 'rrcf', )
        self._ptype_labels = ('Rectangular', 'Manchester', 'Root Raised Cosine in Freq', )
        self._ptype_group_box = Qt.QGroupBox('ptype')
        self._ptype_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ptype_button_group = variable_chooser_button_group()
        self._ptype_group_box.setLayout(self._ptype_box)
        for i, label in enumerate(self._ptype_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ptype_box.addWidget(radio_button)
        	self._ptype_button_group.addButton(radio_button, i)
        self._ptype_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ptype_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ptype_options.index(i)))
        self._ptype_callback(self.ptype)
        self._ptype_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ptype(self._ptype_options[i]))
        self.top_grid_layout.addWidget(self._ptype_group_box, 2,0,1,2)
        self._An_range = Range(0, 2, 0.1, 0, 200)
        self._An_win = RangeWidget(self._An_range, self.set_An, 'An', "counter_slider", float)
        self.top_grid_layout.addWidget(self._An_win, 1,0,1,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	Fs, #samp_rate
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

        labels = ['err', 'rate', 'phase', '', '',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 3,0,1,2)
        self.qtgui_sink_x_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	Fs, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 4,0,1,2)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, (pf.pampt(sps,ptype,pparms)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(sps, timing_loop_bw, (1/float(sps)*pf.pampt(sps*nfilts,ptype,pparms)), nfilts, nfilts/2.0, 0.7, 1)
        self.digital_binary_slicer_fb_1 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in 'The quick brown fox...'), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, FB,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/19', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_char*1, samp_dly)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, sym_dly)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, An, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_1, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_binary_slicer_fb_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 1), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 3), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 2), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab06_pam004")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs
        self.set_sps(self.Fs/self.FB)
        self.qtgui_time_sink_x_0.set_samp_rate(self.Fs)
        self.qtgui_sink_x_0.set_frequency_range(0, self.Fs)

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB
        self.set_sps(self.Fs/self.FB)
        self.blocks_throttle_0.set_sample_rate(self.FB)

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_sym_dly(self):
        return self.sym_dly

    def set_sym_dly(self, sym_dly):
        self.sym_dly = sym_dly
        self.blocks_delay_0.set_dly(self.sym_dly)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.interp_fir_filter_xxx_0.set_taps((pf.pampt(self.sps,self.ptype,self.pparms)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((1/float(self.sps)*pf.pampt(self.sps*self.nfilts,self.ptype,self.pparms)))

    def get_samp_dly(self):
        return self.samp_dly

    def set_samp_dly(self, samp_dly):
        self.samp_dly = samp_dly
        self.blocks_delay_0_0.set_dly(self.samp_dly)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)
        self.interp_fir_filter_xxx_0.set_taps((pf.pampt(self.sps,self.ptype,self.pparms)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((1/float(self.sps)*pf.pampt(self.sps*self.nfilts,self.ptype,self.pparms)))

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms
        self.interp_fir_filter_xxx_0.set_taps((pf.pampt(self.sps,self.ptype,self.pparms)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((1/float(self.sps)*pf.pampt(self.sps*self.nfilts,self.ptype,self.pparms)))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.digital_pfb_clock_sync_xxx_0.update_taps((1/float(self.sps)*pf.pampt(self.sps*self.nfilts,self.ptype,self.pparms)))

    def get_An(self):
        return self.An

    def set_An(self, An):
        self.An = An
        self.analog_noise_source_x_0.set_amplitude(self.An)


def main(top_block_cls=lab06_pam004, options=None):

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
