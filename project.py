import os
import csv
import shutil
import datetime
import logging

DATA_FILE = "transactions.csv"
BACKUP_FOLDER = "backups"
LOG_FILE = "financial_assistant.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_data_file():
    """Initialize the data file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category", "Amount", "Type"])
        logging.info("Data file initialized successfully.")

def backup_data():
    """Backup the data file."""
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    backup_file = os.path.join(BACKUP_FOLDER, f"transactions_backup_{datetime.datetime.now():%Y%m%d%H%M%S}.csv")
    shutil.copy(DATA_FILE, backup_file)
    logging.info(f"Data backed up successfully to {backup_file}")
    print("Data backed up successfully.")

def recover_data():
    """Recover data from a backup file."""
    if not os.path.exists(BACKUP_FOLDER):
        print("Backup folder does not exist. No backup files found.")
        return

    backup_files = os.listdir(BACKUP_FOLDER)
    if backup_files:
        backup_files.sort()
        print("Available backup files:")
        for i, backup_file in enumerate(backup_files):
            print(f"{i+1}. {backup_file}")
        choice = input("Enter the number of the backup file to recover: ")
        try:
            backup_index = int(choice) - 1
            if 0 <= backup_index < len(backup_files):
                backup_file = os.path.join(BACKUP_FOLDER, backup_files[backup_index])
                shutil.copy(backup_file, DATA_FILE)
                logging.info(f"Data recovered successfully from {backup_file}")
                print("Data recovered successfully.")
            else:
                print("Invalid backup file choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("No backup files found.")


def add_transaction():
    """Add a transaction to the data file."""
    transaction_type = input("Enter transaction type (Income/Expense): ").capitalize()
    if transaction_type not in ["Income", "Expense"]:
        print("Invalid transaction type. Please enter either 'Income' or 'Expense'.")
        return

    date = input("Enter transaction date (YYYY-MM-DD): ")
    description = input("Enter transaction description: ")
    category = input("Enter transaction category: ")
    amount = input("Enter transaction amount: ")

    try:
        amount = float(amount)
        if transaction_type == "Expense":
            amount *= -1

        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, description, category, amount, transaction_type])
        logging.info(f"Transaction added successfully: {date}, {description}, {category}, {amount}, {transaction_type}")
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")

def view_transactions():
    """View all transactions stored in the data file."""
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")

def edit_transaction():
    """Edit a transaction in the data file."""
    try:
        # Read the CSV file to get the current transactions
        with open(DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            transactions = list(reader)

        # Display the current transactions with IDs
        print("Current Transactions:")
        for i, transaction in enumerate(transactions[1:], start=1):  # Skip the header
            print(f"{i}. {transaction}")

        transaction_id = int(input("Enter the ID of the transaction you want to edit: "))
        if transaction_id < 1 or transaction_id >= len(transactions):
            print("Invalid transaction ID.")
            return

        # Get the transaction to edit
        transaction_to_edit = transactions[transaction_id]

        # Ask the user for the new details of the transaction
        date = input(f"Enter new date for transaction {transaction_id} (YYYY-MM-DD): ")
        description = input(f"Enter new description for transaction {transaction_id}: ")
        category = input(f"Enter new category for transaction {transaction_id}: ")
        amount = float(input(f"Enter new amount for transaction {transaction_id}: "))
        transaction_type = input(f"Enter new type for transaction {transaction_id} (Income/Expense): ").capitalize()
        if transaction_type not in ["Income", "Expense"]:
            raise ValueError("Invalid transaction type. Please enter either 'Income' or 'Expense'.")

        if transaction_type == "Expense":
            amount *= -1

        # Update the transaction
        transactions[transaction_id] = [date, description, category, amount, transaction_type]

        # Write the updated transactions back to the CSV file
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transactions)

        print("Transaction updated successfully.")
        logging.info(f"Transaction {transaction_id} updated successfully.")

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"Error editing transaction: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during transaction edit: {e}")

def categorize_transactions(category_mapping, transaction_type):
    """Categorize transactions based on predefined mappings."""
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            transactions = list(reader)

        for transaction in transactions:
            if transaction['Type'].lower() == transaction_type.lower():
                for category, keywords in category_mapping.items():
                    if any(keyword in transaction['Description'].lower() for keyword in keywords):
                        transaction['Category'] = category
                        break
                else:
                    transaction['Category'] = "Other"

        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Description", "Category", "Amount", "Type"])
            writer.writeheader()
            writer.writerows(transactions)

        logging.info(f"{transaction_type.capitalize()}s categorized successfully.")
        print(f"{transaction_type.capitalize()}s categorized successfully.")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during {transaction_type} categorization: {e}")
def search_transactions():
    """Search for transactions containing a specific keyword."""
    try:
        search_term = input("Enter search term: ").lower()
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if search_term in str(row).lower():
                    print(row)
                    found = True
            if not found:
                print("No transactions found matching the search term.")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during transaction search: {e}")

def generate_report():
    """Generate a financial report based on transactions."""
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            total_income = 0
            total_expense = 0
            for row in reader:
                amount = float(row['Amount'])
                if amount > 0:
                    total_income += amount
                else:
                    total_expense += amount

        print(f"Total Income: {total_income}")
        print(f"Total Expense: {total_expense}")
        print(f"Net Income: {total_income + total_expense}")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during report generation: {e}")

def analyze_report():
    """Analyze transactions for generating reports."""
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            category_totals = {}
            for row in reader:
                category = row['Category']
                amount = float(row['Amount'])
                if category not in category_totals:
                    category_totals[category] = 0
                category_totals[category] += amount

        print("Analysis of Report:")
        for category, total in category_totals.items():
            print(f"{category}: {total}")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during report analysis: {e}")

def manage_debt():
    """Calculate and manage total debt."""
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            total_debt = 0
            for row in reader:
                amount = float(row['Amount'])
                if amount < 0:
                    total_debt += amount

        print(f"Total debt: {total_debt}")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during debt management: {e}")

def retirement_planning():
    """Plan for retirement based on user inputs."""
    try:
        current_age = int(input("Enter your current age: "))
        retirement_age = int(input("Enter your planned retirement age: "))
        monthly_expenses = float(input("Enter your estimated monthly expenses during retirement: "))
        life_expectancy = int(input("Enter your life expectancy: "))

        years_to_retirement = retirement_age - current_age
        total_months_in_retirement = (life_expectancy - retirement_age) * 12
        total_savings_needed = total_months_in_retirement * monthly_expenses

        print(f"To retire comfortably at age {retirement_age}, you need to save ${total_savings_needed:,.2f} in total, assuming a life expectancy of {life_expectancy}.")
    except ValueError as e:
        print("Invalid input. Please enter valid numeric values.")
        logging.error(f"Invalid input during retirement planning: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during retirement planning: {e}")

def track_insurance():
    """Track insurance policy details."""
    try:
        insurance_provider = input("Enter your insurance provider: ")
        policy_type = input("Enter the type of insurance policy: ")
        premium_amount = float(input("Enter the premium amount: "))
        policy_start_date = input("Enter the policy start date (YYYY-MM-DD): ")

        print("Insurance policy details:")
        print(f"Provider: {insurance_provider}")
        print(f"Policy Type: {policy_type}")
        print(f"Premium Amount: ${premium_amount:.2f}")
        print(f"Start Date: {policy_start_date}")
    except ValueError as e:
        print("Invalid input. Please enter a valid numeric value for the premium amount.")
        logging.error(f"Invalid input during insurance tracking: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during insurance tracking: {e}")

def track_credit_score():
    """Track and evaluate the user's credit score."""
    try:
        credit_score = int(input("Enter your credit score: "))
        if credit_score >= 800:
            print("Excellent credit score! You qualify for the best interest rates.")
        elif 740 <= credit_score < 800:
            print("Very good credit score. You'll likely qualify for good interest rates.")
        elif 670 <= credit_score < 740:
            print("Fair credit score. You may qualify for decent interest rates.")
        elif 580 <= credit_score < 670:
            print("Poor credit score. You may have difficulty qualifying for loans or credit cards.")
        else:
            print("Very poor credit score. You may need to work on improving your credit history.")
    except ValueError as e:
        print("Invalid input. Please enter a valid numeric credit score.")
        logging.error(f"Invalid input during credit score tracking: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during credit score tracking: {e}")

