"""
Expense Tracker
Description: A command-line expense tracker that lets users add, view,
             edit and delete expenses. Data is saved to a CSV file so
             it persists between sessions.
 
AI Usage and other Notes:
used AI to give an idea of how to structure the code and to generate some of the functions.
used triple quotes, like i am right now, to write docstrings for each function, which explain what they do and how they work. This is to make the code easier to understand and maintain.
i also added comments throughout the code to explain specific lines or blocks, especially where the AI-generated code might be doing something non-obvious. This way, if someone else (or future me) looks at this code later, they can quickly understand the logic without having to decipher it from scratch.
there's also a comment at the top of each major section (like "File Handling" and "Core CRUD Functions") to break it up and make it easier to navigate.
"""

# importing necessary libraries for file handling and date management
import csv
import os
from datetime import date

# Constants

FILE_NAME = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Other"]

# File Handling
 
def load_expenses():
    """
    Read expenses from the CSV file and return them as a list of dicts.
    If the file doesn't exist yet, return an empty list.
    AI-assisted
    """
    expenses = []
 
    if not os.path.exists(FILE_NAME):
        return expenses  # Checks if file exists, pevents error if it doesn't
 
    with open(FILE_NAME, newline="") as file: # opens the CSV file safely. The with keyword automatically closes the file when done, even if something goes wrong
        reader = csv.DictReader(file) # reads each row of the CSV as a dictionary, so you can access values by name like row["amount"] instead of by position
        for row in reader:
            # Convert amount back to float (CSV stores everything as strings)
            row["amount"] = float(row["amount"])
            expenses.append(row) # adds each row into the list
 
    return expenses
 
 
def save_expenses(expenses):
    """
    Write the full expenses list to the CSV file.
    Called after every change so data is never lost.
    """
    # AI-assisted: Claude suggested using DictWriter for clean CSV output
    fieldnames = ["id", "description", "amount", "category", "date"] # defines the column names for the CSV
 
    with open(FILE_NAME, "w", newline="") as file: # opens the file in write mode. The "w" means it overwrites whatever was there before
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # writes the column names as the first row
        writer.writerows(expenses) # writes every expense in the list as a row
 
 # Input Validation Helpers
 
def get_valid_amount(prompt):
    """
    Keep asking the user for a number until they enter a valid positive float.
    AI-assisted: Claude suggested the try/except structure.
    I added the negative number check myself.
    """
    while True: # loops forever until we deliberately break out of it with return
        user_input = input(prompt).strip() # removes any accidental spaces the user might have typed
        try: # this is error handling. You "try" to convert the input to a float. If it fails (e.g. the user typed "abc"), Python throws a ValueError and instead of crashing, the except block catches it and prints a helpful message
            amount = float(user_input)
            if amount <= 0:
                print("  Amount must be greater than zero. Try again.")
            else:
                return amount
        except ValueError:
            print("  Invalid input — please enter a number (e.g. 12.50).")
 
 
