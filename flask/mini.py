from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from question_extraction import extract_questions_from_pdf, save_to_csv
import os
import csv
from generate_question_paper import generate_question_paper

app = Flask(__name__)

# Full path to the uploads folder
UPLOADS_FOLDER = os.path.join(os.getcwd(), "static", "uploads")

# Function to generate the question paper URL
def generate_question_paper_route(subject, subject_code, total_marks):
    csv_file = os.path.join(UPLOADS_FOLDER, 'extracted_questions.csv')
    pdf_file_path = generate_question_paper(total_marks, subject, subject_code, csv_file)
    print(pdf_file_path)
    if pdf_file_path:
        return pdf_file_path
    else:
        return None

# Function to save user information to a CSV file
def save_user_info(username, email, password):
    try:
        with open(os.path.join(UPLOADS_FOLDER, 'user.csv'), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, email])
    except Exception as e:
        print(f"Error saving user info to CSV: {e}")
        return False

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
    return render_template("login.html")

# Route to handle the form submission for login
@app.route("/login", methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists
    if username_exists(username):
        # Implement password checking logic here
        #return redirect("/preview")  # Redirect to preview page on successful login
        return redirect("/enter")
    else:
        return redirect("/register")  # Redirect to registration page if username doesn't exist
#@app.route("/home")
# Route to handle the registration page
#def home():
    #return render_template("home.html")
@app.route("/enter")
def uploadfile():
    return render_template("file_uploader.html")
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract questions from the uploaded PDF
            questions, code, name = extract_questions_from_pdf(file_path)

            # Save questions to CSV
            csv_file = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_questions.csv')
            save_to_csv(questions, code, name, csv_file)

            return redirect(url_for('upload_form'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        save_user_info(username, email, password)
        
        return redirect("/login")  # Redirect to login page after registration
    return render_template("register.html")

# Route to handle the preview page
@app.route("/preview", methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        subject = request.form['subject']
        subject_code = request.form['subject_code']
        total_marks = int(request.form['total_marks'])

        csv_file = os.path.join(UPLOADS_FOLDER, 'extracted_questions.csv')
        pdf_file_path = generate_question_paper(total_marks, subject, subject_code, csv_file)
        
        if pdf_file_path:
            pdf_file_url = pdf_file_path.replace(os.getcwd(), '')
            return render_template("preview.html", pdf_file_url=pdf_file_url)
        else:
            return render_template("preview.html", error_message="Failed to generate question paper.")
    return render_template("preview.html")

@app.route("/download_pdf/<path:pdf_file>")
def download_pdf(pdf_file):
    pdf_full_path = os.path.join(os.getcwd(), pdf_file)
    print("PATH: ",pdf_full_path)
    return send_file(pdf_full_path, as_attachment=True, mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)