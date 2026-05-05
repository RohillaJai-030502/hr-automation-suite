# ============================================================
# app.py — Main Flask Application (Version 2)
# ============================================================

from flask import Flask, render_template, request, send_file, redirect, url_for, session, jsonify
from logic.notice_generator import generate_notice_docx
from logic.form_generator import generate_form_docx
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hr_automation_secret_key_2024"

DATA_FILE     = "data.json"
HISTORY_FILE  = "history.json"
DEFAULTS_FILE = "defaults.json"

DEGREE_OPTIONS = [
    "B.Tech/B.E.", "M.Tech", "B.Sc", "M.Sc", "PhD"
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ── Helpers ──
def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_departments():
    return load_json(DATA_FILE, {"departments": []})["departments"]

def save_departments(departments):
    save_json(DATA_FILE, {"departments": departments})

def load_history():
    return load_json(HISTORY_FILE, {"history": []})["history"]

def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    history = history[:20]
    save_json(HISTORY_FILE, {"history": history})

def load_defaults():
    return load_json(DEFAULTS_FILE, {})

def save_defaults(defaults):
    save_json(DEFAULTS_FILE, defaults)

# ── Dashboard (Home) ──
@app.route("/", methods=["GET"])
def index():
    return render_template("dashboard.html")

# ── ION Notice Form ──
@app.route("/ion-notice", methods=["GET"])
def ion_notice():
    saved = session.pop("form_data", {})
    defaults = load_defaults()
    return render_template(
        "notice_form.html",
        departments=load_departments(),
        degree_options=DEGREE_OPTIONS,
        months=MONTHS,
        saved=saved,
        defaults=defaults,
        history=load_history()
    )

# ── Save Defaults ──
@app.route("/save-defaults", methods=["POST"])
def save_defaults_route():
    defaults = {
        "signatory_name":        request.form.get("signatory_name", ""),
        "signatory_designation": request.form.get("signatory_designation", ""),
        "ion_prefix":            request.form.get("ion_prefix", ""),
    }
    save_defaults(defaults)
    session["form_data"] = {
        "degree":                request.form.get("degree"),
        "start_month":           request.form.get("start_month"),
        "start_year":            request.form.get("start_year"),
        "end_month":             request.form.get("end_month"),
        "end_year":              request.form.get("end_year"),
        "last_date":             request.form.get("last_date"),
        "ion_number":            request.form.get("ion_number"),
        "notice_date":           request.form.get("notice_date"),
        "signatory_name":        request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":           request.form.getlist("departments"),
    }
    return redirect(url_for("ion_notice"))

# ── Preview ──
@app.route("/preview", methods=["POST"])
def preview():
    departments = request.form.getlist("departments")
    num_cols = 5
    num_rows = -(-len(departments) // num_cols)
    padded_depts = departments + [""] * (num_rows * num_cols - len(departments))
    dept_rows = [padded_depts[r * num_cols:(r + 1) * num_cols] for r in range(num_rows)]

    data = {
        "degree":                request.form.get("degree"),
        "start_month":           request.form.get("start_month"),
        "start_year":            request.form.get("start_year"),
        "end_month":             request.form.get("end_month"),
        "end_year":              request.form.get("end_year"),
        "last_date":             request.form.get("last_date"),
        "ion_number":            request.form.get("ion_number"),
        "notice_date":           request.form.get("notice_date"),
        "signatory_name":        request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":           departments,
        "dept_rows":             dept_rows,
    }
    session["form_data"] = data
    return render_template("notice_preview.html", data=data)

# ── Edit (back from preview) ──
@app.route("/edit", methods=["POST"])
def edit():
    session["form_data"] = {
        "degree":                request.form.get("degree"),
        "start_month":           request.form.get("start_month"),
        "start_year":            request.form.get("start_year"),
        "end_month":             request.form.get("end_month"),
        "end_year":              request.form.get("end_year"),
        "last_date":             request.form.get("last_date"),
        "ion_number":            request.form.get("ion_number"),
        "notice_date":           request.form.get("notice_date"),
        "signatory_name":        request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":           request.form.getlist("departments"),
    }
    return redirect(url_for("ion_notice"))

# ── Generate (direct download) ──
@app.route("/generate", methods=["POST"])
def generate():
    data = {
        "degree":                request.form.get("degree"),
        "start_month":           request.form.get("start_month"),
        "start_year":            request.form.get("start_year"),
        "end_month":             request.form.get("end_month"),
        "end_year":              request.form.get("end_year"),
        "last_date":             request.form.get("last_date"),
        "ion_number":            request.form.get("ion_number"),
        "notice_date":           request.form.get("notice_date"),
        "signatory_name":        request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":           request.form.getlist("departments"),
    }
    filepath = generate_notice_docx(data)
    save_history({
        "filename": os.path.basename(filepath),
        "degree": data["degree"],
        "period": f"{data['start_month']} {data['start_year']} - {data['end_month']} {data['end_year']}",
        "generated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "filepath": filepath,
        "departments_count": len(data["departments"])
    })
    return send_file(filepath, as_attachment=True)

# ── Download after Preview ──
@app.route("/download", methods=["POST"])
def download():
    data = {
        "degree":                request.form.get("degree"),
        "start_month":           request.form.get("start_month"),
        "start_year":            request.form.get("start_year"),
        "end_month":             request.form.get("end_month"),
        "end_year":              request.form.get("end_year"),
        "last_date":             request.form.get("last_date"),
        "ion_number":            request.form.get("ion_number"),
        "notice_date":           request.form.get("notice_date"),
        "signatory_name":        request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":           request.form.getlist("departments"),
    }
    filepath = generate_notice_docx(data)
    save_history({
        "filename": os.path.basename(filepath),
        "degree": data["degree"],
        "period": f"{data['start_month']} {data['start_year']} - {data['end_month']} {data['end_year']}",
        "generated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "filepath": filepath,
        "departments_count": len(data["departments"])
    })
    return send_file(filepath, as_attachment=True)

# ── Download from History ──
@app.route("/history/download/<filename>", methods=["GET"])
def download_history(filename):
    filepath = os.path.join("generated_notices", filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

# ── Clear History ──
@app.route("/history/clear", methods=["POST"])
def clear_history():
    save_json(HISTORY_FILE, {"history": []})
    return redirect(url_for("ion_notice"))

# ── Add Department ──
@app.route("/departments/add", methods=["POST"])
def add_department():
    name = request.form.get("new_dept", "").strip().upper()
    if name:
        departments = load_departments()
        if name not in departments:
            departments.append(name)
            save_departments(departments)
    return redirect(url_for("ion_notice"))

# ── Delete Department ──
@app.route("/departments/delete/<name>", methods=["POST"])
def delete_department(name):
    departments = load_departments()
    departments = [d for d in departments if d != name]
    save_departments(departments)
    return redirect(url_for("ion_notice"))

# ── Edit Department ──
@app.route("/departments/edit", methods=["POST"])
def edit_department():
    old_name = request.form.get("old_name", "").strip()
    new_name = request.form.get("new_name", "").strip().upper()
    if old_name and new_name:
        departments = load_departments()
        departments = [new_name if d == old_name else d for d in departments]
        save_departments(departments)
    return redirect(url_for("ion_notice"))

# ── Generate FM/HRD-09 Form ──
@app.route("/form/hrd09", methods=["GET"])
def generate_hrd09():
    filepath = generate_form_docx()
    return send_file(filepath, as_attachment=True)

# ── API: History for Dashboard ──
@app.route("/api/history", methods=["GET"])
def api_history():
    return jsonify({"history": load_history()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)