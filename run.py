import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('cred.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('gas_station_analysis')

customers = SHEET.worksheet('customers')

data = customers.get_all_values()

print(data)


def get_customers_data():
    """
    Get customers data from the user
    """
    print("Please enter customer data from the previous entries")
    print("Data must be five numbers, separated by commas.")
    print("Example: 1,200,300,400,500 \n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

    cust_data = data_str.split(",")
    validate_data(cust_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if the string cannot be converted into int,
    or if there aren't exactly 5 values.
    """
    print(values)
    try: 
        [int(value) for value in values]
        if len(values) != 5:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again \n")

get_customers_data()
