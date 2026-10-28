# Reflection

## 1. Why are static-analysis tools useful, and what can they miss?

Static-analysis tools quickly find patterns such as unsafe evaluation, weak
hashing, swallowed exceptions, and style problems without needing a test for
each one. They do not understand every business rule, though: the unused
withdrawal fee was a likely behavior bug that required reading the code and
observing the program rather than relying on a lint warning alone.

## 2. Which finding was most important, and why?

The arbitrary `eval` in bonus calculation was the most important finding
because it could run Python code supplied as the expression. Replacing it with
a numeric rate restricts the input to the calculation the bank feature
actually needs.

## 3. How did the fixes preserve the program's purpose?

The program still creates accounts, accepts deposits, processes withdrawals,
calculates a bonus, generates a temporary PIN, hashes a PIN, and exports a
backup. The fixes make failure outcomes explicit, apply the already-declared
withdrawal fee, and use safer APIs while preserving the demonstration flow.

## 4. What did you learn about using multiple analysis tools?

Bandit highlighted security-sensitive APIs, while Flake8 and Pylint exposed
style, naming, and maintainability issues. Their reports were useful starting
points, but reviewing runtime output and the surrounding code was also
necessary to identify behavior that the tools did not report. Rerunning all
three tools after changes provides evidence that the reported patterns have
been addressed.
