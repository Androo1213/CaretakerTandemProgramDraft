import arrow
import logging

# Set up logging
logger = logging.getLogger(__name__)


def parse_bolus_history(data):
    """
    Parses bolus data and returns more readable string
    """
    try:
        parsed_data = []
        for entry in data:
            parsed_entry = {
                "timestamp": arrow.get(entry["timestamp"]).format('YYYY-MM-DD HH:mm:ss'),
                "bolus_amount": entry["bolusAmount"],
                "carb_amount": entry["carbAmount"],
                "bolus_type": entry.get("bolusType", "Standard"),
            }
            parsed_data.append(parsed_entry)
        return parsed_data
    except Exception as e:
        logger.error(f"Error parsing bolus history data: {e}")
        return []


def parse_iob_data(data):
    """
    Parses the IOB data from the API response returns more readable string
    """
    try:
        parsed_data = []
        for entry in data:
            parsed_entry = {
                "timestamp": arrow.get(entry["timestamp"]).format('YYYY-MM-DD HH:mm:ss'),
                "iob": entry["iob"],
                "active_insulin": entry.get("activeInsulin", 0),
            }
            parsed_data.append(parsed_entry)
        return parsed_data
    except Exception as e:
        logger.error(f"Error parsing IOB data: {e}")
        return []


def format_bolus_history(bolus_history):
    """
    Makes bolus history more readable
    returns formatted string
    """
    formatted_data = "Bolus History:\n"
    for entry in bolus_history:
        formatted_data += f"Date: {entry['timestamp']}, Bolus Amount: {entry['bolus_amount']} units, "
        formatted_data += f"Carbs: {entry['carb_amount']} grams, Type: {entry['bolus_type']}\n"
    return formatted_data


def format_iob_data(iob_data):
    """Also makes IOB data more readable"""
    formatted_data = "IOB Data:\n"
    for entry in iob_data:
        formatted_data += f"Date: {entry['timestamp']}, IOB: {entry['iob']} units, "
        formatted_data += f"Active Insulin: {entry['active_insulin']} units\n"
    return formatted_data
