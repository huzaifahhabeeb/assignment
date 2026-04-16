"""
Expense Tracker
Description: A command-line expense tracker that lets users add, view,
             edit and delete expenses. Data is saved to a CSV file so
             it persists between sessions.
 
AI Usage Notes:
used AI to give an idea of how to structure the code and to generate some of the functions.
"""

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
    """
    expenses = []
 
    if not os.path.exists(FILE_NAME):
        return expenses  # No file yet — first run
 
    with open(FILE_NAME, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert amount back to float (CSV stores everything as strings)
            row["amount"] = float(row["amount"])
            expenses.append(row)
 
    return expenses
 
 
def save_expenses(expenses):
    """
    Write the full expenses list to the CSV file.
    Called after every change so data is never lost.
    """
    # AI-assisted: Claude suggested using DictWriter for clean CSV output
    fieldnames = ["id", "description", "amount", "category", "date"]
 
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)
 
 # Input Validation Helpers
 
def get_valid_amount(prompt):
    """
    Keep asking the user for a number until they enter a valid positive float.
    AI-assisted: Claude suggested the try/except structure.
    I added the negative number check myself.
    """
    while True:
        user_input = input(prompt).strip()
        try:
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
    """
    print("\n  Categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"    {i}. {cat}")
 
    while True:
        choice = input("  Choose a category (1-6): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        else:
            print("  Please enter a number between 1 and 6.")
 
 
def generate_id(expenses):
    """
    Generate the next unique ID based on the current list.
    If the list is empty, start at 1.
    """
    if not expenses:
        return "1"
    # Find the highest existing ID and add 1
    max_id = max(int(e["id"]) for e in expenses)
    return str(max_id + 1)

# Core CRUD Functions
 
def add_expense(expenses):
    """CREATE — Add a new expense to the list and save to file."""
    print("\n── Add Expense ──────────────────────")
 
    description = input("  Description: ").strip()
    if not description:
        print("  Description cannot be empty. Returning to menu.")
        return
 
    amount = get_valid_amount("  Amount (£): ")
    category = get_valid_category()
    today = date.today().strftime("%Y-%m-%d")
 
    new_expense = {
        "id": generate_id(expenses),
        "description": description,
        "amount": amount,
        "category": category,
        "date": today
    }
 
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"\n  ✓ Expense added: {description} — £{amount:.2f} ({category})")
 
 
def view_expenses(expenses):
    """READ — Display all expenses in a formatted table."""
    print("\n── All Expenses ─────────────────────")
 
    if not expenses:
        print("  No expenses recorded yet.")
        return
 
    # Print header row
    print(f"  {'ID':<5} {'Description':<20} {'Amount':>8}  {'Category':<15} {'Date'}")
    print("  " + "-" * 62)
 
    for e in expenses:
        print(f"  {e['id']:<5} {e['description']:<20} £{e['amount']:>7.2f}  {e['category']:<15} {e['date']}")
 
    # Show running total at the bottom
    calculate_total(expenses)
 
 
def edit_expense(expenses):
    """UPDATE — Find an expense by ID and let the user change its fields."""
    print("\n── Edit Expense ─────────────────────")
 
    if not expenses:
        print("  No expenses to edit.")
        return
 
    view_expenses(expenses)
    expense_id = input("\n  Enter the ID of the expense to edit: ").strip()
 
    # Find the expense with a matching ID
    target = None
    for e in expenses:
        if e["id"] == expense_id:
            target = e
            break
 
    if target is None:
        print("  No expense found with that ID.")
        return
 
    print(f"\n  Editing: {target['description']} — £{target['amount']:.2f}")
    print("  (Press Enter to keep the current value)\n")
 
    # Only update fields the user provides input for
    new_desc = input(f"  New description [{target['description']}]: ").strip()
    if new_desc:
        target["description"] = new_desc
 
    change_amount = input(f"  Change amount? Current: £{target['amount']:.2f} (y/n): ").strip().lower()
    if change_amount == "y":
        target["amount"] = get_valid_amount("  New amount (£): ")
 
    change_cat = input(f"  Change category? Current: {target['category']} (y/n): ").strip().lower()
    if change_cat == "y":
        target["category"] = get_valid_category()
 
    save_expenses(expenses)
    print("\n  ✓ Expense updated.")
 
 
def delete_expense(expenses):
    """DELETE — Remove an expense by ID after confirmation."""
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
        expenses.remove(target)
        save_expenses(expenses)
        print("  ✓ Expense deleted.")
    else:
        print("  Deletion cancelled.")
 
 # Utility Functions
 
def calculate_total(expenses):
    """
    Add up all expense amounts and print the total.
    Also shows a breakdown by category.
    """
    if not expenses:
        return
 
    total = sum(e["amount"] for e in expenses)
    print(f"\n  {'Total:':<25} £{total:.2f}")
 
    # Category breakdown using a dictionary
    breakdown = {}
    for e in expenses:
        cat = e["category"]
        if cat not in breakdown:
            breakdown[cat] = 0
        breakdown[cat] += e["amount"]
 
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
    """
    expenses = load_expenses()
    print(f"\n  Loaded {len(expenses)} expense(s) from file.")
 
    while True:
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