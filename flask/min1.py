from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from question_extraction1 import extract_questions_from_pdf, save_to_csv
from generate_question_paper1 import generate_question_paper
import os
import csv

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Full path to the uploads folder
UPLOADS_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

# Function to check if username exists in the CSV file
def username_exists(username):
    with open(os.path.join(UPLOADS_FOLDER, 'user.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

# Route to handle the login page
@app.route('/')
def login():
    return render_template("index.html")

# Route to handle the form submission for login
@app.route("/login", methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists
    if username_exists(username):
        # Implement password checking logic here
        return redirect("/enter")  # Redirect to preview page on successful login
    else:
        return redirect("/register")  # Redirect to registration page if username doesn't exist

@app.route("/enter")
def enter():
    return render_template("home.html")
@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            print("SUccessfule entry")
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print("Path:",file_path)

            # Extract questions from the uploaded PDF
            questions, code, course_name = extract_questions_from_pdf(file_path)
            print("Questions: ",questions)
            print("Code: ",code)
            print("course_name: ",course_name)

            # Save questions to CSV
            csv_file = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_questions1.csv')
            print("CSV", csv_file)
            save_to_csv(questions, code, course_name, csv_file)
            print("Added")

            # Redirect to fileuploader.html or any other page
            return redirect(url_for('fileuploader'))
    return render_template('fileuploader.html')

@app.route('/fileuploader')
def fileuploader():
    return render_template('fileuploader.html')
# Route to handle the preview page
@app.route("/preview", methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        subject = request.form['subject']
        subject_code = request.form['subject_code']
        total_marks = int(request.form['total_marks'])
        current_cgpa = float(request.form['current_cgpa'])

        csv_file = os.path.join(UPLOADS_FOLDER, 'extracted_questions.csv')
        pdf_file_path = generate_question_paper(total_marks, subject, subject_code, csv_file,current_cgpa)
        
        if pdf_file_path:
            pdf_file_url = pdf_file_path.replace(os.getcwd(), '')
            return render_template("preview.html", pdf_file_url=pdf_file_url)
        else:
            return render_template("preview.html", error_message="Failed to generate question paper.")
    return render_template("preview.html")


@app.route("/download_pdf/<path:pdf_file>")
def download_pdf(pdf_file):
    pdf_full_path = os.path.join(os.getcwd(), pdf_file)
    print("Path: ", pdf_full_path)
    return send_file(pdf_full_path, as_attachment=True, mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
