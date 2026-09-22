"""
Employee Attendance & Salary Processing System
-----------------------------------------------
A Python program that:
1. Calculates attendance percentage
2. Calculates overtime pay
3. Calculates final salary
4. Identifies employees below the attendance threshold
5. Generates a summary report (summary_report.txt)

Author: <your name>
"""

# -----------------------------
# Step 1: Employee Data (list of dictionaries)
# -----------------------------
import random

FIRST_NAMES = ["Ravi", "Anita", "Suresh", "Divya", "Karthik", "Priya", "Arjun",
               "Meena", "Vikram", "Sneha", "Rohan", "Kavya", "Manoj", "Deepa",
               "Sanjay", "Pooja", "Ajay", "Neha", "Vishal", "Swathi"]
LAST_NAMES = ["Kumar", "Rao", "Iyer", "Menon", "Raj", "Sharma", "Reddy",
              "Nair", "Gupta", "Patel", "Singh", "Verma", "Pillai", "Joshi"]
DEPARTMENTS = ["Finance", "HR", "IT", "Marketing", "Operations", "Sales"]


def generate_employee_records(n=5, seed=42):
    """Generate n random employee records as a list of dictionaries."""
    random.seed(seed)  # fixed seed = same data every run (reproducible for testing)
    records = []
    for i in range(1, n + 1):
        emp = {
            "id": f"EMP{1000 + i}",
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "dept": random.choice(DEPARTMENTS),
            "days_present": random.randint(10, 26),
            "basic_salary": random.randint(25000, 60000),
            "overtime_hours": random.randint(0, 15),
        }
        records.append(emp)
    return records


# Change the number here to scale: 5, 100, 200, or however many you need
employee_records = generate_employee_records(n=200)

# -----------------------------
# Constants
# -----------------------------
TOTAL_WORKING_DAYS = 26
OVERTIME_RATE_PER_HOUR = 250
OVERTIME_MULTIPLIER = 1.5
ATTENDANCE_THRESHOLD = 75  # percent


# -----------------------------
# Step 2: Core Calculation Functions
# -----------------------------
def calculate_attendance_pct(days_present, total_days=TOTAL_WORKING_DAYS):
    """Return attendance percentage rounded to 2 decimal places."""
    return round((days_present / total_days) * 100, 2)


def calculate_overtime_pay(overtime_hours, rate=OVERTIME_RATE_PER_HOUR):
    """Return overtime pay at 1.5x the hourly rate."""
    return overtime_hours * rate * OVERTIME_MULTIPLIER


def calculate_total_salary(basic_salary, overtime_pay):
    """Return final salary = basic salary + overtime pay."""
    return basic_salary + overtime_pay


def get_attendance_status(pct, threshold=ATTENDANCE_THRESHOLD):
    """Return 'OK' or 'Below Threshold' based on attendance percentage."""
    return "OK" if pct >= threshold else "Below Threshold"


# -----------------------------
# Step 3: Process Records + Generate Report
# -----------------------------
def process_employees(records, report_filename="summary_report.txt"):
    below_threshold_employees = []

    with open(report_filename, "w") as report:
        report.write("EMPLOYEE ATTENDANCE & SALARY SUMMARY REPORT\n")
        report.write("=" * 55 + "\n\n")
        report.write(f"{'Name':<15}{'Attendance %':<15}{'Total Salary':<15}{'Status'}\n")
        report.write("-" * 55 + "\n")

        for emp in records:
            try:
                pct = calculate_attendance_pct(emp["days_present"])
                overtime_pay = calculate_overtime_pay(emp["overtime_hours"])
                total_salary = calculate_total_salary(emp["basic_salary"], overtime_pay)
                status = get_attendance_status(pct)

                if status == "Below Threshold":
                    below_threshold_employees.append(emp["name"])

                line = f"{emp['name']:<15}{pct:<15}{'Rs.' + str(total_salary):<15}{status}\n"
                report.write(line)

            except KeyError as e:
                print(f"Missing field for {emp.get('id', 'UNKNOWN')}: {e}")
            except ZeroDivisionError:
                print(f"Invalid total working days for {emp.get('id', 'UNKNOWN')}")

        report.write("\n" + "-" * 55 + "\n")
        total = len(records)
        flagged_count = len(below_threshold_employees)
        report.write(f"Total Employees Processed: {total}\n")
        report.write(f"Employees Below {ATTENDANCE_THRESHOLD}% Attendance: {flagged_count}\n")

        if flagged_count:
            preview = ", ".join(below_threshold_employees[:20])
            report.write(f"Names (first 20 shown): {preview}")
            if flagged_count > 20:
                report.write(f" ... and {flagged_count - 20} more")
            report.write("\n")

    return below_threshold_employees


# -----------------------------
# Step 4: Run the Program
# -----------------------------
if __name__ == "__main__":
    flagged = process_employees(employee_records)
    print(f"Processed {len(employee_records)} employees.")
    print("Summary report generated successfully as 'summary_report.txt'.")
    if flagged:
        print(f"{len(flagged)} employee(s) below attendance threshold "
              f"(see summary_report.txt for full list).")
    else:
        print("All employees meet the attendance threshold.")
