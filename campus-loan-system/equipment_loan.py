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


# def borrow_equipment(equipment):
#     """Validate and process an equipment loan."""
#     if not equipment:
#         print("No equipment is available.")
#         return

#     eq_id = input("\nEnter equipment ID: ").strip()
#     if eq_id not in equipment:
#         print(f"Equipment ID '{eq_id}' was not found.")
#         return

#     details = equipment[eq_id]
#     available = details["available_quantity"]
#     if available <= 0:
#         print("This equipment is currently unavailable.")
#         return

#     borrower = input("Enter borrower Bournemouth email: ").strip().lower()
#     if REQUIRED_EMAIL_DOMAIN not in borrower:
#         print(f"Invalid email. The email must use {REQUIRED_EMAIL_DOMAIN}.")
#         return

#     try:
#         quantity = int(input("Enter quantity to borrow: ").strip())
#     except ValueError:
#         print("Quantity must be a whole number.")
#         return

#     if quantity <= 0:
#         print("Quantity must be greater than zero.")
#         return
#     if quantity > available:
#         print(f"Only {available} unit(s) are available.")
#         return

#     details["available_quantity"] -= quantity
#     details["loaned_quantity"] += quantity

#     active_loans = details.setdefault("active_loans", [])
#     matching_loan = next(
#         (loan for loan in active_loans if loan.get("email") == borrower),
#         None,
#     )
#     if matching_loan:
#         matching_loan["quantity"] += quantity
#     else:
#         active_loans.append({"email": borrower, "quantity": quantity})

#     print(f"Loan recorded: {quantity} unit(s) of {details['description']} for {borrower}.")

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

def return_equipment(equipment):
    """Validate and process an equipment return."""
    eq_id = input("\nEnter equipment ID: ").strip()
    if eq_id not in equipment:
        print(f"Equipment ID '{eq_id}' was not found.")
        return

    details = equipment[eq_id]
    borrower = input("Enter borrower Bournemouth email: ").strip().lower()
    active_loans = details.setdefault("active_loans", [])
    matching_loan = next(
        (loan for loan in active_loans if loan.get("email") == borrower),
        None,
    )

    if not matching_loan:
        print(f"No active loan for '{borrower}' was found on this item.")
        return

    try:
        quantity = int(input("Enter quantity to return: ").strip())
    except ValueError:
        print("Quantity must be a whole number.")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return
    if quantity > matching_loan["quantity"]:
        print(f"This borrower currently has {matching_loan['quantity']} unit(s) on loan.")
        return

    matching_loan["quantity"] -= quantity
    if matching_loan["quantity"] == 0:
        active_loans.remove(matching_loan)

    details["available_quantity"] += quantity
    details["loaned_quantity"] = max(0, details["loaned_quantity"] - quantity)
    print(f"Return recorded: {quantity} unit(s) of {details['description']}.")


def view_current_loans(equipment):
    """Display all items that currently have active borrowers."""
    print("\nCURRENT ACTIVE LOANS")
    print("-" * 72)

    loan_count = 0
    for eq_id, details in equipment.items():
        active_loans = details.get("active_loans", [])
        if not active_loans:
            continue

        print(f"{eq_id} - {details['description']}")
        for loan in active_loans:
            if loan.get("quantity", 0) > 0:
                print(f"  {loan['email']:<35} Quantity: {loan['quantity']}")
                loan_count += 1

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