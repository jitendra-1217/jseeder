# Logger util
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="\n%(levelname)s - [%(asctime)s] %(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)
