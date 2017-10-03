################################################################################
# sound.py
# A. Hornof (ajh) - Sept 2017
#
# Sound class and functions for use in an auditory menu assignment.
#
# PyAudio-specific code adapted from https://people.csail.mit.edu/hubert/pyaudio/
# by ajh - Sept 2017
#
################################################################################
__author__ = 'hornof'

import pyaudio
import wave

###############################################################################
# Initialize module.
################################################################################

# Global variables
PYAUDIO = pyaudio.PyAudio()     # Instantiate PyAudio.
# Keep track of the last object played so the next one can stop it.
LAST_OBJECT_PLAYED = None

################################################################################
# class Play
# The class does much more than play a sound. It creates an object that stops a
#   previously-playing sound, opens a sound file (the name of which was passed
#   in),  and plays the sound file in a separate thread (that can be interrupted
#   by another "Play" object being created and played.
# However, because these details can all probably be hidden from the programmer,
#   I just call it a Play object.
# A new Play object will be created and played for every sound played.
################################################################################
class Play:

    # Initializer function
    def __init__(self, sound_file_name):

        # Declare as global to gain access the module-level global variable.
        global LAST_OBJECT_PLAYED

        # Instance variables.
        self.filename = sound_file_name
        # Open file using the wave module.
        self.wave_object = wave.open(self.filename, 'rb')
        # Initialize the variable for the pyaudio stream that will play the sound.
        self.pyaudio_stream = None

        # Close the stream for the last SoundObject that was played.
        if LAST_OBJECT_PLAYED:      # If there is a last object
            LAST_OBJECT_PLAYED.close()

        # Create the callback function for the stream that will be created
        #   to play this sound object.
        # (See https://people.csail.mit.edu/hubert/pyaudio/docs/)
        def callback(in_data, frame_count, time_info, status):
            data = self.wave_object.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # Open the stream and play the sound.
        self.pyaudio_stream = PYAUDIO.open(format=PYAUDIO.get_format_from_width
                (self.wave_object.getsampwidth()),
            channels=self.wave_object.getnchannels(),
            rate=self.wave_object.getframerate(),
            output=True,
            stream_callback=callback,
            start=True)

        # Record this stream as the last stream played.
        LAST_OBJECT_PLAYED = self

    # Close pyaudio PlaySound object.
    def close(self):
        self.wave_object.close()
        self.pyaudio_stream.close()

################################################################################
# Concatenate two audio files.
# From http://web.mit.edu/jgross/Public/21M.065/sound.py 9-24-2017
# File parameters must all match, or else the exception will be called.
# Sampling rates can be changed in Audacity, by changing the "project rate".
################################################################################
def combine_wav_files(out_file, *files):
    with wave.open(out_file, 'wb') as out:
        with wave.open(files[0], 'rb') as first_in:
            (nchannels, sampwidth, framerate, nframes, comptype, compname) =\
                first_in.getparams()
            out.setparams(first_in.getparams())
        for filename in files:
            with wave.open(filename, 'rb') as cur_in:
                if (cur_in.getnchannels() != nchannels or
                    cur_in.getsampwidth() != sampwidth or
                    cur_in.getframerate() != framerate or
                    cur_in.getcomptype() != comptype or
                    cur_in.getcompname() != compname):
                    raise Exception('Mismatched file parameters: ' + filename)
                out.writeframes(cur_in.readframes(cur_in.getnframes()))

################################################################################
# Module cleanup.
# This should be called when the module is no longer needed.
################################################################################
def cleanup():
    # Terminate PyAudio.
    PYAUDIO.terminate()
#########################################################################