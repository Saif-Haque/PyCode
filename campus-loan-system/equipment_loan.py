import json
import os

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================
# Build the full file path to 'equipment.json' in the same folder as this script
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipment.json")

# Only emails ending with this domain are allowed to borrow or return equipment
REQUIRED_EMAIL_DOMAIN = "@bournemouth.ac.uk"

# Standard width for table divider lines
TABLE_WIDTH = 72


# ============================================================================
# FILE PERSISTENCE FUNCTIONS (LOAD & SAVE)
# ============================================================================
def load_equipment(filename=DATA_FILE):
    """Load the equipment dictionary from the JSON file into memory."""
    # Check if the JSON file exists before trying to open it
    if not os.path.exists(filename):
        print(f"Error: Data file '{filename}' not found.")
        return {}

    try:
        # Open the file in read mode ('r') using UTF-8 text encoding
        with open(filename, "r", encoding="utf-8") as file:
            # Convert the JSON text into a Python dictionary and return it
            return json.load(file)
    except json.JSONDecodeError:
        # Catch formatting mistakes inside the JSON file so the program doesn't crash
        print(f"Error: '{filename}' contains invalid JSON.")
        return {}


def save_equipment(equipment, filename=DATA_FILE):
    """Save the current in-memory equipment dictionary back to the JSON file."""
    # Open the file in write mode ('w'), replacing old contents with updated data
    with open(filename, "w", encoding="utf-8") as file:
        # Convert the Python dictionary back into formatted JSON (indent=2 makes it readable)
        json.dump(equipment, file, indent=2)

    print("Changes saved successfully.")


# ============================================================================
# DISPLAY & SEARCH FUNCTIONS
# ============================================================================
def view_equipment(equipment):
    """Display all equipment items in a clean, aligned table."""
    print("\n" + "-" * TABLE_WIDTH)
    # Print column headers using fixed character widths (<8, <20, etc.) for neat alignment
    print(f"{'ID':<8} {'Description':<20} {'Category':<15} {'Avail':<8} {'Loaned':<8}")
    print("-" * TABLE_WIDTH)

    # Loop through each equipment ID (key) and its inner details dictionary (value)
    for eq_id, details in equipment.items():
        print(
            f"{eq_id:<8} "
            f"{details['description']:<20} "
            f"{details['category']:<15} "
            f"{details['available_quantity']:<8} "
            f"{details['loaned_quantity']:<8}"
        )

    print("-" * TABLE_WIDTH)


def search_equipment(equipment):
    """Search for equipment by partial match on ID, description, or category."""
    # Step 1: Ask for a search term and normalize it (remove spaces, make lowercase)
    query = input("\nEnter ID, description, or category to search: ").strip().lower()

    # Guard clause: Stop early if the user pressed Enter without typing anything
    if query == "":
        print("Search cannot be empty.")
        return

    # Step 2: Create an empty dictionary to store any items that match the search
    matches = {}

    # Loop through every item in the equipment dictionary
    for eq_id, details in equipment.items():
        # Convert searchable fields to lowercase so matching is case-insensitive
        id_lower = eq_id.lower()
        desc_lower = details["description"].lower()
        cat_lower = details["category"].lower()

        # Check if the search term appears anywhere inside the ID, description, or category
        if (query in id_lower) or (query in desc_lower) or (query in cat_lower):
            matches[eq_id] = details  # Add matching item to the results dictionary

    # Step 3: Display the results after the loop finishes checking all items
    if len(matches) > 0:
        print(f"\nFound {len(matches)} matching item(s):")
        # Reuse view_equipment() to print the matching subset in the same table format
        view_equipment(matches)
    else:
        print(f"No equipment found matching '{query}'.")


