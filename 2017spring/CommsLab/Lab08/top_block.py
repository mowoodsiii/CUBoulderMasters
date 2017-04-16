#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AM Receiver 01
# Generated: Sat Apr 15 12:33:04 2017
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
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
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
        gr.top_block.__init__(self, "AM Receiver 01")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AM Receiver 01")
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
        self.samp_rate_2 = samp_rate_2 = 512000
        self.samp_rate_1 = samp_rate_1 = 32000
        self.fcorr = fcorr = 0
        self.fc = fc = 124000

        ##################################################
        # Blocks
        ##################################################
        self._fcorr_range = Range(-10, 10, 0.01, 0, 200)
        self._fcorr_win = RangeWidget(self._fcorr_range, self.set_fcorr, 'Fine Tune', "counter_slider", float)
        self.top_layout.addWidget(self._fcorr_win)
        self._fc_options = (124000, 144000, )
        self._fc_labels = ('Station 1', 'Station 2', )
        self._fc_group_box = Qt.QGroupBox("fc")
        self._fc_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._fc_button_group = variable_chooser_button_group()
        self._fc_group_box.setLayout(self._fc_box)
        for i, label in enumerate(self._fc_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._fc_box.addWidget(radio_button)
        	self._fc_button_group.addButton(radio_button, i)
        self._fc_callback = lambda i: Qt.QMetaObject.invokeMethod(self._fc_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._fc_options.index(i)))
        self._fc_callback(self.fc)
        self._fc_button_group.buttonClicked[int].connect(
        	lambda i: self.set_fc(self._fc_options[i]))
        self.top_layout.addWidget(self._fc_group_box)
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_1, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)



        self.qtgui_sink_x_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_2, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.low_pass_filter_0 = filter.fir_filter_fff(16, firdes.low_pass(
        	2, samp_rate_2, 4000, 2000, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate_2,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/home/maurice/Desktop/AMsignal_002.bin', True)
        self.audio_sink_0 = audio.sink(samp_rate_1, '', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate_2, analog.GR_COS_WAVE, fcorr, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate_2, analog.GR_COS_WAVE, fc, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate_2(self):
        return self.samp_rate_2

    def set_samp_rate_2(self, samp_rate_2):
        self.samp_rate_2 = samp_rate_2
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate_2)
        self.low_pass_filter_0.set_taps(firdes.low_pass(2, self.samp_rate_2, 4000, 2000, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_2)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate_2)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate_2)

    def get_samp_rate_1(self):
        return self.samp_rate_1

    def set_samp_rate_1(self, samp_rate_1):
        self.samp_rate_1 = samp_rate_1
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate_1)

    def get_fcorr(self):
        return self.fcorr

    def set_fcorr(self, fcorr):
        self.fcorr = fcorr
        self.analog_sig_source_x_0_0.set_frequency(self.fcorr)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self._fc_callback(self.fc)
        self.analog_sig_source_x_0.set_frequency(self.fc)


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
