import arrow
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Parsing Functions

def parse_bolus_history(data):
    """
    Parses bolus data from api response
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
    Parses iob data from api response
    :param data:
    :return:
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

# Formatting Functions

def format_bolus_history(bolus_history):
    """
    Formats parsed bolus history data into a readable string.
    """
    formatted_data = "Bolus History:\n"
    for entry in bolus_history:
        formatted_data += f"Date: {entry['timestamp']}, Bolus Amount: {entry['bolus_amount']} units, "
        formatted_data += f"Carbs: {entry['carb_amount']} grams, Type: {entry['bolus_type']}\n"
    return formatted_data

def format_iob_data(iob_data):
    """
    formats parsed IOB data into a more readable str
    """
    formatted_data = "IOB Data:\n"
    for entry in iob_data:
        formatted_data += f"Date: {entry['timestamp']}, IOB: {entry['iob']} units, "
        formatted_data += f"Active Insulin: {entry['active_insulin']} units\n"
    return formatted_data

# Filtering and Processing Functions

def filter_data_by_date(data, start_date, end_date):
    start = arrow.get(start_date)
    end = arrow.get(end_date)
    return [entry for entry in data if start <= arrow.get(entry['timestamp']) <= end]

def convert_units(value, from_unit, to_unit):
    """
    unit conversion
    """
    conversions = {
        ('mg/dL', 'mmol/L'): 0.0555,
        ('mmol/L', 'mg/dL'): 18.0182,
    }
    try:
        return value * conversions[(from_unit, to_unit)]
    except KeyError:
        logger.error(f"Conversion from {from_unit} to {to_unit} is not supported.")
        return value

def process_bolus_history(data, start_date=None, end_date=None):
    """
    processes bolus history data
    """
    parsed_data = parse_bolus_history(data)
    if start_date and end_date:
        parsed_data = filter_data_by_date(parsed_data, start_date, end_date)
    return format_bolus_history(parsed_data)

def process_iob_data(data, start_date=None, end_date=None):
    """
    process iob data, can filter by date if needed
    """
    parsed_data = parse_iob_data(data)
    if start_date and end_date:
        parsed_data = filter_data_by_date(parsed_data, start_date, end_date)
    return format_iob_data(parsed_data)
