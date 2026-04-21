# ============================================================
# app.py — Main Flask Application
# ============================================================

from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from logic.notice_generator import generate_notice_docx
import os
import json

app = Flask(__name__)

DATA_FILE = "data.json"

DEGREE_OPTIONS = [
    "B.Tech/B.E.", "M.Tech", "B.Sc", "M.Sc", "PhD"
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ── Helper: Load departments from JSON ──
def load_departments():
    with open(DATA_FILE, "r") as f:
        return json.load(f)["departments"]

# ── Helper: Save departments to JSON ──
def save_departments(departments):
    with open(DATA_FILE, "w") as f:
        json.dump({"departments": departments}, f, indent=4)

# ── Main Form ──
@app.route("/", methods=["GET"])
def index():
    return render_template(
        "notice_form.html",
        departments=load_departments(),
        degree_options=DEGREE_OPTIONS,
        months=MONTHS,
        saved={}
    )

# ── Edit (back from preview with data preserved) ──
@app.route("/edit", methods=["POST"])
def edit():
    saved = {
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
    return render_template(
        "notice_form.html",
        departments=load_departments(),
        degree_options=DEGREE_OPTIONS,
        months=MONTHS,
        saved=saved
    )

# ── Generate Notice (direct download) ──
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
    return send_file(filepath, as_attachment=True)

# ── Preview Notice ──
@app.route("/preview", methods=["POST"])
def preview():
    departments = request.form.getlist("departments")
    num_cols = 5
    num_rows = -(-len(departments) // num_cols)

    padded_depts = departments + [""] * (num_rows * num_cols - len(departments))

    dept_rows = []
    for r in range(num_rows):
        row = padded_depts[r * num_cols:(r + 1) * num_cols]
        dept_rows.append(row)

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
    return render_template("notice_preview.html", data=data)

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
    return send_file(filepath, as_attachment=True)

# ── Add Department ──
@app.route("/departments/add", methods=["POST"])
def add_department():
    name = request.form.get("new_dept", "").strip().upper()
    if name:
        departments = load_departments()
        if name not in departments:
            departments.append(name)
            save_departments(departments)
    return redirect(url_for("index"))

# ── Delete Department ──
@app.route("/departments/delete/<name>", methods=["POST"])
def delete_department(name):
    departments = load_departments()
    departments = [d for d in departments if d != name]
    save_departments(departments)
    return redirect(url_for("index"))

# ── Edit Department ──
@app.route("/departments/edit", methods=["POST"])
def edit_department():
    old_name = request.form.get("old_name", "").strip()
    new_name = request.form.get("new_name", "").strip().upper()
    if old_name and new_name:
        departments = load_departments()
        departments = [new_name if d == old_name else d for d in departments]
        save_departments(departments)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)