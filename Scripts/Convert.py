import os
import subprocess

# Set the input folder containing the WAV files
input_folder = 'wavs'

# Set the output folder where the converted files will be saved
output_folder = 'converted_wavs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set the desired specifications
sample_rate = 22050
bit_depth = 16
channels = 1

# Function to convert the audio file
def convert_audio(input_path, output_path, sample_rate, bit_depth, channels):
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-ar', str(sample_rate),
        '-ac', str(channels),
        '-acodec', 'pcm_s16le',
        output_path,
    ]
    subprocess.run(cmd)

# Iterate through the input folder and convert all WAV files
for file_name in os.listdir(input_folder):
    if file_name.endswith('.wav'):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        convert_audio(input_path, output_path, sample_rate, bit_depth, channels)

print("All WAV files have been converted.")
