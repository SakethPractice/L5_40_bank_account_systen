# Static Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Arbitrary code execution through `eval` | Security (high) | 39 | `compute_bonus` evaluated caller-provided Python code. | Replace the expression with a validated bonus rate and calculate the bonus directly. |
| Weak PIN hashing | Security (high) | 44 | MD5 is unsuitable for hashing PINs and its output was unsalted. | Generate a random salt and use PBKDF2-HMAC-SHA256. |
| Shell command injection risk | Security (high) | 55 | `os.system` included the backup filename in a shell command. | Remove shell execution and report successful backup using Python. |
| Deposit failures hidden | Reliability (medium) | 21-24 | A bare `except` swallowed missing-account and other errors without changing/reporting success. | Validate the account and amount, then return an explicit success value. |
| Shared mutable default | Correctness (medium) | 11 | A default list persisted across calls to account creation. | Use `None` as the default and append only to a caller-provided transaction list. |
| Unused withdrawal fee | Correctness (medium) | 27-32 | The fee was assigned but never deducted from an account. | Define the fee once, include it in the balance check, and deduct it on successful withdrawal. |
| Insecure temporary PIN generation | Security (low) | 48 | `random.randint` is not intended for security-sensitive values. | Use `secrets.randbelow` to generate the PIN. |
| Lint and style issues | Quality (low) | Multiple | The original code had an unused import, non-snake-case function name, missing docstrings, formatting errors, and unmanaged file handles. | Remove unused imports, use conventional naming/docstrings, and manage the backup with a context manager and explicit encoding. |

Line numbers describe the original version before fixes.
