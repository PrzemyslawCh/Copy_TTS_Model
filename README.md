# TTS Model Training Scripts
This project contains a set of scripts designed to automate the process of downloading, converting, and analyzing Text-to-Speech (TTS) models from fakeyou.com.

## Contents
The repository includes the following scripts:

Auto.py: This script automates the process of calling the API and saving the .wav files to a local directory.
Convert.py: This script converts the downloaded .wav files to a specified sample rate, bit depth, and number of channels.
Time.py: This script calculates the total duration of all .wav files combined.
text.txt: A text file that contains sentences in the following format: wavs/1.wav|In 100 meters, turn left onto Maple Street. This file is used by Auto.py to download the necessary files for TTS model training.
## Usage
Auto.py: Run this script to start the process. It will read the sentences from text.txt and make calls to the API to download the corresponding .wav files.

Usage: python Auto.py

Convert.py: After downloading the .wav files, use this script to convert them to the desired format. The script is currently set to convert files to a sample rate of 22050, a bit depth of 16, and a single channel.

Usage: python Convert.py

Time.py: Use this script to calculate the total duration of all the .wav files. This can be useful for understanding the total amount of speech data you have.

Usage: python Time.py

Ensure that the scripts are run in the above order for proper functioning.

## Dependencies
To run these scripts, you will need Python 3 and libraries which are inside scripts

## Contributing
Contributions are welcome. Please open an issue to discuss your idea or submit a Pull Request.

## License
MIT License

