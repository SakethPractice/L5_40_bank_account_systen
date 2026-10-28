"""Bank account management module."""

import hashlib
import os
import random

account_data = {}


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create an account and optionally record its creation."""
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    if transactions is not None:
        transactions.append(
            f"Created {acc_id} with initial balance {initial_deposit}"
        )
    return True


def deposit(acc_id, amount):
    """Deposit an amount and return whether the operation succeeded."""
    account = account_data.get(acc_id)
    if account is None or amount <= 0:
        return False
    account["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw an amount and the service fee when funds are sufficient."""
    service_fee = 2.50
    account = account_data.get(acc_id)
    if account is None or amount <= 0:
        return False
    if account["balance"] < amount + service_fee:
        return False
    account["balance"] -= amount + service_fee
    return True


def compute_bonus(acc_id, bonus_rate):
    """Calculate an account bonus for a rate between zero and one."""
    if not 0 <= bonus_rate <= 1:
        raise ValueError("bonus_rate must be between 0 and 1")
    return account_data[acc_id]["balance"] * bonus_rate


def get_hash(pin):
    """Return the MD5 digest of a PIN."""
    return hashlib.md5(pin.encode()).hexdigest()


def generate_temp_pin():
    """Generate a temporary PIN."""
    return random.randint(1000, 9999)


def backup_data(filename="backup.txt"):
    """Write the account ledger to a backup file."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        backup_file.write(str(account_data))
    os.system("echo Backup complete: " + filename)


def main():
    """Run a small bank-account demonstration."""
    admin_token = "SUPER_SECRET_BANK_TOKEN_2026"
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


main()
