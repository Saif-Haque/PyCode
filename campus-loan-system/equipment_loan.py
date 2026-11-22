import json
import os

# Named constants for configuration (satisfies "no unexplained magic values")
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipment.json")
REQUIRED_EMAIL_DOMAIN = "@bournemouth.ac.uk"


def load_equipment(filename=DATA_FILE):
    """Load equipment dictionary from a JSON file."""
    if not os.path.exists(filename):
        print(f"Error: Data file '{filename}' not found.")
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON.")
        return {}


def save_equipment(equipment, filename=DATA_FILE):
    """Save the current equipment dictionary back to the JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(equipment, file, indent=2)
    print("Changes saved successfully.")


def view_equipment(equipment):
    """Display all equipment items in a clean, readable table."""
    print("\n" + "-" * 72)
    print(f"{'ID':<8} {'Description':<20} {'Category':<15} {'Avail':<8} {'Loaned':<8}")
    print("-" * 72)
    for eq_id, details in equipment.items():
        print(
            f"{eq_id:<8} "
            f"{details['description']:<20} "
            f"{details['category']:<15} "
            f"{details['available_quantity']:<8} "
            f"{details['loaned_quantity']:<8}"
        )
    print("-" * 72)


def search_equipment(equipment):
    query: str = input("\nEnter ID, description, or category to search: ").strip().lower()

    if query == "":
        print("Search cannot be empty.")
        return

    # Step 2: Create the empty dictionary BEFORE the loop!
    matches = {}
    for eq_id, details in equipment.items():
        id_lower = eq_id.lower()
        desc_lower = details["description"].lower()
        cat_lower = details["category"].lower()

        if (query in id_lower) or (query in desc_lower) or (query in cat_lower):
            matches[eq_id] = details

    # Step 3: Check matches AFTER the loop finishes
    if len(matches) > 0:
        print(f"\nFound {len(matches)} matching item(s):")
        view_equipment(matches)  # Use display_equipment_table(matches) only if you created that function
    else:
        print(f"No equipment found matching '{query}'.")


  print(f"Loan recorded: {quantity} unit(s) of {details['description']} for {borrower}.")

def borrow_equipment(equipment):
    """Allow a student with a valid Bournemouth email to borrow an available item."""
    eq_id = input("\nEnter equipment ID to borrow (e.g., E001): ").strip().upper()

    # Check 1: Does this ID exist in our dictionary?
    if eq_id not in equipment:
        print(f"Error: Equipment ID '{eq_id}' not found.")
        return

    item = equipment[eq_id]

    # Check 2: Is at least 1 unit available to borrow?
    if item["available_quantity"] <= 0:
        print(f"Sorry, '{item['description']}' ({eq_id}) is currently out of stock.")
        return

    print(f"Selected: {item['description']} (Available: {item['available_quantity']})")
# Check 3: Validate the student's Bournemouth email address
    email = input(f"Enter borrower email ({REQUIRED_EMAIL_DOMAIN}): ").strip().lower()

    if not email.endswith(REQUIRED_EMAIL_DOMAIN) or email == REQUIRED_EMAIL_DOMAIN:
        print(f"Error: Email must be a valid '{REQUIRED_EMAIL_DOMAIN}' address.")
        return

    # Step 4: Update quantities and borrower list in memory
    item["available_quantity"] -= 1
    item["loaned_quantity"] += 1
    item["borrowers"].append(email)

    print(f"Success! {item['description']} ({eq_id}) loaned to {email}.")
def return_equipment(equipment):
    """Allow a borrower to return a loaned equipment item."""
    # Ask for the equipment ID and standardize it (remove spaces, make uppercase)
    eq_id = input("\nEnter equipment ID to return (e.g., E001): ").strip().upper()

    # Check 1: Does this ID exist in our equipment dictionary?
    if eq_id not in equipment:
        print(f"Error: Equipment ID '{eq_id}' not found.")
        return

    # Create a shortcut reference to this specific item's inner dictionary
    item = equipment[eq_id]

    # Check 2: Are any units of this item currently on loan?
    if item["loaned_quantity"] <= 0:
        print(f"Error: '{item['description']}' ({eq_id}) has no active loans to return.")
        return

    # Check 3: Ask for the borrower's email and validate its domain format
    email = input(f"Enter borrower email ({REQUIRED_EMAIL_DOMAIN}): ").strip().lower()

    if not email.endswith(REQUIRED_EMAIL_DOMAIN) or email == REQUIRED_EMAIL_DOMAIN:
        print(f"Error: Email must be a valid '{REQUIRED_EMAIL_DOMAIN}' address.")
        return

    # Check 4: Verify this email is actually on this item's borrower list
    if email not in item["borrowers"]:
        print(f"Error: No active loan found for '{email}' on {item['description']} ({eq_id}).")
        return

    # Step 5: Update quantities and remove one instance of the borrower's email in memory
    item["available_quantity"] += 1
    item["loaned_quantity"] -= 1
    item["borrowers"].remove(email)  # Removes only the first matching email in the list

    print(f"Success! {item['description']} ({eq_id}) returned by {email}.")
    
def view_current_loans(equipment):
    """Display all equipment items that currently have active borrowers."""
    print("\nCURRENT ACTIVE LOANS")
    print("-" * 72)

    # Keep a running count of individual loans displayed so we know if none exist
    loan_count = 0

    # Loop through every item in the equipment dictionary (eq_id is e.g. 'E001',
    # and details is the inner dictionary containing description, quantities, and borrowers)
    for eq_id, details in equipment.items():

        # Only display items that currently have at least 1 unit loaned out
        if details["loaned_quantity"] > 0:
            print(f"{eq_id} - {details['description']} (Loaned: {details['loaned_quantity']})")

            # Loop through the list of borrower email strings for this item
            for borrower in details["borrowers"]:
                print(f"  - {borrower}")
                loan_count += 1  # Add 1 to our total active loan counter

    # If the loop finished and loan_count is still 0, nothing is currently borrowed
    if loan_count == 0:
        print("No active loans.")

    print("-" * 72)

def main():
    """Main application loop and user menu interaction."""
    equipment = load_equipment()
    if not equipment:
        return

    while True:
        print("\nCAMPUS EQUIPMENT LOAN SYSTEM\n")
        print("1. View equipment")
        print("2. Search equipment")
        print("3. Borrow equipment")
        print("4. Return equipment")
        print("5. View current loans")
        print("6. Save and exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            view_equipment(equipment)
        elif choice == "2":
            search_equipment(equipment)
        elif choice == "3":
            borrow_equipment(equipment)
        elif choice == "4":
            return_equipment(equipment)
        elif choice == "5":
            view_current_loans(equipment)
        elif choice == "6":
            save_equipment(equipment)
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()