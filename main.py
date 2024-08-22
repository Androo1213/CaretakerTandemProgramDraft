import logging
import sys
import arrow
from api import TConnectApi
from parser import format_bolus_history, format_iob_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("Welcome to the Caretaker Tandem Program!")

    email = input("Please enter your t:connect email: ")
    password = input("Please enter your t:connect password: ")

    try:
        tconnect_api = TConnectApi(email, password)
    except Exception as e:
        logger.error(f"Failed to authenticate with t:connect: {e}")
        sys.exit(1)

    while True:
        print("\nPlease choose the type of data you want to retrieve:")
        print("1. Bolus History")
        print("2. IOB Data")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            try:
                bolus_history = tconnect_api.get_bolus_history(start_date, end_date)
                formatted_data = format_bolus_history(bolus_history)
                print(formatted_data)
            except Exception as e:
                logger.error(f"Failed to retrieve bolus history: {e}")

        elif choice == '2':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            try:
                iob_data = tconnect_api.get_iob_data(start_date, end_date)
                formatted_data = format_iob_data(iob_data)
                print(formatted_data)
            except Exception as e:
                logger.error(f"Failed to retrieve IOB data: {e}")

        elif choice == '3':
            print("Exiting the program. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
