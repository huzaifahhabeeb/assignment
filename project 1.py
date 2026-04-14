"""
Expense Tracker
Author: Huzaifah Habeeb
Description: A command-line expense tracker that lets users add, view,
             edit and delete expenses. Data is saved to a CSV file so
             it persists between sessions.
 
AI Usage Notes:
used AI to give an idea of how to structure the code and to generate some of the functions.
"""

import csv
import os
from datetime import date

# ─── Constants ────────────────────────────────────────────────────────────────

FILE_NAME = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Other"]

# ─── File Handling ────────────────────────────────────────────────────────────
 
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
 
 # ─── Input Validation Helpers ─────────────────────────────────────────────────
 
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
 