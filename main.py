# Handle the main flow of the program

import pandas as pd #allow to load csv file
import csv 
from datetime import datetime 
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMS = ["Date", "Amount", "Category", "Description"]
    FORMAT= "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
           
            df = pd.DataFrame(columns=cls.COLUMS) #Data Frame: Object that allows access different rows/columns from a csv file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        #with: context manager, automatically closes the file
        with open(cls.CSV_FILE, "a", newline="") as csvfile: #a: append, add in the end of the file
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMS)
            writer.writerow(new_entry)
        print ("Entry added successfully")
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT) #converted str to datetime object
        start_date = datetime.strptime(start_date, CSV.FORMAT) 
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date) #use & instead of and when working with pandas dataframes or mask
        filtered_df = df.loc[mask] # locates and returns new filtered dataframe
         
        if filtered_df.empty:
            print("No transactions found for the given date range")
        else: 
            print (
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(  
                  filtered_df.to_string(
                      index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                      )
                  )
            total_income = filtered_df[filtered_df["Category"] == "Income"] ["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"] ["Amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print (f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df  
    
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (dd-mm-yyyy) or enter for today's date:", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('Date', inplace=True) #index is the way wich we locate and manipulate rows
    
    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    
    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs Expense")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
def main():
    while True:
        print ("\n1.Add a new transaction")
        print ("2.View transactions and summary within range")
        print ("3.Exit")
        choice = input("Enter your choice(1-3): ")
        
        if choice=="1":
            add()
        elif choice=="2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input ("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice=="3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()