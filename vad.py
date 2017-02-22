"""
 Voice Activity Detector based on WebRTC VAD (https://github.com/wiseman/py-webrtcvad)
 Copyright (c) 2016 Seeed Technology Limited.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import collections
import sys

import webrtcvad


class WebRTCVAD:
    def __init__(self, sample_rate=16000, level=3):
        """

        Args:
            sample_rate: audio sample rate
            level: between 0 and 3. 0 is the least aggressive about filtering out non-speech, 3 is the most aggressive.
        """
        self.sample_rate = sample_rate

        self.frame_ms = 30
        self.frame_bytes = int(2 * self.frame_ms * self.sample_rate / 1000)   # S16_LE, 2 bytes width

        self.vad = webrtcvad.Vad(level)
        self.active = False
        self.data = b''
        self.history = collections.deque(maxlen=128)

    def is_speech(self, data):
        self.data += data
        while len(self.data) >= self.frame_bytes:
            frame = self.data[:self.frame_bytes]
            self.data = self.data[self.frame_bytes:]

            if self.vad.is_speech(frame, self.sample_rate):
                sys.stdout.write('1')
                self.history.append(1)
            else:
                sys.stdout.write('0')
                self.history.append(0)

            num_voiced = 0
            for i in range(-8, 0):
                try:
                    num_voiced += self.history[i]
                except IndexError:
                    continue

            if not self.active:
                if num_voiced >= 4:
                    sys.stdout.write('+')
                    self.active = True
                    break
                elif len(self.history) == self.history.maxlen and sum(self.history) == 0:
                    for _ in range(self.history.maxlen / 2):
                        self.history.popleft()

            else:
                if num_voiced < 1:
                    sys.stdout.write('-')
                    self.active = False
                elif sum(self.history) > self.history.maxlen * 0.9:
                    for _ in range(int(self.history.maxlen / 2)):
                        self.history.popleft()

        sys.stdout.flush()

        return self.active

    def reset(self):
        self.data = b''
        self.active = False
        self.history.clear()


vad = WebRTCVAD()

