"""
Contact Book CLI
- Store contacts in a list of dictionaries
- Features:
  * Add new contact
  * View all contacts
  * Search by name (case-insensitive, partial match)
  * Delete contact (by index or by exact name)
- Optional persistence to a JSON file (contacts.json) so contacts survive between runs

Run with: python contact_book_cli.py
"""

import json
import os
from typing import List, Dict

DATA_FILE = "contacts.json"


def load_contacts() -> List[Dict]:
    """Load contacts from DATA_FILE if it exists, otherwise return an empty list."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            print("Warning: Failed to load contacts file. Starting with an empty list.")
    return []


def save_contacts(contacts: List[Dict]):
    """Save contacts to DATA_FILE in JSON format."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving contacts: {e}")


def add_contact(contacts: List[Dict]):
    name = input("Enter full name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Enter phone number (optional): ").strip()
    email = input("Enter email (optional): ").strip()
    address = input("Enter address (optional): ").strip()

    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }

    contacts.append(contact)
    save_contacts(contacts)
    print(f"Contact '{name}' added.")


def view_contacts(contacts: List[Dict]):
    if not contacts:
        print("No contacts found.")
        return

    print("\nAll contacts:")
    for idx, c in enumerate(contacts, start=1):
        print(f"[{idx}] {c.get('name')} | Phone: {c.get('phone','-')} | Email: {c.get('email','-')} | Address: {c.get('address','-')}")
    print()


def search_contacts(contacts: List[Dict]):
    query = input("Search by name (partial, case-insensitive): ").strip().lower()
    if not query:
        print("Empty search query.")
        return

    results = [ (i,c) for i,c in enumerate(contacts, start=1) if query in c.get('name','').lower() ]
    if not results:
        print("No matching contacts found.")
        return

    print(f"\nFound {len(results)} matching contact(s):")
    for idx, c in results:
        print(f"[{idx}] {c.get('name')} | Phone: {c.get('phone','-')} | Email: {c.get('email','-')} | Address: {c.get('address','-')}")
    print()


def delete_contact(contacts: List[Dict]):
    if not contacts:
        print("No contacts to delete.")
        return

    view_contacts(contacts)
    choice = input("Delete by (i)ndex or (n)ame? (i/n): ").strip().lower()
    if choice == 'i':
        try:
            idx = int(input("Enter index to delete: ").strip())
            if 1 <= idx <= len(contacts):
                removed = contacts.pop(idx - 1)
                save_contacts(contacts)
                print(f"Removed contact: {removed.get('name')}")
            else:
                print("Index out of range.")
        except ValueError:
            print("Invalid index.")
    elif choice == 'n':
        name = input("Enter exact name to delete: ").strip().lower()
        matched = [c for c in contacts if c.get('name','').lower() == name]
        if not matched:
            print("No contact with that exact name found.")
            return
        if len(matched) == 1:
            contacts.remove(matched[0])
            save_contacts(contacts)
            print(f"Removed contact: {matched[0].get('name')}")
        else:
            print(f"Found {len(matched)} contacts with that name. Please delete by index instead.")
    else:
        print("Unknown option. Cancelled.")


def main():
    contacts = load_contacts()

    MENU = """
Contact Book - Choose an option:
1. Add new contact
2. View all contacts
3. Search by name
4. Delete contact
5. Exit
"""

    while True:
        print(MENU)
        choice = input("Enter choice (1-5): ").strip()
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            search_contacts(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == '__main__':
    main()
