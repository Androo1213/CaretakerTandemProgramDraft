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
    """ makes timestamp readable
    """
    try:
        return arrow.get(timestamp).format('YYYY-MM-DD HH:mm:ss')
    except Exception as e:
        logging.error(f"Error formatting timestamp: {e}")
        return str(timestamp)

def validate_required_fields(data, required_fields):
    """
    returns bool regarding if all data fields that are required are filled
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.error(f"Missing required fields: {missing_fields}")
        return False
    return True

def parse_date(date_string):
    """
    makes date string into date obj
    """
    try:
        return arrow.get(date_string).datetime
    except Exception as e:
        logging.error(f"Error parsing date: {e}")
        return None

def cap_length(text, maxlen):
    """
    perhaps will need to truncate text later
    """
    if not text or len(text) <= maxlen:
        return text
    return f'{text[:maxlen//2]}...{text[-maxlen//2:]}'
