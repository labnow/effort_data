import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('default.log')

# Configure level and formatter and add it to handlers
stream_handler.setLevel(logging.DEBUG) # warning and above is logged to the stream
file_handler.setLevel(logging.DEBUG) # error and above is logged to a file

stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
# logger.addHandler(stream_handler) # std_out not required
logger.addHandler(file_handler)
