# cancel_echo.py
import logging
import argcomplete
import minimal
import numpy as np
from buffer import Buffering__verbose, Buffering
import sounddevice as sd
import numpy as np
import struct
import threading




class EchoCancellation(Buffering):
    def __init__(self, delay_samples=200, attenuation_factor=0):
        super().__init__()
        self.delay_samples = delay_samples
        self.attenuation_factor = attenuation_factor
        self.delay_buffer = np.zeros((self.cells_in_buffer, self.delay_samples))

    def apply_echo_cancellation(self, signal, echo):
        # Aplicar atenuación al eco
        attenuated_echo = echo * self.attenuation_factor

        # Obtener la señal retrasada del buffer
        delayed_signal = self.delay_buffer[self.played_chunk_number % self.cells_in_buffer]

        # Actualizar el buffer con la señal actual
        self.delay_buffer[self.played_chunk_number % self.cells_in_buffer] = signal

        # Sumar la señal actual con el eco atenuado y retrasado
        return signal - attenuated_echo + delayed_signal

    def _record_io_and_play_with_echo_cancellation(self, indata, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.CHUNK_NUMBERS
        packed_chunk = self.pack(self.chunk_number, indata)
        self.send(packed_chunk)

        chunk = self.unbuffer_next_chunk()
        echo_cancellation_result = self.apply_echo_cancellation(indata, chunk)

        self.play_chunk(outdata, echo_cancellation_result)

    def _read_io_and_play_with_echo_cancellation(self, outdata, frames, time, status):
        self.chunk_number = (self.chunk_number + 1) % self.CHUNK_NUMBERS
        read_chunk = self.read_chunk_from_file()
        packed_chunk = self.pack(self.chunk_number, read_chunk)
        self.send(packed_chunk)

        chunk = self.unbuffer_next_chunk()
        echo_cancellation_result = self.apply_echo_cancellation(read_chunk, chunk)

        self.play_chunk(outdata, echo_cancellation_result)
        return read_chunk

# Versión para salida verbose
class EchoCancellation__verbose(EchoCancellation, Buffering__verbose):
    def __init__(self, delay_samples=200, attenuation_factor=0):
        super().__init__(delay_samples=delay_samples, attenuation_factor=attenuation_factor)

 
if __name__ == "__main__":
    minimal.parser.description = __doc__
    try:
        argcomplete.autocomplete(minimal.parser)
    except Exception:
        logging.warning("argcomplete no funciona :-/")
    minimal.args = minimal.parser.parse_known_args()[0]

    # Crear una instancia de la clase deseada (verbose o no verbose)
    if minimal.args.show_stats or minimal.args.show_samples:
        intercom = EchoCancellation__verbose()
    else:
        intercom = EchoCancellation()

    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT recibida")
    finally:
        intercom.print_final_averages()
