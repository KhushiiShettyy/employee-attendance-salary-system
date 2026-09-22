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
Employee records are generated programmatically instead of hardcoded, so the
program can handle any number of employees — 5, 200, or 2000 — without
manually typing each one.

```python
employee_records = generate_employee_records(n=200)
```

Change the value of `n` in `employee_analytics.py` to scale up or down.
A fixed random seed (`seed=42`) keeps the generated data reproducible across runs.

## How to Run
```bash
python3 employee_analytics.py
```

This generates a `summary_report.txt` file in the same folder with the attendance %, total salary, and status (OK / Below Threshold) for each employee.

## Sample Output (console)
```
Processed 200 employees.
Summary report generated successfully as 'summary_report.txt'.
124 employee(s) below attendance threshold (see summary_report.txt for full list).
```

## Sample Output (summary_report.txt, excerpt)
```
EMPLOYEE ATTENDANCE & SALARY SUMMARY REPORT
=======================================================

Name           Attendance %   Total Salary   Status
-------------------------------------------------------
Divya Kumar    69.23          Rs.43674.0     Below Threshold
Neha Menon     88.46          Rs.44696.0     OK
Vikram Iyer    76.92          Rs.32448.0     OK
...

-------------------------------------------------------
Total Employees Processed: 200
Employees Below 75% Attendance: 124
Names (first 20 shown): Divya Kumar, Karthik Verma, Ravi Rao ... and 104 more
```

## Author
<your name here>

---

## Part 2: Web Dashboard (app.py)

A Flask-based web dashboard was added to visualize and manage the same employee data interactively in a browser, instead of only as a script + text file.

### Features
- View all employees in a live, styled dashboard table
- Add new employees through a form (name, department, days present, salary, overtime hours)
- Remove employees with one click
- Summary stat cards: Total Employees, Average Attendance %, Employees Below Threshold, Total Payroll
- Search/filter employees by name or department
- "Load New Sample Data" button to regenerate a fresh random dataset (300 employees by default)

### How to Run
```bash
pip install flask
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

### Tech Used
- Python (Flask web framework)
- HTML/CSS (inline, no external frameworks)
- JavaScript (client-side search/filter)