# Employee Attendance & Salary Processing System

A Python program that processes employee attendance and payroll data — built as Mini Project 01 for the "Python Programming Foundations" course.

## Problem Statement
A company needs to automatically:
1. Calculate attendance percentage for each employee
2. Calculate overtime pay
3. Calculate final salary (basic + overtime)
4. Identify employees below the attendance threshold (75%)
5. Generate a summary report

## Concepts Used
- Dictionaries & Lists
- Loops (`for`)
- Functions
- Operators (arithmetic, comparison)
- Control flow (`if`/`else`)
- Exception handling (`try`/`except`)
- File handling (`with open(...)`)
- The `random` module (for generating scalable sample data)

## Scaling the Data
Employee records are generated programmatically instead of hardcoded, so the program can handle any number of employees — 5, 200, or 2000 — without manually typing each one.

```python
employee_records = generate_employee_records(n=200)
```

Change the value of `n` in `employee_analytics.py` to scale up or down. A fixed random seed (`seed=42`) keeps the generated data reproducible across runs.

## How to Run
```bash
python3 employee_analytics.py
```

This generates a `summary_report.txt` file in the same folder with the attendance %, total salary, and status (OK / Below Threshold) for each employee.

## Sample Output (console)