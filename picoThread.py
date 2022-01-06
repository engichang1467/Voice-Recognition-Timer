from threading import Thread, Timer
import os
import struct
from picovoice import Picovoice
import pyaudio

class PicovoiceThread(Thread):
    def __init__(self, time_label, access_key):
        super().__init__()

        self._access_key = access_key

        self.time_label = time_label

        self._is_paused = False
        self._hours = 0
        self._minutes = 0
        self._seconds = 0

        self._is_ready = False
        self._stop = False
        self._is_stopped = False

        self._countdown()

    def _countdown(self):
        if not self._is_paused:
            update = False
            if self._seconds > 0:
                self._seconds -= 1
                update = True
            elif self._minutes > 0:
                self._minutes -= 1
                self._seconds = 59
                update = True
            elif self._hours > 0:
                self._hours -= 1
                self._minutes = 59
                self._seconds = 59
                update = True

            if update:
                self.time_label.configure(text='%.2d : %.2d : %.2d' % (self._hours, self._minutes, self._seconds))

        Timer(1, self._countdown).start()

    @staticmethod
    def keywordPath():
        return os.path.join(
            os.path.dirname(__file__),
            'hey_pico_mac_v2.0.0/hey-pico_en_mac_v2_0_0.ppn'
        )

    @staticmethod
    def contextPath():
        return os.path.join(
            os.path.dirname(__file__),
            'pico_mac_v2.0.0/Pico_en_mac_v2_0_0.rhn'
        )

    def _wake_word_callback(self):
        self.time_label.configure(fg='red')

    def _inference_callback(self, inference):
        self.time_label.configure(fg='black')

        if inference.is_understood:
            if inference.intent == 'setAlarm':
                self._is_paused = False
                self._hours = int(inference.slots['hours']) if 'hours' in inference.slots else 0
                self._minutes = int(inference.slots['minutes']) if 'minutes' in inference.slots else 0
                self._seconds = int(inference.slots['seconds']) if 'seconds' in inference.slots else 0
                self.time_label.configure(text='%.2d : %.2d : %.2d' % (self._hours, self._minutes, self._seconds))
            elif inference.intent == 'reset':
                self._is_paused = False
                self._hours = 0
                self._minutes = 0
                self._seconds = 0
                self.time_label.configure(text='00 : 00 : 00')
            elif inference.intent == 'pause':
                self._is_paused = True
            elif inference.intent == 'resume':
                self._is_paused = False
            else:
                raise ValueError("unsupported intent '%s'" % inference.intent)

    def run(self):
        pv = None
        py_audio = None
        audio_stream = None

        try:
            pv = Picovoice(
                access_key=self._access_key,
                keyword_path=self.keywordPath(),
                porcupine_sensitivity=0.75,
                wake_word_callback=self._wake_word_callback,
                context_path=self.contextPath(),
                inference_callback=self._inference_callback)

            print(pv.context_info)

            py_audio = pyaudio.PyAudio()
            audio_stream = py_audio.open(
                rate=pv.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=pv.frame_length)

            self._is_ready = True

            while not self._stop:
                pcm = audio_stream.read(pv.frame_length)
                pcm = struct.unpack_from("h" * pv.frame_length, pcm)
                pv.process(pcm)
        finally:
            if audio_stream is not None:
                audio_stream.close()
            if py_audio is not None:
                py_audio.terminate()

            if pv is not None:
                pv.delete()

        self._is_stopped = True

    def is_ready(self):
        return self._is_ready

    def stop(self):
        self._stop = True

    def is_stopped(self):
        return self._is_stopped