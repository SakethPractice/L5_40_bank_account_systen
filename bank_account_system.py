"""Bank account management module."""

import hashlib
import hmac
import json
import secrets

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
    """Return a salted PBKDF2-HMAC-SHA256 hash of a PIN."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", pin.encode("utf-8"), salt, 200_000
    )
    return f"{salt.hex()}:{digest.hex()}"


def verify_pin(pin, stored_hash):
    """Compare a PIN with the salted hash returned by get_hash."""
    try:
        salt_hex, digest_hex = stored_hash.split(":", maxsplit=1)
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)
    except ValueError:
        return False

    actual_digest = hashlib.pbkdf2_hmac(
        "sha256", pin.encode("utf-8"), salt, 200_000
    )
    return hmac.compare_digest(actual_digest, expected_digest)


def generate_temp_pin():
    """Generate a cryptographically secure temporary PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Write the account ledger as UTF-8 JSON."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        json.dump(account_data, backup_file, indent=2)
        backup_file.write("\n")
    print(f"Backup complete: {filename}")


def main():
    """Run a small bank-account demonstration."""
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    temporary_pin = generate_temp_pin()
    print("PIN Hash:", get_hash(str(temporary_pin)))
    backup_data()


if __name__ == "__main__":
    main()
