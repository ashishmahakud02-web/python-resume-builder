import os
from flask import Flask, render_template, request, session, send_file, redirect, url_for
from pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "resume-builder-dev-key")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    data = {
        "name": request.form.get("name", "").strip(),
        "title": request.form.get("title", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "location": request.form.get("location", "").strip(),
        "summary": request.form.get("summary", "").strip(),
        "education": request.form.get("education", "").strip(),
        "skills": request.form.get("skills", "").strip(),
        "projects": request.form.get("projects", "").strip(),
        "experience": request.form.get("experience", "").strip(),
        "certifications": request.form.get("certifications", "").strip(),
        "linkedin": request.form.get("linkedin", "").strip(),
        "github": request.form.get("github", "").strip(),
        "template": request.form.get("template", "blue")
    }

    if not data["name"]:
        return redirect(url_for("home"))

    session["resume_data"] = data
    return render_template("resume.html", data=data)


@app.route("/download", methods=["POST"])
def download():
    data = session.get("resume_data")

    if not data:
        return redirect(url_for("home"))

    pdf_file = generate_pdf(data)

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="My_Resume.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
