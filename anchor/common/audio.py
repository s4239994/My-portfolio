import io
import math
import struct
import wave


def generate_ambient_tone(duration_sec: int = 45, sample_rate: int = 22050) -> bytes:
    """A soft, layered sine-wave drone -- just a pleasant ambient sound to
    breathe along with. Not based on any brainwave-entrainment claim, and
    not a copy of any existing track."""
    n_samples = duration_sec * sample_rate
    freqs = [110.0, 165.0, 220.0]  # a soft, consonant low chord
    amps = [0.5, 0.3, 0.25]

    buf = io.BytesIO()
    wav = wave.open(buf, "wb")
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    fade_samples = sample_rate * 3  # 3-second fade in/out
    frames = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        value = 0.0
        for f, a in zip(freqs, amps):
            value += a * math.sin(2 * math.pi * f * t)
        value /= len(freqs)

        envelope = 1.0
        if i < fade_samples:
            envelope = i / fade_samples
        elif i > n_samples - fade_samples:
            envelope = (n_samples - i) / fade_samples

        sample = int(value * envelope * 12000)
        frames += struct.pack("<h", sample)

    wav.writeframes(bytes(frames))
    wav.close()
    return buf.getvalue()
