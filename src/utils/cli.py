# Cli utils

import sys, getopt

from src.utils import logger


# Prints help
def getCliHelpText():

    helpText = """
        Help:

        - Run using `python src/run.py -i <Absolute input file path>`
        - Run tests using `python tests/__init__.py`
        - Ref to following url on writing input config file:
          https://github.com/jitendra-1217/jseeder/blob/master/src/configs/input/sample.yaml

        *Readme to be added..
        """

    return helpText


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
