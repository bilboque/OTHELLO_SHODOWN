VALID_PLAYER_TYPES = ["BOT", "HUMAN"]
VALID_EVAL_TYPES = ["RANDOM", "SCORE", "WEIGHTS"]

# Select the player 1 and 2 type.
# if the player is of type "BOT"
# you also have to configure a bot strength in {1,...,5}
# and the eval function to use
PLAYER_1_TYPE = "BOT"
PLAYER_1_STRENGTH = 5
PLAYER_1_EVAL = "WEIGHTS"

PLAYER_2_TYPE = "HUMAN"
PLAYER_2_STRENGTH = 5
PLAYER_2_EVAL = "WEIGHTS"


# True if you want to visualise the game with pygames
# Needs to be true if at least one player is set to HUMAN
VISIBLE_BOARD = True
