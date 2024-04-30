import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
import random

def generate_question_paper(total_marks, subject, subject_code, csv_file):
    # Check if CSV file exists
    if not os.path.isfile(csv_file):
        print("Error: CSV file not found.")
        return None

    # Read CSV file
    try:
        questions_df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Remove leading/trailing whitespaces from subject
    subject = subject.strip()

    # Shuffle the DataFrame to randomize the order of questions
    questions_df = questions_df.sample(frac=1).reset_index(drop=True)

    # Initialize list to store selected questions
    selected_questions = []
    remaining_marks = total_marks

    # Iterate over each row in the shuffled DataFrame
    for _, row in questions_df.iterrows():
        # Check if the course name matches the subject and marks are within remaining_marks
        if row['Course_Name'].strip().lower() == subject.lower() and row['Marks'] <= remaining_marks:
            # Append question and marks to selected_questions list
            selected_questions.append({'Question': row['Question'], 'Marks': row['Marks']})
            remaining_marks -= row['Marks']

        if remaining_marks == 0:
            break
    
    # Validate if total marks requirement is met
    if remaining_marks != 0:
        print(f"Total marks of selected questions ({total_marks - remaining_marks}) does not match the provided total_marks.")
        return None

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add PDF header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Generated Question Set {datetime.now().year}", ln=True, align="C")
    pdf.set_font("Arial", 'I', 14)
    pdf.cell(0, 10, f"SUBJECT: {subject}", ln=True, align="C")
    pdf.cell(0, 10, f"SUBJECT CODE: {subject_code}", ln=True, align="C")
    pdf.cell(0, 10, f"MARKS: {total_marks}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)  # Add some vertical spacing
    
    # Write questions to PDF
    for i, question in enumerate(selected_questions):
        # Handle encoding for Unicode characters
        question_text = question['Question'].encode('latin-1', 'replace').decode('utf-8')
        pdf.multi_cell(0, 10, f"Question {i+1}: {question_text}")
        pdf.multi_cell(0, 10, f"Marks: {question['Marks']}")
        #pdf.cell(0, 10, "")  # Add empty line between questions
    
    # Define output directory and filename
    output_dir = os.path.join(os.path.dirname(csv_file), 'question_papers')
    os.makedirs(output_dir, exist_ok=True)
    pdf_output_file = os.path.join(output_dir, f"Generated_Question_Set_{datetime.now().year}.pdf")

    # Save PDF to file
    pdf.output(pdf_output_file)
    print("Success")
    return pdf_output_file

# Example usage
total_marks = 30
subject = "Compiler Design"
subject_code = "CD101"
csv_file = r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\extracted_questions.csv"
question_paper_pdf = generate_question_paper(total_marks, subject, subject_code, csv_file)

if question_paper_pdf:
    print(f"Question paper generated: {question_paper_pdf}")
else:
    print("Question paper could not be generated.")