def get_valid_category():
    """
    Show the category list and return the user's valid choice.
    Uses a simple numbered menu with an if/else guard.
    AI-assisted
    """
    print("\n  Categories:") # new line 
    for i, cat in enumerate(CATEGORIES, start=1): # loops through the list and gives each item a number starting at 1. So i is the number, cat is the category name
        print(f"    {i}. {cat}") # The f"..." strings are f-strings — they let you put variables directly inside {}
 
    while True:
        choice = input("  Choose a category (1-6): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES): #  checks if what they typed is actually a number before trying to use it as one. Prevents crashes
            return CATEGORIES[int(choice) - 1] #  the -1 is because lists in Python start at index 0, but our menu starts at 1. So if the user picks 1, we want index 0
        else:
            print("  Please enter a number between 1 and 6.")
 
 
def generate_id(expenses):
    """
    Generate the next unique ID based on the current list.
    If the list is empty, start at 1.
    AI-assisted
    """
    if not expenses: # if the list is empty, just return "1" as the first ID
        return "1"
    max_id = max(int(e["id"]) for e in expenses) # loops through all expenses, converts their IDs to integers, and finds the highest one
    return str(max_id + 1) # adds 1 to the highest ID and converts it back to a string (because the CSV stores everything as text)

# Core CRUD Functions
 
def add_expense(expenses):
    """CREATE — Add a new expense to the list and save to file.
    AI-assisted"""
    print("\n── Add Expense ──────────────────────")
 
    description = input("  Description: ").strip()
    if not description: # catches empty input. If the user just pressed Enter without typing anything, we stop here
        print("  Description cannot be empty. Returning to menu.")
        return
 
    amount = get_valid_amount("  Amount (£): ")
    category = get_valid_category()
    today = date.today().strftime("%Y-%m-%d") # gets today's date and formats it as "2025-01-14"
 
    new_expense = { # builds a dictionary with all the expense details
        "id": generate_id(expenses),
        "description": description,
        "amount": amount,
        "category": category,
        "date": today
    }
 
    expenses.append(new_expense) #  adds it to the list in memory
    save_expenses(expenses) # immediately writes it to the CSV so it's not lost
    print(f"\n  ✓ Expense added: {description} — £{amount:.2f} ({category})")
 
 
def view_expenses(expenses):
    """READ — Display all expenses in a formatted table.
    AI-assisted"""
    print("\n── All Expenses ─────────────────────")
 
    if not expenses: # nothing to show, so exit early
        print("  No expenses recorded yet.")
        return
 
    # Print header row
    print(f"  {'ID':<5} {'Description':<20} {'Amount':>8}  {'Category':<15} {'Date'}") # The f"..." strings are f-strings — they let you put variables directly inside {}. The :<5 and :>8 parts control the spacing and alignment so the columns line up neatly
    print("  " + "-" * 62)
 
    for e in expenses:
        print(f"  {e['id']:<5} {e['description']:<20} £{e['amount']:>7.2f}  {e['category']:<15} {e['date']}") # the .2f means show exactly 2 decimal places
 
    # Show running total at the bottom
    calculate_total(expenses)
 
 
def edit_expense(expenses):
    """UPDATE — Find an expense by ID and let the user change its fields.
    AI-assisted"""
    print("\n── Edit Expense ─────────────────────")
 
    if not expenses:
        print("  No expenses to edit.")
        return
 
    view_expenses(expenses)
    expense_id = input("\n  Enter the ID of the expense to edit: ").strip()
 
    # Find the expense with a matching ID It loops through all expenses comparing IDs until it finds a match
    target = None
    for e in expenses:
        if e["id"] == expense_id:
            target = e
            break
 
    if target is None:
        print("  No expense found with that ID.")
        return
 
    print(f"\n  Editing: {target['description']} — £{target['amount']:.2f}") # Because target points directly to the expense inside the expenses list, changing target["description"] changes it in the list too — no need to find it again
    print("  (Press Enter to keep the current value)\n") # For each field, it only updates if the user actually typed something — if they just pressed Enter, the original value is kept
 
    # Only update fields the user provides input for
    new_desc = input(f"  New description [{target['description']}]: ").strip()
    if new_desc:
        target["description"] = new_desc
 
    change_amount = input(f"  Change amount? Current: £{target['amount']:.2f} (y/n): ").strip().lower() # .lower() converts whatever they type to lowercase, so "Y", "y" and "YES" would all work for the first letter check
    if change_amount == "y":
        target["amount"] = get_valid_amount("  New amount (£): ")
 
    change_cat = input(f"  Change category? Current: {target['category']} (y/n): ").strip().lower()
    if change_cat == "y":
        target["category"] = get_valid_category()
 
    save_expenses(expenses)
    print("\n  ✓ Expense updated.")
 
 
def delete_expense(expenses):
    """DELETE — Remove an expense by ID after confirmation.
    AI-assisted"""
    print("\n── Delete Expense ───────────────────")
 
    if not expenses:
        print("  No expenses to delete.")
        return
 
    view_expenses(expenses)
    expense_id = input("\n  Enter the ID of the expense to delete: ").strip()
 
    # Search for the expense
    target = None
    for e in expenses:
        if e["id"] == expense_id:
            target = e
            break
 
    if target is None:
        print("  No expense found with that ID.")
        return
 
    # Confirm before deleting
    confirm = input(f"  Delete '{target['description']}' (£{target['amount']:.2f})? (y/n): ").strip().lower()
 
    if confirm == "y":
        expenses.remove(target) # removes that specific dictionary object from the list
        save_expenses(expenses)
        print("  ✓ Expense deleted.")
    else:
        print("  Deletion cancelled.")
 
 # Utility Functions
 
def calculate_total(expenses):
    """
    Add up all expense amounts and print the total.
    Also shows a breakdown by category.
    AI-assisted
    """
    if not expenses:
        return
 
    total = sum(e["amount"] for e in expenses) #  loops through every expense and adds up all the amounts in one line
    print(f"\n  {'Total:':<25} £{total:.2f}")
 
    # Category breakdown using a dictionary
    breakdown = {} # an empty dictionary that will store category totals
    for e in expenses:
        cat = e["category"]
        if cat not in breakdown: #  if we haven't seen this category before, create it with a starting value of 0
            breakdown[cat] = 0
        breakdown[cat] += e["amount"] # add the amount to that category's running total
 
    print("\n  Breakdown by category:")
    for cat, subtotal in breakdown.items():
        print(f"    {cat:<20} £{subtotal:.2f}")
 
 
def display_menu():
    """Print the main menu options."""
    print("\n════════════════════════════════════")
    print("       EXPENSE TRACKER")
    print("════════════════════════════════════")
    print("  1. Add expense")
    print("  2. View all expenses")
    print("  3. Edit expense")
    print("  4. Delete expense")
    print("  5. View total & breakdown")
    print("  6. Exit")
    print("────────────────────────────────────")
 
 # Main Loop
 
def main():
    """
    Entry point. Loads existing data, then runs the menu loop
    until the user chooses to exit.
    AI-assisted
    """
    expenses = load_expenses() # runs once at the start to get saved data
    print(f"\n  Loaded {len(expenses)} expense(s) from file.")
 
    while True: # keeps the menu looping forever until the user picks 6 to exit
        display_menu()
        choice = input("  Choose an option (1-6): ").strip()
 
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("\n── Totals ───────────────────────────")
            calculate_total(expenses)
        elif choice == "6":
            print("\n  Goodbye. Your data has been saved.\n")
            break
        else:
            print("  Invalid option — please enter a number between 1 and 6.")
 
 
# Run the program
if __name__ == "__main__":
    main()