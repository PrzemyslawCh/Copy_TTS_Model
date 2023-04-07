import os
import wave

def get_wav_duration(file_path):
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        duration = frames / float(frame_rate)
        return duration

def main():
    wav_folder = 'wavs'
    wav_files = [f for f in os.listdir(wav_folder) if f.endswith('.wav')]

    total_duration = 0
    for wav_file in wav_files:
        file_path = os.path.join(wav_folder, wav_file)
        duration = get_wav_duration(file_path)
        total_duration += duration

    print(f"Total duration of all WAV files: {total_duration:.2f} seconds")

if __name__ == "__main__":
    main()
