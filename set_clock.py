################################################################################
# set_clock.py
# A. Hornof - Sept 2017
# Edited by Alex Dibb - Oct 2017
# 
# A simple program to select a time through audio queues and the right-hand
# home keys.
#
# DEVNOTE: Should probably be reworked. I'm not very happy with how it came 
# out, especially regarding the abuse of globals. 
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
    global SET_DATE_AND_TIME_WAV, YOU_SELECTED_WAV, NUMBERS_WAV, WEEKDAYS_WAV,\
        PRESS_AGAIN_TO_QUIT_WAV, EXITING_PROGRAM_WAV, SET_DAY_OF_WEEK_WAV, \
        SET_HOUR_WAV, SET_MINUTES_WAV, EXITING_PROGRAM_WAV_DURATION, \
        OH_WAV, O_CLOCK_WAV, TMP_FILE_WAV
    # DEVNOTE: Holy globals, Batman! 

    # Create  sounds.
    nav_path = "wav_files_provided/miscellaneous_f/"
    num_path = "wav_files_provided/numbers_f/"
    day_path = "wav_files_provided/days_of_week_f/"
    SET_DATE_AND_TIME_WAV = nav_path + "Set_date_and_time_f.wav"
    YOU_SELECTED_WAV = nav_path + "you_selected_f.wav"

    # Create list of number sounds
    NUMBERS_WAV = []
    for x in range(60):
        if x < 10:
            end_path = "0" + str(x) + "_f.wav"
        else:
            end_path = str(x) + "_f.wav"
        NUMBERS_WAV.append(num_path + end_path)

    # Create list of weekday sounds
    WEEKDAYS_WAV = [day_path] * 7
    WEEKDAYS_WAV[0] += "saturday_f.wav"   # Explicit ordering 
    WEEKDAYS_WAV[1] += "sunday_f.wav"     # DEVNOTE: Likely a better way. Look 
    WEEKDAYS_WAV[2] += "monday_f.wav"     # into later. List comprehension?
    WEEKDAYS_WAV[3] += "tuesday_f.wav"
    WEEKDAYS_WAV[4] += "wednesday_f.wav"
    WEEKDAYS_WAV[5] += "thursday_f.wav"
    WEEKDAYS_WAV[6] += "friday_f.wav"

    SET_DAY_OF_WEEK_WAV = nav_path + "Set_day_of_week_f.wav"
    SET_HOUR_WAV = nav_path + "Set_hour_f.wav"
    SET_MINUTES_WAV = nav_path + "Set_minutes_f.wav"
    OH_WAV = num_path + "oh_f.wav"
    O_CLOCK_WAV = nav_path + "o_clock_f.wav"
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
    for x in range(60):
        sound.Play(NUMBERS_WAV[x])
    for x in range(7):
        sound.Play(WEEKDAYS_WAV[x])
    sound.Play(SET_DAY_OF_WEEK_WAV)
    sound.Play(SET_HOUR_WAV)
    sound.Play(SET_MINUTES_WAV)
    sound.Play(OH_WAV)
    sound.Play(O_CLOCK_WAV)
    sound.Play(SET_DATE_AND_TIME_WAV)

    # First sound we want is a concatenation
    sound.combine_wav_files(TMP_FILE_WAV,
            SET_DATE_AND_TIME_WAV,
            SET_DAY_OF_WEEK_WAV,
            WEEKDAYS_WAV[0])
    sound.Play(TMP_FILE_WAV)

################################################################################
# Create some global constants and variables for the menu.
################################################################################
def create_menu_globals():

    # Declare global variables as such.
    global CONTINUE_KEY, ADD_KEY, SUB_KEY, UNDO_KEY, QUIT_KEY,\
        MINIMAL_HELP_STRING, TIME_VAL

    # Constants
    # Keystrokes for the keyboard interaction.
    CONTINUE_KEY = '\x20' # space bar
    ADD_KEY = 'j'
    SUB_KEY = 'k'
    UNDO_KEY = 'l'
    QUIT_KEY = ';'

    # A bare minimum of text to display to guide the user.
    MINIMAL_HELP_STRING = "Press '" + ADD_KEY + "' and '" + SUB_KEY \
        + "' to add and subtract.\n" \
        + "Press '" + CONTINUE_KEY + "' and '" + UNDO_KEY \
        + "' to continue and undo.\n" \
        + "Press '" + QUIT_KEY + "' to quit."
    # DEVNOTE: Tone this down. There's no actual display; try to put together an
    # audio prompt instead.
    # DEVNOTE: Mic is being obtuse. Can't get acceptable sound quality. I'll try 
    # again later, but I don't think it's going to happen. Just use the text for 
    # now and consider it a script for later.

    # Global variables
    TIME_VAL = [0] * 3     # The selected times for day, hour, and minutes.
    TIME_VAL[1] = 15       # Start hours in evening to show 24-hour clock


