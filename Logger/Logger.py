  ###
    #
    #    ######  #####  #####  #####  #  ##
    #    #    #  #   #  #   #  #   #  ###
    #    #    #  #   #  #   #  #####  #
    #    #    #  #####  #####  #      #
  #####  ######      #      #  #####  #
                 #   #  #   #
                 #####  #####

# Simple logger module ~ SigmaOne ~ 2018

import time

def log(msg, level=0):
  """
  Writes logs to the terminal
  Params:
    - msg (string): the message to write
    - level (int):  the level of the log Entry
        - 0: information, normal functionality (green)
        - 1: warning, unexpected behaviour, but not enough to cause problems (yellow)
        - 2: error, unexpected behaviour, usually enough to halt the program (red)
  """

  if level == 0:
    log_type = "\033[92m [INFO]\033[0m: "
  elif level == 1:
    log_type = "\033[93m [WARN]\033[0m: "
  elif level == 2:
    log_type = "\033[91m [ERR]\033[0m: "

  print(time.strftime("<%d.%m.%Y - %H:%M:%S>") + log_type + msg)
