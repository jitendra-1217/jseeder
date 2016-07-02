# Cli utils

import sys, getopt

from src.utils import logger


# Prints help
def getCliHelpText():
    return "This should print help on console!"


# Parses cli options
def parseOptions(argv):

    # Intialize defaults
    inputFile = "/home/vagrant/jseeder/src/configs/input/sample.yaml"

    try:
        options, args = getopt.getopt(argv, "hi:", ["inputFile="])
    except getopt.GetoptError as e:
        logger.error(str(e))
        sys.exit(1)

    for option, arg in options:
        if option == "-h":
            print(getCliHelpText())
            sys.exit()
        elif option in ("-i", "--inputFile"):
            inputFile = arg

    logger.debug("Input file: {}".format(inputFile))

    return (inputFile)
