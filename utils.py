import logging
import arrow
from datetime import datetime

# Set up logging
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def format_timestamp(timestamp):
    """
    Converts a timestamp to a human-readable format.
    """
    try:
        return arrow.get(timestamp).format('YYYY-MM-DD HH:mm:ss')
    except Exception as e:
        logging.error(f"Error formatting timestamp: {e}")
        return str(timestamp)

def validate_required_fields(data, required_fields):
    """
    Ensures that all required fields are present in the data.
    :param data: Dictionary containing the data.
    :param required_fields: List of required field names.
    :return: True if all fields are present, False otherwise.
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.error(f"Missing required fields: {missing_fields}")
        return False
    return True

def parse_date(date_string):
    """
    Parses a date string into a datetime object.
    :param date_string: Date string to parse.
    :return: datetime object or None if parsing fails.
    """
    try:
        return arrow.get(date_string).datetime
    except Exception as e:
        logging.error(f"Error parsing date: {e}")
        return None

def cap_length(text, maxlen):
    """
    Truncates a string to a maximum length, adding ellipsis if necessary.
    :param text: The string to truncate.
    :param maxlen: Maximum length of the string.
    :return: Truncated string.
    """
    if not text or len(text) <= maxlen:
        return text
    return f'{text[:maxlen//2]}...{text[-maxlen//2:]}'
