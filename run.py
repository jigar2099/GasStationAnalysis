import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import numpy as np
import termplotlib as tpl
import plotext as plt
from prettytable import PrettyTable

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
    while True:
        print("Please enter customer data from the previous entries")
        print("Data must be five numbers, separated by commas.")
        print("Example: 1,200,300,400 \n")

        data_str = input("Enter your data here: ")
        print(f"The customer data provided is {data_str}")


        cust_data = data_str.split(",")
        if validate_data(cust_data):
            print("Data is valid!")

        data_str1 = input("Enter your data here: ")
        print(f"The pt-ev data provided is {data_str1}")
        ptev_data = data_str1.split(",")
        if validate_data(ptev_data):
            print("Data is valid!")

        data_str2 = input("Enter your data here: ")
        print(f"The pt-ev data provided is {data_str2}")
        itev_data = data_str2.split(",")
        if validate_data(itev_data):
            print("Data is valid!")
            break
    return cust_data, ptev_data, itev_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if the string cannot be converted into int,
    or if there aren't exactly 4 values.
    """
    #print(values)
    try: 
        [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again \n")
        return False

    return True

def update_worksheet(data, sheet_name):
    """
    customer sheet update
    """
    print("Updateing customer worksheet...\n")
    cust_worksheet = SHEET.worksheet(sheet_name)
    cust_worksheet.append_row(data)
    print(f" {sheet_name} worksheet updated successfully...\n")

def calculate_non_ev(cust_row,ptev_row,itev_row):
    """
    Calculate number of non-ev customers
    """
    print("Updating non-ev customer sheet...\n")

    
    nev = [i-(j+k) for i,j,k in zip(cust_row,ptev_row,itev_row)]
    non_ev_sheet = SHEET.worksheet("non-ev")
    non_ev_sheet.append_row(nev)
    print("Non-ev worksheet updated successfully...")



def get_report():
    """
    Get statistical report of business.
    """
    print("Creating report... \n")
    unu = SHEET.worksheet("unused").get_all_values()
    cust = SHEET.worksheet("customers").get_all_values()
    pt_ev = SHEET.worksheet("public-transport-ev").get_all_values()
    it_ev = SHEET.worksheet("individual-transport-ev").get_all_values()
    non_ev = SHEET.worksheet(("non-ev")).get_all_values()
    
    cust_mat = np.array(cust)[1:].astype(int)
    ptev_mat = np.array(pt_ev)[1:].astype(int)
    itev_mat = np.array(it_ev)[1:].astype(int)
    nonev_mat = np.array(non_ev)[1:].astype(int)

    cust_avg = np.round(np.mean(cust_mat,axis=0), 2)
    ptev_avg = np.round(np.mean(ptev_mat,axis=0), 2)
    itev_avg = np.round(np.mean(itev_mat,axis=0), 2)
    nonev_avg = np.round(np.mean(nonev_mat,axis=0), 2)

    cust_std = np.round(np.std(cust_mat,axis=0),2)
    ptev_std = np.round(np.std(ptev_mat,axis=0),2)
    itev_std = np.round(np.std(itev_mat,axis=0),2)
    nonev_std = np.round(np.std(nonev_mat,axis=0),2)

    t = PrettyTable([' ', 'East', 'West', 'North', 'South'])
    t.add_row(['Customers', str(cust_avg[0])+'+/-'+str(cust_std[0]), str(cust_avg[1])+'+/-'+str(cust_std[1]), str(cust_avg[2])+'+/-'+str(cust_std[2]), str(cust_avg[3])+'+/-'+str(cust_std[3])])
    t.add_row(['PT-EV', str(ptev_avg[0])+'+/-'+str(ptev_std[0]), str(ptev_avg[1])+'+/-'+str(ptev_std[1]), str(ptev_avg[2])+'+/-'+str(ptev_std[2]), str(ptev_avg[3])+'+/-'+str(ptev_std[3])])
    t.add_row(['IT-EV', str(itev_avg[0])+'+/-'+str(itev_std[0]), str(itev_avg[1])+'+/-'+str(itev_std[1]), str(itev_avg[2])+'+/-'+str(itev_std[2]), str(itev_avg[3])+'+/-'+str(itev_std[3])])
    t.add_row(['NON-EV', str(nonev_avg[0])+'+/-'+str(nonev_std[0]), str(nonev_avg[1])+'+/-'+str(nonev_std[1]), str(nonev_avg[2])+'+/-'+str(nonev_std[2]), str(nonev_avg[3])+'+/-'+str(nonev_std[3])])

def main():
    """
    Run all program functions
    """
    cust, ptev, itev = get_customers_data()
    cust_data = [int(ct) for ct in cust]
    ptev_data = [int(pt) for pt in ptev]
    itev_data = [int(it) for it in itev]
    data = np.array([cust_data,ptev_data,itev_data])
    #print(data.shape)
    update_worksheet(cust_data, "customers")
    update_worksheet(ptev_data, "public-transport-ev")
    update_worksheet(itev_data, "individual-transport-ev")
    calculate_non_ev(cust_data, ptev_data, itev_data)
    get_report()

    #plt.plot(cust_data)
    #plt.plot(ptev_data)
    #plt.plot(itev_data)
    #plt.theme("matrix")
    #plt.colorize("red on green, italic",        "red",          "italic",    "green",         True)
    #plt.title("Scatter Plot")
    #plt.show()


main()