################################################################################
# Run the menu in an endless loop until the user exits.
################################################################################
def run_menu():

    global TIME_VAL

    CURRENT_VAL = 0    # Current value of time frame being set
    CURRENT_STAGE = 0   # Current time frame being set: 1=Day, 2=Hour, 3=Minute


    # Provide a minimal indication that the program has started.
    print(MINIMAL_HELP_STRING)

    # Get the first keystroke.
    c = readchar.readchar()

    # Endless loop responding to the user's last keystroke.
    # The loop breaks when the user hits the QUIT_MENU_KEY.
    while True:

        # Respond to the user's input.
        if c == ADD_KEY:

            # Loop over the right list
            WAV_LOOP = WEEKDAYS_WAV if CURRENT_STAGE == 0 else NUMBERS_WAV

            # Limit possible numbers for hour stage
            MAX = 24 if CURRENT_STAGE == 1 else len(WAV_LOOP)

            # Advance the time, looping back around to the start.
            CURRENT_VAL += 1
            if CURRENT_VAL == MAX:
                CURRENT_VAL = 0

            # Play the concatenated file.
            sound.Play(WAV_LOOP[CURRENT_VAL])

        if c == SUB_KEY:

            # Loop over the right list
            WAV_LOOP = WEEKDAYS_WAV if CURRENT_STAGE == 0 else NUMBERS_WAV

            # Limit possible numbers for hour stage
            MAX = 23 if CURRENT_STAGE == 1 else len(WAV_LOOP) - 1

            # Reduce the time, looping forward around to the end.
            CURRENT_VAL -= 1
            if CURRENT_VAL < 0:
                CURRENT_VAL = MAX

            # Play the concatenated file.
            sound.Play(WAV_LOOP[CURRENT_VAL])

        if c == CONTINUE_KEY:

            # Set the time frame and move on to the next one.
            if CURRENT_STAGE < len(TIME_VAL):
                TIME_VAL[CURRENT_STAGE] = CURRENT_VAL
                CURRENT_STAGE += 1
                CURRENT_VAL = 0 if CURRENT_STAGE == len(TIME_VAL) \
                                else TIME_VAL[CURRENT_STAGE]
                # DEVNOTE: How the hell is one supposed to format a multiline 
                # ternary operator? It's definitely not this.
                introduce_stage(CURRENT_STAGE)

            if CURRENT_STAGE >= len(TIME_VAL):
                # Program is concluded - build result feedback
                RESULT = [ YOU_SELECTED_WAV, WEEKDAYS_WAV[TIME_VAL[0]] ]
                
                if TIME_VAL[1] == 0:
                    RESULT.append(OH_WAV)
                else: 
                    RESULT.append(NUMBERS_WAV[TIME_VAL[1]])

                if TIME_VAL[2] == 0:
                    RESULT.append(O_CLOCK_WAV)
                elif 1 <= TIME_VAL[2] and TIME_VAL[2] <= 9:
                    RESULT.append(OH_WAV)
                    RESULT.append(NUMBERS_WAV[TIME_VAL[2]]) 
                else:
                    RESULT.append(NUMBERS_WAV[TIME_VAL[2]]) 
                
                RESULT.append(EXITING_PROGRAM_WAV)

                sound.combine_wav_files(TMP_FILE_WAV, *RESULT)

                sound.Play(TMP_FILE_WAV)
                time.sleep(5)
                # Quit the program
                break

        if c == UNDO_KEY:

            # Revert the time frame
            if CURRENT_STAGE > 0:
                CURRENT_STAGE -= 1
                CURRENT_VAL = TIME_VAL[CURRENT_STAGE]
                introduce_stage(CURRENT_STAGE)

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
# Helper function to introduce the given stage.
################################################################################
def introduce_stage(stage):
    if stage == 0:
        # Stage is 'Set Day of Week'
        sound.combine_wav_files(TMP_FILE_WAV,
            SET_DATE_AND_TIME_WAV,
            SET_DAY_OF_WEEK_WAV,
            WEEKDAYS_WAV[TIME_VAL[0]])
    elif stage == 1:
        # Stage is 'Set Hour'
        sound.combine_wav_files(TMP_FILE_WAV,
            SET_HOUR_WAV,
            NUMBERS_WAV[TIME_VAL[1]])
    elif stage == 2:
        # Stage is 'Set Minute'
        sound.combine_wav_files(TMP_FILE_WAV,
            SET_MINUTES_WAV,
            NUMBERS_WAV[TIME_VAL[2]])
    sound.Play(TMP_FILE_WAV)

################################################################################
main()
################################################################################
