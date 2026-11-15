import json
import os

# Named constants for configuration (satisfies "no unexplained magic values")
DATA_FILE = "equipment.json"
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
    """Search items by ID, description, or category."""
    print("\n[TODO: Implement search logic]")


def borrow_equipment(equipment):
    """Validate and process an equipment loan."""
    print("\n[TODO: Implement borrow logic]")


def return_equipment(equipment):
    """Validate and process an equipment return."""
    print("\n[TODO: Implement return logic]")


def view_current_loans(equipment):
    """Display all items that currently have active borrowers."""
    print("\n[TODO: Implement active loans view]")


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