def delete_transaction():
    """Delete a transaction from the data file."""
    try:
        transaction_id = int(input("Enter the ID of the transaction you want to delete: "))
        with open(DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            transactions = list(reader)

        if transaction_id < 1 or transaction_id > len(transactions):
            print("Invalid transaction ID.")
            return

        del transactions[transaction_id]

        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transactions)

        print("Transaction deleted successfully.")
        logging.info(f"Transaction {transaction_id} deleted successfully.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during transaction deletion: {e}")

def delete_category():
    """Delete a category from the data file."""
    try:
        category_to_delete = input("Enter the name of the category you want to delete: ")
        updated_transactions = []

        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Category'] != category_to_delete:
                    updated_transactions.append(row)

        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_transactions)

        print(f"Category '{category_to_delete}' and all associated transactions have been deleted.")
        logging.info(f"Category '{category_to_delete}' and all associated transactions have been deleted.")
    except FileNotFoundError:
        print("Data file not found.")
        logging.error("Data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error occurred during category deletion: {e}")

def main():
    """Main function to run the program."""
    print("Welcome to the Financial Assistant!")
    print("Developed by Arefeayinie Asrat.")
    initialize_data_file()
    while True:
        print("\n1. Manage Transactions")
        print("2. Generate Reports")
        print("3. Financial Planning")
        print("4. Data Management")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            manage_transactions_menu()
        elif choice == "2":
            generate_reports_menu()
        elif choice == "3":
            financial_planning_menu()
        elif choice == "4":
            data_management_menu()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
def manage_transactions_menu():
    """Manage transactions menu."""
    while True:
        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            edit_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def generate_reports_menu():
    """Generate reports menu."""
    while True:
        print("\n1. Generate Report")
        print("2. Analyze Report")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_report()
        elif choice == "2":
            analyze_report()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def financial_planning_menu():
    """Financial planning menu."""
    while True:
        print("\n1. Manage Debt")
        print("2. Retirement Planning")
        print("3. Track Insurance")
        print("4. Track Credit Score")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            manage_debt()
        elif choice == "2":
            retirement_planning()
        elif choice == "3":
            track_insurance()
        elif choice == "4":
            track_credit_score()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def data_management_menu():
    """Data management menu."""
    while True:
        print("\n1. Backup Data")
        print("2. Recover Data")
        print("3. Delete Category")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            backup_data()
        elif choice == "2":
            recover_data()
        elif choice == "3":
            delete_category()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
