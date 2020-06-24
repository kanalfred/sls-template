import logging
import os

# logger = logging.getLogger('curiosity-honesty')
logger = logging.getLogger(os.environ.get('LOG_NAME'))
logger.addHandler(logging.NullHandler())
logger.setLevel(getattr(logging, os.environ.get('LOG_LEVEL', 'ERROR').upper(), None))
