# Speeded-Inference-Game

Code to run the Speeded Inference Game (short SIG), here presented as Evaluation Edition.

Necessary modules for PsychoPy3 (running with Python 3) are configparser, numpy and imutils.

Start SIG from 'main' script. Enter participant ID at the beginning of the script (logfiles will be saved with this extension).

Setting file should be updated before running. Below is an explanation of each variable:

[General]

picture_size = 135 (displayed size of the targets) 
highscore = 3973 (score in points, will be displayed in all breaks) 
timeout = 2 (time in sec, after which timeout occurs and trial is stopped at the beginning of the game) 
evaluation_time = 4 (time in sec, after which evaluation screen is closed when participant is not responding) 
block_number = 14 (amount of blocks for experiment) 
input_keys = y, x, n, m (identification of four response buttons to chose targets) 
color_scheme = 1 (should be a number between 1 and 4 for four different colour-category mixtures of the targets)

[Block]

decrease_timeout = 0.8 (percentage of past accuracy - if accuracy of the last 1/2 block is higher than this number, the threshold for the timeout will be decreased/ shortened to induce more temporal pressure) 
increase_timeout = 0.6 (percentage of past accuracy - if accuracy of the last 1/2 block is lower than this number, the threshold for the timeout will be increased/ prolonged to reduce the temporal pressure) 
pause = 5 (time in sec, after which participant can freely decide to continue with next block) 
main_length = 28 (number of trials used in each block during the real experiment) 
tryout_length = 8 (number of trials used in each block during both training blocks) 
congruent_number = 4 (number of trials applying rule 1, which are used during both training blocks) 
congruent_number_main = 14 (number of trials applying rule 1, which are used during the real experiment)