"""Bank account management module."""

import hashlib
import secrets
import os

account_data = {}


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create a bank account with an optional initial transaction list."""
    if transactions is None:
        transactions = []

    if acc_id in account_data:
        return False

    account_data[acc_id] = {
        "name": name,
        "balance": initial_deposit,
    }
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id, amount):
    """Deposit a positive amount into an existing account."""
    if acc_id not in account_data or amount <= 0:
        return False

    account_data[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw money if the account exists and has sufficient funds."""
    if account_data.get(acc_id) is None:
        return False

    if amount <= 0:
        return False

    if account_data[acc_id]["balance"] < amount:
        return False

    account_data[acc_id]["balance"] -= amount
    return True


def compute_bonus(acc_id, rate=0.05):
    """Calculate a bonus using a specified rate."""
    if acc_id not in account_data:
        return 0

    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1.")

    balance = account_data[acc_id]["balance"]
    return balance * rate


def get_hash(pin):
    """Hash a PIN using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = secrets.token_bytes(16)
    pin_hash = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        600_000,
    )
    return f"{salt.hex()}:{pin_hash.hex()}"


def generate_temp_pin():
    """Generate a cryptographically secure four-digit PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Back up account data to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(account_data))

    print("Backup complete:", filename)


def main():
    """Run the sample bank-account operations."""
    admin_token = os.environ.get("BANK_ADMIN_TOKEN")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token is not None)


main()
