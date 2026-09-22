"""
Employee Attendance & Salary Processing System — Web Dashboard
------------------------------------------------------------------
A professional Flask web app to add, remove, and view employees,
with live-calculated attendance %, overtime pay, and salary status.

Run with: python app.py
Then open: http://127.0.0.1:5000
"""

import random
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# -----------------------------
# Constants
# -----------------------------
TOTAL_WORKING_DAYS = 26
OVERTIME_RATE_PER_HOUR = 250
OVERTIME_MULTIPLIER = 1.5
ATTENDANCE_THRESHOLD = 75

FIRST_NAMES = ["Ravi", "Anita", "Suresh", "Divya", "Karthik", "Priya", "Arjun",
               "Meena", "Vikram", "Sneha", "Rohan", "Kavya", "Manoj", "Deepa"]
LAST_NAMES = ["Kumar", "Rao", "Iyer", "Menon", "Raj", "Sharma", "Reddy", "Nair"]
DEPARTMENTS = ["Finance", "HR", "IT", "Marketing", "Operations", "Sales"]


# -----------------------------
# In-memory employee store (resets when server restarts)
# -----------------------------
def generate_initial_employees(n=15):
    records = []
    for i in range(1, n + 1):
        records.append({
            "id": f"EMP{1000 + i}",
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "dept": random.choice(DEPARTMENTS),
            "days_present": random.randint(10, 26),
            "basic_salary": random.randint(25000, 60000),
            "overtime_hours": random.randint(0, 15),
        })
    return records


employees = generate_initial_employees(300)
next_id_counter = len(employees) + 1001


# -----------------------------
# Calculation logic
# -----------------------------
def calculate_attendance_pct(days_present, total_days=TOTAL_WORKING_DAYS):
    return round((days_present / total_days) * 100, 2)


def calculate_overtime_pay(overtime_hours, rate=OVERTIME_RATE_PER_HOUR):
    return overtime_hours * rate * OVERTIME_MULTIPLIER


def process_employees(records):
    processed = []
    for emp in records:
        try:
            pct = calculate_attendance_pct(emp["days_present"])
            overtime_pay = calculate_overtime_pay(emp["overtime_hours"])
            total_salary = emp["basic_salary"] + overtime_pay
            status = "OK" if pct >= ATTENDANCE_THRESHOLD else "Below Threshold"
            processed.append({**emp, "pct": pct, "total_salary": total_salary, "status": status})
        except (KeyError, TypeError, ZeroDivisionError):
            continue
    return processed


