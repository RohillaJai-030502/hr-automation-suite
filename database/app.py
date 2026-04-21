# ============================================================
# app.py — Main Flask Application
# ============================================================

from flask import Flask, render_template, request, send_file
from logic.notice_generator import generate_notice_docx
import os

app = Flask(__name__)

# All departments list
DEPARTMENTS = [
    "AFTD", "ADS", "BIDS", "BEHI", "SS", "TELIC", "PPG", "QMG",
    "ETF", "PC", "WHD", "EXPD", "WHT&E", "ARISE", "PCD", "AIG",
    "RTRS", "S&D", "R&QA", "WKS", "SEED", "CERBERUS", "DPB",
    "HSP", "I2G"
]

DEGREE_OPTIONS = [
    "B.Tech/B.E.", "M.Tech", "B.Sc", "M.Sc", "PhD"
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "notice_form.html",
        departments=DEPARTMENTS,
        degree_options=DEGREE_OPTIONS,
        months=MONTHS
    )

@app.route("/generate", methods=["POST"])
def generate():
    # Collect form data
    data = {
        "degree":           request.form.get("degree"),
        "start_month":      request.form.get("start_month"),
        "start_year":       request.form.get("start_year"),
        "end_month":        request.form.get("end_month"),
        "end_year":         request.form.get("end_year"),
        "last_date":        request.form.get("last_date"),
        "ion_number":       request.form.get("ion_number"),
        "notice_date":      request.form.get("notice_date"),
        "signatory_name":   request.form.get("signatory_name"),
        "signatory_designation": request.form.get("signatory_designation"),
        "departments":      request.form.getlist("departments"),
    }
    filepath = generate_notice_docx(data)
    return send_file(filepath, as_attachment=True)

# ── Preview Notice ──
@app.route("/preview", methods=["POST"])
def preview():
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
    return render_template(
        "notice_preview.html",
        data=data
    )

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)