import sys
import numpy as np
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from Picoscope import Picoscope
import pyqtgraph as pg
import time as t
try:
    from picosdk.ps5000a import ps5000a as ps
    from picosdk.functions import adc2mV, assert_pico_ok, mV2adc
except ImportError:
    print('Picotech libries not installed')

# the class is only run through once, so a function needs to be called.
class Window(QMainWindow):
    def __init__(self):
        self.plt = pg.plot()
        pg.QtGui.QApplication.processEvents()
        super().__init__()
        self.pico = Picoscope()
        self.possibleResValues = {
            "8-bit": "PS5000A_DR_8BIT",
            "12-bit": "PS5000A_DR_12BIT",
            "14-bit": "PS5000A_DR_14BIT",
            "15-bit": "PS5000A_DR_15BIT",
            "16-bit": "PS5000A_DR_16BIT"}
        self.resolutionString = ''
        self.possibleSamplingModes = {'Rapid Block Mode': 'rapid_block'}
        self.possibleRanges = {
            '10 mV': {'psRANGE': 'PS5000A_10MV', 'intRange': 10},
            '20 mV': {'psRANGE': 'PS5000A_20MV', 'intRange': 20},
            '50 mV': {'psRANGE': 'PS5000A_50MV', 'intRange': 50},
            '100 mV': {'psRANGE': 'PS5000A_100MV', 'intRange': 100},
            '200 mV': {'psRANGE': 'PS5000A_200MV', 'intRange': 200},
            '500 mV': {'psRANGE': 'PS5000A_500MV', 'intRange': 500},
            '1 V': {'psRANGE': 'PS5000A_1V', 'intRange': 1000},
            '2 V': {'psRANGE': 'PS5000A_2V', 'intRange': 2000},
            '5 V': {'psRANGE': 'PS5000A_5V', 'intRange': 5000},
            '10 V': {'psRANGE': 'PS5000A_10V', 'intRange': 10000},
            '20 V': {'psRANGE': 'PS5000A_20V', 'intRange': 20000},
        }
        self.possibleTriggers = {
            'External': True,
            'Channel A': False,
        }

        # setting title
        self.setWindowTitle("Python")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method for UI components
        self.UiComponents()

        # showing all the widgets
        self.show()

    def UiComponents(self):
        # Setting window title
        self.setWindowTitle("Picoscope GUI")

        layout = QVBoxLayout()
        form_layout = QFormLayout()
        # setCentralWidget for qmainwindow

        # ComboBox to select the avialable digital resolutions
        self.resOptions = QComboBox(self)
        self.resOptions.setToolTip('Selection digital resolution of the Picoscope')
        # self.resOptions.addItem('Select a resolution...')
        resolutions = self.possibleResValues.keys()
        # resolutions = ['8-bit', '12-bit', '14-bit', '15-bit', '16-bit']
        for resolution in resolutions:
            self.resOptions.addItem(resolution)
        self.resOptions.activated[int].connect(self.ResSelection)
        # Set our defualt index, should be done in config
        default_index = len(resolutions) - 1
        self.resOptions.setCurrentIndex(default_index)
        self.ResSelection(default_index)

        # ComboBox to select the available voltage range scales
        self.rangeScaleOptions = QComboBox(self)
        self.rangeScaleOptions.setToolTip('Select the voltage scale for the active channel')
        rangeScaleOpts = self.possibleRanges.keys()
        for rangeScaleOpt in rangeScaleOpts:
            self.rangeScaleOptions.addItem(rangeScaleOpt)
        self.rangeScaleOptions.activated[int].connect(self.RangeScaleSelection)
        # Set our default index, should be done in config
        default_index = 9
        self.rangeScaleOptions.setCurrentIndex(default_index)
        self.RangeScaleSelection(default_index)

        # ComboBox to select the available sampling modes
        self.samplingOptions = QComboBox(self)
        self.samplingOptions.setToolTip('Select the sampling mode of the Picoscope')
        samplingOpts = self.possibleSamplingModes.keys()
        for samplingOpt in samplingOpts:
            self.samplingOptions.addItem(samplingOpt)
        self.samplingOptions.activated[int].connect(self.SamplingSelection)
        # Set our default index, should be done in config
        default_index = 0
        self.samplingOptions.setCurrentIndex(default_index)
        self.SamplingSelection(default_index)

        # QCombobox
        self.triggerOptions = QComboBox(self)
        self.triggerOptions.setToolTip('Select the trigger input of the Picoscope')
        triggerOpts = self.possibleTriggers.keys()
        for triggerOpt in triggerOpts:
            self.triggerOptions.addItem(triggerOpt)
        self.triggerOptions.activated[int].connect(self.TriggerSelection)
        # Set our default index, should be done in config
        default_index = 0
        self.triggerOptions.setCurrentIndex(default_index)
        self.TriggerSelection(default_index)

        # buttons
        self.btn = QPushButton("Plot")

        self.btn2 = QPushButton("Initialize")
        self.btn2.pressed.connect(self.confirm_data) # Press to activate function


        # spinboxes
        self.waveforms = QSpinBox()
        self.waveforms.setMinimum(1)
        self.waveforms.setMaximum(100)

        self.presamples = QSpinBox()
        self.presamples.setMinimum(0)
        self.presamples.setMaximum(10000)

        self.xMin = QSpinBox()
        self.xMin.setMinimum(-10000000)
        self.xMin.setMaximum(10000000)
        self.xMin.setValue(0)
        self.xMin.valueChanged[int].connect(self.PlotSettings)
        self.xMax = QSpinBox()
        self.xMax.setMinimum(-10000000)
        self.xMax.setMaximum(10000000)
        self.xMax.setValue(10000)
        self.xMax.valueChanged[int].connect(self.PlotSettings)
        self.yMin = QSpinBox()
        self.yMin.setMinimum(-10000000)
        self.yMin.setMaximum(10000000)
        self.yMin.setValue(-10000)
        self.yMin.valueChanged[int].connect(self.PlotSettings)
        self.yMax = QSpinBox()
        self.yMax.setMinimum(-10000000)
        self.yMax.setMaximum(10000000)
        self.yMax.setValue(10000)
        self.PlotSettings()

        self.yMax.valueChanged[int].connect(self.PlotSettings)


        self.presamples = QSpinBox()
        self.presamples.setMinimum(0)
        self.presamples.setMaximum(10000)

        self.postsamples = QSpinBox()
        self.postsamples.setMinimum(10)
        self.postsamples.setMaximum(10000)
        self.postsamples.setValue(2500)

        self.triggerthreshold = QSpinBox()
        self.triggerthreshold.setMinimum(0)
        self.triggerthreshold.setMaximum(10000)
        self.triggerthreshold.setValue(5000)


        # label
        self.setting_lbl = QLabel("User Settings:")
        self.font = self.setting_lbl.font()
        self.font.setPointSize(12)
        self.setting_lbl.setFont(self.font)
        self.setting_lbl.setAlignment(Qt.AlignLeft)

        print(self.samplingOptions.currentText())

        # this one activates after a selection is made
        self.samplingOptions.activated.connect(self.SamplingSelection)


        # Adding widgets
        #layout.addWidget(self.setting_lbl)
        form_layout.addRow('Trigger source',self.triggerOptions)
        form_layout.addRow('Voltage range', self.rangeScaleOptions)
        form_layout.addRow('Resolution', self.resOptions)
        form_layout.addRow('Sampling mode', self.samplingOptions)
        form_layout.addRow('Number of waveforms', self.waveforms)
        form_layout.addRow('Pre-trigger samples', self.presamples)
        form_layout.addRow('Post-trigger samples',self.postsamples)
        form_layout.addRow('Trigger Threshold', self.triggerthreshold)
        form_layout.addRow('Initialize', self.btn2)
        form_layout.addRow('Plot xMin (ns)', self.xMin)
        form_layout.addRow('Plot xMax (ns)', self.xMax)
        form_layout.addRow('Plot yMin (mV)', self.yMin)
        form_layout.addRow('Plot yMax (mV)', self.yMax)

        # Setting up GroupBox
        self.settingsGroupBox = QGroupBox('Picoscope Settings')
        self.settingsGroupBox.setLayout(form_layout)
        self.settingsGroupBox.setStyleSheet('QGroupBox { color: #52988C; font: bold 12pt; }')

        # Setting grouped layout in settingsGroupBox
        widget = QWidget()

        grid = QGridLayout() # Note: Layout is a bit finicky
        grid.addWidget(self.settingsGroupBox, 0, 0, 1, 0) # last two numbers extend or shorten the box
        #grid.addWidget(self.samplingOptions, 1, 0, 1, 1)
        grid.addWidget(self.btn, 1, 1, 1, 1)
        #grid.addWidget(self.postsamples, 2, 0, 1, 1)

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    #@Slot()
    def testing(self):
        print("Testing function: " + self.samplingOptions.currentText())

    #@Slot()
    def confirm_data(self):

        self.trigger = self.possibleTriggers[self.triggerOptions.currentText()]# retrieves current text
        self.range = self.possibleRanges[self.rangeScaleOptions.currentText()]
        self.res = self.possibleResValues[self.resOptions.currentText()]
        self.samplingMode = self.possibleSamplingModes[self.samplingOptions.currentText()]
        self.pico.close()
        print(self.range['intRange'])
        #self.pico.setup(range_mV=10000, blocks=100, timebase=2, external=True, triggermV=5000, preSamples=0,
                   #postSamples=2500)
        self.pico.setup(range_mV = self.range['intRange'], blocks = self.waveforms.value(), timebase = 2, external = self.trigger, triggermV= self.triggerthreshold.value(), preSamples = self.presamples.value(), postSamples = self.postsamples.value())
        self.pico.block()
        average = np.mean(self.pico.data_mVRay, axis=0)
        self.plt.plot(self.pico.time, average, clear=True)

    @Slot(int)
    def PlotSettings(self):
        self.plt.setXRange(self.xMin.value(), self.xMax.value(), padding=.01)  # nanoseconds
        self.plt.setYRange(self.yMin.value(), self.yMax.value(), padding=.1)  # millivolts

    @Slot(int)
    def ResSelection(self, resolution_index=None):
        '''
        Slot function that is called when we select an item in the resolution dropdown menu.
        '''
        if resolution_index is not None:
            this_text = self.resOptions.itemText(resolution_index)
            # print(this_text)
            # this_ps_resolution = self.psResolutionList[resolution]
            # print(this_ps_resolution)
            print('Resolution is {}'.format(self.resolutionString))
        else:
            print('Got None.')

    @Slot(int)
    def SamplingSelection(self, sampling_index=None):
        print("Changing sampling selection")
        '''
        Slot function that is called when the sampling type is selected in the dropdown menu.
        '''
        if sampling_index is not None:
            this_text = self.samplingOptions.itemText(sampling_index)
            print('Sampling Mode is {}'.format(self.possibleSamplingModes[this_text]))
        else:
            print('Got None')

    @Slot(int)
    def TriggerSelection(self, trigger_index=None):
        print("Changing trigger selection")
        '''
        Slot function that is called when the sampling type is selected in the dropdown menu.
        '''
        if trigger_index is not None:
            this_text = self.triggerOptions.itemText(trigger_index)
            print('Sampling Mode is {}'.format(self.possibleTriggers[this_text]))
        else:
            print('Got None')

    @Slot(int)
    def WaveformSelection(self, waveform_index=None):
        print("Changing waveform selection")
        '''
        Slot function that is called when the sampling type is selected in the dropdown menu.
        '''
        if waveform_index is not None:
            this_text = self.waveformOptions.itemText(waveform_index)
            print('Number of waveforms is {}')
        else:
            print('Got None')

    @Slot(int)
    def RangeScaleSelection(self, range_index=None):
        print("Changing voltage range")



def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()