# -----------------------------
# HTML Template
# -----------------------------
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Employee Attendance & Salary Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {
    --bg: #0a0e1a; --card: #151b2b; --border: #2a3348;
    --text: #f1f4f9; --muted: #a8b3cc; --accent: #5b9bff;
    --green: #3ddb8f; --red: #ff6b81; --amber: #ffc061;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
    background: var(--bg); color: var(--text); margin: 0; padding: 32px;
    font-size: 15px; line-height: 1.5;
  }
  h1 { font-size: 26px; margin: 0 0 6px 0; font-weight: 700; letter-spacing: -0.3px; }
  .subtitle { color: var(--muted); margin-bottom: 28px; font-size: 14.5px; }

  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px; }
  .stat-card {
    background: linear-gradient(145deg, #1a2438, #121a2c);
    border: 1px solid var(--border); border-radius: 12px; padding: 20px 22px;
  }
  .stat-label { color: var(--muted); font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.6px; font-weight: 600; }
  .stat-value { font-size: 28px; font-weight: 800; margin-top: 8px; letter-spacing: -0.5px; }
  .stat-value.green { color: var(--green); }
  .stat-value.red { color: var(--red); }
  .stat-value.accent { color: var(--accent); }

  .panel {
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 22px; margin-bottom: 24px;
  }
  .panel h2 { font-size: 17px; margin: 0 0 16px 0; font-weight: 700; }

  form.add-form { display: grid; grid-template-columns: repeat(6, 1fr) auto; gap: 12px; align-items: end; }
  form.add-form label { font-size: 12px; color: var(--muted); display: block; margin-bottom: 6px; font-weight: 600; }
  form.add-form input, form.add-form select {
    width: 100%; padding: 10px 12px; border-radius: 7px; border: 1px solid var(--border);
    background: #0e1626; color: var(--text); font-size: 14px;
  }
  form.add-form input::placeholder { color: #5c6785; }
  .btn {
    background: var(--accent); color: #061024; border: none; padding: 11px 20px;
    border-radius: 7px; cursor: pointer; font-weight: 700; font-size: 14px;
  }
  .btn:hover { background: #4a8aff; }
  .btn-danger { background: transparent; color: var(--red); border: 1px solid var(--red); padding: 7px 14px; font-size: 12.5px; font-weight: 600; }
  .btn-danger:hover { background: rgba(255,107,129,0.12); }
  .btn-ghost { background: transparent; color: var(--text); border: 1px solid var(--border); font-weight: 600; }
  .btn-ghost:hover { border-color: var(--accent); }

  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.6px;
       color: var(--muted); padding: 12px 14px; border-bottom: 1px solid var(--border); font-weight: 700; }
  td { padding: 13px 14px; border-bottom: 1px solid var(--border); font-size: 14px; color: var(--text); }
  tbody tr:nth-child(even) { background: rgba(255,255,255,0.015); }
  tr:hover td { background: rgba(91,155,255,0.07); }

  .badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; display: inline-block; }
  .badge.ok { background: rgba(61,219,143,0.18); color: var(--green); }
  .badge.below { background: rgba(255,107,129,0.18); color: var(--red); }

  .name-cell { font-weight: 700; color: var(--text); }
  .dept-tag {
    color: #c3cbe0; font-size: 12.5px; font-weight: 600; background: rgba(168,179,204,0.12);
    padding: 3px 10px; border-radius: 6px; display: inline-block;
  }
  .toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 12px; flex-wrap: wrap; }
  #searchBox {
    padding: 10px 14px; border-radius: 7px; border: 1px solid var(--border);
    background: #0e1626; color: var(--text); font-size: 14px; width: 240px;
  }
  #searchBox::placeholder { color: #5c6785; }
  .table-scroll { max-height: 620px; overflow-y: auto; border: 1px solid var(--border); border-radius: 8px; }
  .table-scroll table { margin: 0; }
  .table-scroll th { position: sticky; top: 0; background: #1e2a44; z-index: 1; }
  .row-count { color: var(--muted); font-size: 12.5px; margin-top: 10px; font-weight: 500; }
</style>
</head>
<body>

  <h1>Employee Attendance &amp; Salary Dashboard</h1>
  <div class="subtitle">Live view of attendance, overtime, and payroll status</div>

  <div class="stats">
    <div class="stat-card">
      <div class="stat-label">Total Employees</div>
      <div class="stat-value accent">{{ total }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Attendance</div>
      <div class="stat-value">{{ avg_attendance }}%</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Below Threshold</div>
      <div class="stat-value red">{{ below_count }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total Payroll</div>
      <div class="stat-value green">Rs. {{ "{:,.0f}".format(total_payroll) }}</div>
    </div>
  </div>

  <div class="panel">
    <h2>Add New Employee</h2>
    <form class="add-form" method="POST" action="{{ url_for('add_employee') }}">
      <div>
        <label>Name</label>
        <input type="text" name="name" required placeholder="e.g. Rahul Verma">
      </div>
      <div>
        <label>Department</label>
        <select name="dept">
          {% for d in departments %}<option value="{{ d }}">{{ d }}</option>{% endfor %}
        </select>
      </div>
      <div>
        <label>Days Present</label>
        <input type="number" name="days_present" min="0" max="31" required value="24">
      </div>
      <div>
        <label>Basic Salary</label>
        <input type="number" name="basic_salary" min="0" required value="40000">
      </div>
      <div>
        <label>Overtime Hours</label>
        <input type="number" name="overtime_hours" min="0" required value="0">
      </div>
      <div></div>
      <button class="btn" type="submit">+ Add Employee</button>
    </form>
  </div>

  <div class="panel">
    <div class="toolbar">
      <h2 style="margin:0;">Employee Records</h2>
      <div style="display:flex; gap:10px;">
        <input id="searchBox" type="text" placeholder="🔍 Search name or department..." onkeyup="filterTable()">
        <form method="GET" action="{{ url_for('regenerate') }}">
          <button class="btn btn-ghost" type="submit">🔄 Load New Sample Data</button>
        </form>
      </div>
    </div>
    <div class="table-scroll">
      <table id="empTable">
        <tr>
          <th>ID</th><th>Name</th><th>Dept</th><th>Days Present</th>
          <th>Attendance</th><th>Basic Salary</th><th>OT Hours</th>
          <th>Total Salary</th><th>Status</th><th></th>
        </tr>
        {% for emp in employees %}
        <tr>
          <td>{{ emp.id }}</td>
          <td class="name-cell">{{ emp.name }}</td>
          <td><span class="dept-tag">{{ emp.dept }}</span></td>
          <td>{{ emp.days_present }}</td>
          <td>{{ emp.pct }}%</td>
          <td>Rs. {{ "{:,.0f}".format(emp.basic_salary) }}</td>
          <td>{{ emp.overtime_hours }}</td>
          <td>Rs. {{ "{:,.0f}".format(emp.total_salary) }}</td>
          <td><span class="badge {{ 'ok' if emp.status == 'OK' else 'below' }}">{{ emp.status }}</span></td>
          <td>
            <form method="POST" action="{{ url_for('delete_employee', emp_id=emp.id) }}" style="margin:0;">
              <button class="btn btn-danger" type="submit">Remove</button>
            </form>
          </td>
        </tr>
        {% endfor %}
      </table>
    </div>
    <div class="row-count">Showing {{ total }} employees</div>
  </div>

  <script>
    function filterTable() {
      const input = document.getElementById('searchBox').value.toLowerCase();
      const rows = document.getElementById('empTable').getElementsByTagName('tr');
      for (let i = 1; i < rows.length; i++) {
        const name = rows[i].cells[1].textContent.toLowerCase();
        const dept = rows[i].cells[2].textContent.toLowerCase();
        rows[i].style.display = (name.includes(input) || dept.includes(input)) ? '' : 'none';
      }
    }
  </script>

</body>
</html>
"""


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def dashboard():
    processed = process_employees(employees)
    total = len(processed)
    below_count = sum(1 for e in processed if e["status"] == "Below Threshold")
    avg_attendance = round(sum(e["pct"] for e in processed) / total, 2) if total else 0
    total_payroll = sum(e["total_salary"] for e in processed)

    return render_template_string(
        PAGE_TEMPLATE,
        employees=processed,
        total=total,
        below_count=below_count,
        avg_attendance=avg_attendance,
        total_payroll=total_payroll,
        departments=DEPARTMENTS,
    )


@app.route("/add", methods=["POST"])
def add_employee():
    global next_id_counter
    try:
        new_emp = {
            "id": f"EMP{next_id_counter}",
            "name": request.form["name"].strip() or "Unnamed",
            "dept": request.form.get("dept", "General"),
            "days_present": int(request.form["days_present"]),
            "basic_salary": int(request.form["basic_salary"]),
            "overtime_hours": int(request.form["overtime_hours"]),
        }
        employees.append(new_emp)
        next_id_counter += 1
    except (ValueError, KeyError) as e:
        print(f"Invalid form data: {e}")
    return redirect(url_for("dashboard"))


@app.route("/delete/<emp_id>", methods=["POST"])
def delete_employee(emp_id):
    global employees
    employees = [e for e in employees if e["id"] != emp_id]
    return redirect(url_for("dashboard"))


@app.route("/regenerate")
def regenerate():
    global employees, next_id_counter
    employees = generate_initial_employees(300)
    next_id_counter = len(employees) + 1001
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)