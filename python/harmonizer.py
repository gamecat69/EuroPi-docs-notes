from europi import *
from time import ticks_diff, ticks_ms, sleep
from random import randint, uniform
from europi_script import EuroPiScript
import machine
import json
import gc

'''
Harmonizer
author: Nik Ansell (github.com/gamecat69)

digital_in: Clock input
analog_in: Incoming CV

button_1: TBC
button_2: TBC

output_1: Arpeggiated sequence
output_2: Root Note
output_3: 3rd note in scale
output_4: 5th note in scale
output_5: 7th Note in scale
output_6: Root minus 1 octave

'''
# Needed if using europi_script
class Harmonizer(EuroPiScript):
    def __init__(self):
        
        # Needed if using europi_script
        super().__init__()

        # Overclock the Pico for improved performance.
        machine.freq(250_000_000)

        # Enable SMPS mode for greater anologue input accuracy
        g23 = Pin(23, Pin.OUT)
        g23.value(1)

        # Params
        self.callibrationOffset = 0.0
        self.clockStep = 0
        self.step = 0
        self.maxSteps = 3
        self.ainVal = 0.0
        self.previousAinVal = 0.0
        self.noteName = 'n'
        self.noteOctave = 0
        self.noteFloat = 0.0
        self.quantizedVoltage = 0.0
        self.quantizedNote = 0.0
        self.arpSeq = [0.0, 0.0, 0.0]
        self.noteDivisions = [0.0, 0.08333333333, 0.1666666667, 0.25, 0.3333333333, 0.4166666667, 0.5, 0.5833333333, 0.6666666667, 0.75, 0.8333333333, 0.9166666667]
        self.noteNames = ['C', 'C#', 'D', "D#", 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.NoteChanged = False
        self.ainSampleCount = 0
        self.maxAinSampleCount = 1
        self.ainSamples = []
        for n in range(self.maxAinSampleCount):
            self.ainSamples.append(0.0)
        #self.ainSamples = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]\
            
        # for testing
        self.note = 0

        self.cv1Out = 0
        self.cv2Out = 0
        self.cv3Out = 0
        self.cv4Out = 0
        self.cv5Out = 0
        self.cv6Out = 0

        @din.handler
        def clockRising():
            self.handleClock()
            self.clockStep +=1
            self.step += 1

        @b1.handler
        def ainTest():
            numSamples = 100
            # Clear samples list
            ainSamples = []
            # Populate samples list
            note = 0
            for n in range(numSamples):
                ainSamples.append(0.0)
                ainSamples[n] = round(ain.read_voltage(), 2)
                sleep(0.01)
            #print(f"Test Complete. Min: {min(ainSamples)}. Max: {max(ainSamples)}. Average: {sum(ainSamples) / len(ainSamples)}")
            print(f"{self.noteDivisions[self.note]},{min(ainSamples)},{max(ainSamples)},{sum(ainSamples) / len(ainSamples)}")
            self.note += 1



    def handleClock(self):

        #self.sampleAin()

        # If the note has changed since the last clock
        if self.NoteChanged:

            self.NoteChanged = False
            # Get octave (The integer voltage rounded up e.g. 1.96 = 2)
            if self.ainVal - int(self.ainVal) > 0.97:
                self.noteOctave = round(self.ainVal)
            else:
                self.noteOctave = int(self.ainVal)
            # set self.quantizedVoltage (The quantized float voltage)
            self.quantize(self.ainVal - self.noteOctave)
            # Set noteName by indexing the noteDivisions
            self.noteName = self.noteNames[self.noteDivisions.index(self.quantizedVoltage)]
            # Set the output quantizedNote
            self.quantizedNote = self.quantizedVoltage + self.noteOctave

            # Create Major arp pattern
            #self.arpSeq = [self.quantizedNote, self.quantizedNote + (3 * 1/12), self.quantizedNote + (5 * 1/12)]

            # Create Minor arp pattern
            self.arpSeq = [self.quantizedNote, self.quantizedNote + (2 * 1/12), self.quantizedNote + (5 * 1/12)]

            cv1.voltage(self.arpSeq[self.step])
            cv2.voltage(self.quantizedNote)
            cv3.voltage(self.quantizedNote + (3 * 1/12))
            cv4.voltage(self.quantizedNote + (5 * 1/12))
            cv5.voltage(self.quantizedNote + (7 * 1/12))
            cv6.voltage(self.quantizedNote - 1)

        if self.step == self.maxSteps - 1:
            self.step = 0

    def quantize(self, voltage):
        self.quantizedVoltage = self.noteDivisions[min(range(len(self.noteDivisions)), key = lambda i: abs(self.noteDivisions[i]-voltage))]

    def main(self):
        while True:
            self.updateScreen()
            self.sampleAin()

    def sampleAin(self):

        # Sample self.maxAinSampleCount times, then set the average
        if self.ainSampleCount <= self.maxAinSampleCount-1:
            self.ainSamples[self.ainSampleCount] = round(ain.read_voltage(), 2)
            self.ainSampleCount += 1
            #print(f"SampleCount: {self.ainSampleCount}")
            #print(self.ainSamples)
        else:
            #print('FINISHED SAMPLING')
            self.ainSampleCount = 0
            self.ainVal = sum(self.ainSamples) / len(self.ainSamples)
            #self.ainSamples = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            for n in range(self.maxAinSampleCount):
                self.ainSamples[n] = 0.0

            # Correct for non-linear inaccuracies with the analogue input voltage readings
            if self.ainVal <= 1.75:
                self.callibrationOffset = -0.05
                self.ainVal += self.callibrationOffset 
                #print('-0.05 setting callibration offset')
            elif self.ainVal >= 5.5:
                self.callibrationOffset = 0.03
                self.ainVal += self.callibrationOffset
                #print('0.02 setting callibration offset') 
            else:
                #print('0.00 setting callibration offset')
                self.callibrationOffset = 0.0

            # If the voltage has changed by more than a semi-tone, startsampling again
            if (abs(self.ainVal - self.previousAinVal)) > 1/13:
                self.ainSampleCount = 0
                self.NoteChanged = True
                #print('NOTE CHANGED')
            
            self.previousAinVal = self.ainVal

        # # Only resample if the incomign voltage has changed more than 1/11th.
        # # This should avoid flip-flopping when the value is on a boundary
        # #print(f"prev: {self.previousAinVal}")
        # #print(f"new : {self.ainVal}")
        # #print(f"dif : {abs(self.ainVal - self.previousAinVal)}")
        # if (abs(self.ainVal - self.previousAinVal)) > 1/11:
        #     # The integer voltage (octave)
        #     self.noteOctave = int(self.ainVal)
        #     # The float part of the voltage
        #     self.noteFloat = self.ainVal - self.noteOctave

        #     self.previousAinVal = self.ainVal
        #     self.NoteChanged = True
        #     #print('NOTE CHANGED')

    def updateScreen(self):
        # Clear the screen
        oled.fill(0)
        oled.text('vin :' + str(self.ainVal), 0, 0, 1)
        oled.text('vout:' + str(self.quantizedNote), 0, 12, 1)
        oled.text(self.noteName + str(self.noteOctave), 100, 20, 1)
        #oled.text(str(self.NoteChanged), 50, 20, 1)
        oled.text( str(self.callibrationOffset), 0, 20, 1)
        oled.show()

if __name__ == '__main__':
    dm = Harmonizer()
    dm.main()