
from src.utils import logger

# To catch mysql warnings
import MySQLdb, warnings
warnings.filterwarnings('error', category=MySQLdb.Warning)


def tryCatchWrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Warning as w:
            logger.warning(str(w), exc_info=True)
        except Exception as e:
            logger.error(str(e), exc_info=True)
    return wrapper
