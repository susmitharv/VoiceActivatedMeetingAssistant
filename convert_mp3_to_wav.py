from pydub import AudioSegment
import pydub.utils
import os

# Absolute paths to ffmpeg and ffprobe
ffmpeg_path = r"D:\Susmitha\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
ffprobe_path = r"D:\Susmitha\ffmpeg-7.1.1-full_build\bin\ffprobe.exe"

# Force pydub to use them globally BEFORE any AudioSegment call
pydub.utils.get_encoder_name = lambda: ffmpeg_path
pydub.utils.get_prober_name = lambda: ffprobe_path

# Confirm executables exist
if not os.path.exists(ffmpeg_path): raise FileNotFoundError("FFmpeg path is wrong")
if not os.path.exists(ffprobe_path): raise FileNotFoundError("FFprobe path is wrong")

# Convert
input_file = "Record.mp3"
output_file = "converted.wav"

audio = AudioSegment.from_file(input_file, format="mp3")
audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
audio.export(output_file, format="wav")

print(f"✅ Conversion complete: {output_file}")