# ============================================================================
# LOAN & RETURN TRANSACTION FUNCTIONS
# ============================================================================
def borrow_equipment(equipment):
    """Allow a student with a valid Bournemouth email to borrow an available item."""
    # Ask for the equipment ID and standardize it (remove spaces, make uppercase)
    eq_id = input("\nEnter equipment ID to borrow (e.g., E001): ").strip().upper()

    # Check 1: Does this ID exist in our equipment dictionary?
    if eq_id not in equipment:
        print(f"Error: Equipment ID '{eq_id}' not found.")
        return

    # Create a shortcut reference pointing directly to this item's inner dictionary
    item = equipment[eq_id]

    # Check 2: Is at least 1 unit available to borrow?
    if item["available_quantity"] <= 0:
        print(f"Sorry, '{item['description']}' ({eq_id}) is currently out of stock.")
        return

    print(f"Selected: {item['description']} (Available: {item['available_quantity']})")

    # Check 3: Ask for the borrower's email and validate its university domain
    email = input(f"Enter borrower email ({REQUIRED_EMAIL_DOMAIN}): ").strip().lower()

    # Reject emails that don't end with '@bournemouth.ac.uk' or have nothing before the '@'
    if not email.endswith(REQUIRED_EMAIL_DOMAIN) or email == REQUIRED_EMAIL_DOMAIN:
        print(f"Error: Email must be a valid '{REQUIRED_EMAIL_DOMAIN}' address.")
        return

    # Step 4: Update stock quantities and append the email to the borrowers list in memory
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

    # Create a shortcut reference pointing directly to this item's inner dictionary
    item = equipment[eq_id]

    # Check 2: Are any units of this item currently on loan?
    if item["loaned_quantity"] <= 0:
        print(f"Error: '{item['description']}' ({eq_id}) has no active loans to return.")
        return

    # Check 3: Ask for the borrower's email and validate its university domain
    email = input(f"Enter borrower email ({REQUIRED_EMAIL_DOMAIN}): ").strip().lower()

    # Reject emails that don't end with '@bournemouth.ac.uk' or have nothing before the '@'
    if not email.endswith(REQUIRED_EMAIL_DOMAIN) or email == REQUIRED_EMAIL_DOMAIN:
        print(f"Error: Email must be a valid '{REQUIRED_EMAIL_DOMAIN}' address.")
        return

    # Check 4: Verify this email is actually recorded in this item's borrowers list
    if email not in item["borrowers"]:
        print(f"Error: No active loan found for '{email}' on {item['description']} ({eq_id}).")
        return

    # Step 5: Update stock quantities and remove one matching email from the borrowers list
    item["available_quantity"] += 1
    item["loaned_quantity"] -= 1
    item["borrowers"].remove(email)  # Removes only the first matching instance in the list

    print(f"Success! {item['description']} ({eq_id}) returned by {email}.")


def view_current_loans(equipment):
    """Display all equipment items that currently have active borrowers."""
    print("\nCURRENT ACTIVE LOANS")
    print("-" * TABLE_WIDTH)

    # Keep a running count of individual loans displayed so we know if none exist
    loan_count = 0

    # Outer loop: Check each equipment item in the dictionary
    for eq_id, details in equipment.items():
        # Only display items that currently have at least 1 unit loaned out
        if details["loaned_quantity"] > 0:
            print(f"{eq_id} - {details['description']} (Loaned: {details['loaned_quantity']})")

            # Inner loop: Print each borrower email stored in this item's list
            for borrower in details["borrowers"]:
                print(f"  - {borrower}")
                loan_count += 1  # Increment total active loan counter

    # If the loop finished and loan_count is still 0, nothing is currently borrowed
    if loan_count == 0:
        print("No active loans.")

    print("-" * TABLE_WIDTH)


# ============================================================================
# MAIN MENU LOOP
# ============================================================================
def main():
    """Run the main menu loop and route user selections to the appropriate functions."""
    # Load initial equipment records from disk into memory once at startup
    equipment = load_equipment()

    # Exit immediately if the data file could not be loaded
    if not equipment:
        return

    # Keep displaying the menu until the user selects Option 6 to save and exit
    while True:
        print("\nCAMPUS EQUIPMENT LOAN SYSTEM\n")
        print("1. View equipment")
        print("2. Search equipment")
        print("3. Borrow equipment")
        print("4. Return equipment")
        print("5. View current loans")
        print("6. Save and exit")

        # Read the user's menu choice and strip any accidental spaces
        choice = input("\nSelect an option: ").strip()

        # Route the choice to the matching function
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
            # Save all in-memory changes to equipment.json before breaking out of the loop
            save_equipment(equipment)
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 6.")


# Standard Python entry point: only run main() when this script is executed directly
if __name__ == "__main__":
    main()