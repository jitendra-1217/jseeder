
import sys, yaml, json

from src.utils import logger

# Parses given yaml file
def parseYamlFile(absoluteFilePath):

    with open(absoluteFilePath) as f:
        try:
            inputConfig = yaml.load(f)
        except yaml.YAMLError as e:
            logger.error(str(e))
            sys.exit(1)

    logger.debug("Parsed config:\n{}".format(json.dumps(inputConfig, indent=4, sort_keys=True)))

    return inputConfig
