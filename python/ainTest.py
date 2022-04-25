from europi import *
from time import ticks_diff, ticks_ms, sleep
from random import randint, uniform
import machine


class ainTest():
    def __init__(self):

        # Overclock the Pico for improved performance.
        machine.freq(250_000_000)

        # Enable SMPS mode for greater anologue input accuracy
        g23 = Pin(23, Pin.OUT)
        g23.value(1)

        # for testing
        self.note = 0
        self.noteDivisions = [0.0, 0.08333333333, 0.1666666667, 0.25, 0.3333333333, 0.4166666667, 0.5, 0.5833333333, 0.6666666667, 0.75, 0.8333333333, 0.9166666667]
        self.noteNames = ['C', 'C#', 'D', "D#", 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.testStarted = False
        self.octave = 0

        @b1.handler
        def ainTest():
            numSamples = 100
            if not self.testStarted:
                self.updateScreen()
                self.testStarted = True
                return
            if self.testStarted:
                # Clear samples list
                ainSamples = []
                # Populate samples list
                for n in range(numSamples):
                    ainSamples.append(0.0)
                    ainSamples[n] = round(ain.read_voltage(), 2)
                    sleep(0.01)
                #print(f"Test Complete. Min: {min(ainSamples)}. Max: {max(ainSamples)}. Average: {sum(ainSamples) / len(ainSamples)}")
                print(f"{self.noteNames[self.note]},{self.noteDivisions[self.note] + self.octave},{min(ainSamples)},{max(ainSamples)},{sum(ainSamples) / len(ainSamples)}")
                if self.note == len(self.noteNames)-1:
                    self.note = 0
                    self.octave += 1
                else:
                    self.note += 1
                self.updateScreen()

    def main(self):
        pass

    def updateScreen(self):
        # Clear the screen
        oled.fill(0)
        oled.text(self.noteNames[self.note] + ' ' + str(self.octave), 0, 0, 1)
        oled.show()

if __name__ == '__main__':
    dm = ainTest()
    dm.main()