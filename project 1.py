"""
Expense Tracker
Author: [Your Name]
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
 