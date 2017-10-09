################################################################################
# menu.py
# A. Hornof - Sept 2017
#
# A sample program to show how to move through a list of sound objects with
# single keystrokes.
# 
# Edited by Alex Dibb - Oct 2017
#
################################################################################
__author__ = 'hornof'

# Package imports
import readchar
import time         # for time.sleep()

# Local imports
import sound        # sound.py accompanies this file

################################################################################
# main()
################################################################################
def main():
    create_sound_filenames()
    verify_sound_filenames()
    create_menu_globals()
    run_menu()

################################################################################
# Create the sound objects for the auditory menus and display.
################################################################################
def create_sound_filenames():

    # Declare global variables.
    global SET_DATE_AND_TIME_WAV, YOU_SELECTED_WAV, NUMBERS_WAV, AM_WAV,\
        PRESS_AGAIN_TO_QUIT_WAV, EXITING_PROGRAM_WAV,\
        EXITING_PROGRAM_WAV_DURATION, TMP_FILE_WAV

    # Create  sounds.
    nav_path = "wav_files_provided/miscellaneous_f/"
    num_path = "wav_files_provided/numbers_f/"
    SET_DATE_AND_TIME_WAV = nav_path + "Set_date_and_time_f.wav"
    YOU_SELECTED_WAV = nav_path + "you_selected_f.wav"
    NUMBERS_WAV = [num_path + "28_f.wav", num_path + "29_f.wav",
           num_path + "30_f.wav", num_path + "31_f.wav"]
    AM_WAV = nav_path + "AM_f.wav"
    PRESS_AGAIN_TO_QUIT_WAV = nav_path + "Press_again_to_quit_f.wav"
    EXITING_PROGRAM_WAV = nav_path + "Exiting_program_f.wav"
    EXITING_PROGRAM_WAV_DURATION = 1.09 # in s. 1.09 is accurate but 0.45 saves time.

    TMP_FILE_WAV = "tmp_file_p782s8u.wav" # Random filename  for output

################################################################################
# Verify all files can be loaded and played.
# Play all sound files to make sure the paths and filenames are correct and valid.
# The very last sound tested/played should be the sound that plays at startup.
################################################################################
def verify_sound_filenames():
    sound.Play(PRESS_AGAIN_TO_QUIT_WAV)
    sound.Play(EXITING_PROGRAM_WAV)
    sound.Play(YOU_SELECTED_WAV)
    sound.Play(NUMBERS_WAV[0])
    sound.Play(NUMBERS_WAV[1])
    sound.Play(NUMBERS_WAV[2])
    sound.Play(NUMBERS_WAV[3])
    sound.Play(AM_WAV)
    sound.Play(SET_DATE_AND_TIME_WAV)

################################################################################
# Create some global constants and variables for the menu.
################################################################################
def create_menu_globals():

    # Declare global variables as such.
    global CONTINUE_KEY, FORWARD_KEY, BACKWARD_KEY, UNDO_KEY, QUIT_KEY,\
        MINIMAL_HELP_STRING, CURRENT_TIME

    # Constants
    # Keystrokes for the keyboard interaction.
    CONTINUE_KEY = '\x20' # space bar
    FORWARD_KEY = 'j'
    BACKWARD_KEY = 'k'
    UNDO_KEY = 'l'
    QUIT_KEY = ';'

    # A bare minimum of text to display to guide the user.
    MINIMAL_HELP_STRING = "Press '" + FORWARD_KEY + "' and '" + BACKWARD_KEY \
        + "' to go forward and back.\n" \
        + "Press '" + CONTINUE_KEY + "' and '" + UNDO_KEY \
        + "' to go continue and undo.\n" \
        + "Press '" + QUIT_KEY + "' to quit."

    # Global variables
    CURRENT_TIME = 0    # The current time that is set. (Just an integer for now.)


################################################################################
# Run the menu in an endless loop until the user exits.
################################################################################
def run_menu():

    global CURRENT_TIME

    # Provide a minimal indication that the program has started.
    print(MINIMAL_HELP_STRING)

    # Get the first keystroke.
    c = readchar.readchar()

    # Endless loop responding to the user's last keystroke.
    # The loop breaks when the user hits the QUIT_MENU_KEY.
    while True:

        # Respond to the user's input.
        if c == FORWARD_KEY:

            # Advance the time, looping back around to the start.
            CURRENT_TIME += 1
            if CURRENT_TIME == len(NUMBERS_WAV):
                CURRENT_TIME = 0

            # Concatenate three audio files to generate the message.
            sound.combine_wav_files(TMP_FILE_WAV, 
                                    NUMBERS_WAV[CURRENT_TIME], AM_WAV)

            # Play the concatenated file.
            sound.Play(TMP_FILE_WAV)

        if c == BACKWARD_KEY:

            # Reduce the time, looping forward around to the end.
            CURRENT_TIME -= 1
            if CURRENT_TIME < 0:
                CURRENT_TIME = len(NUMBERS_WAV) - 1

            # Concatenate three audio files to generate the message.
            sound.combine_wav_files(TMP_FILE_WAV,
                                    NUMBERS_WAV[CURRENT_TIME], AM_WAV)

            # Play the concatenated file.
            sound.Play(TMP_FILE_WAV)

        # User quits.
        if c == QUIT_KEY:

            # Notify the user that another QUIT_MENU_KEY will quit the program.
            sound.Play(PRESS_AGAIN_TO_QUIT_WAV)

            # Get the user's next keystroke.
            c = readchar.readchar()

            # If the user pressed QUIT_MENU_KEY, quit the program.
            if c == QUIT_KEY:
                sound.Play(EXITING_PROGRAM_WAV)
                # A delay is needed so the sound gets played before quitting.
                time.sleep(EXITING_PROGRAM_WAV_DURATION)
                sound.cleanup()
                # Quit the program
                break

        # The user presses a key that will have no effect.
        else:
            # Get the user's next keystroke.
            c = readchar.readchar()

################################################################################
main()
################################################################################
