import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
import random

def classify_difficulty(cgpa):
    if cgpa <= 8:
        return 1  # Easy
    elif cgpa <= 9:
        return 2  # Medium
    else:
        return 3  # Hard

def generate_question_paper(total_marks, subject, subject_code, csv_file, cgpa):
    try:
        # Read CSV file with 'ISO-8859-15' encoding
        questions_df = pd.read_csv(csv_file, encoding='ISO-8859-15')
        
        # Filter questions based on subject
        subject_questions = []
        for _, row in questions_df.iterrows():
            course_name = str(row['Course_Name']).strip().upper()
            difficulty = row['Difficulty']
            if isinstance(difficulty, int):  # Check if difficulty is already an integer
                subject_questions.append({'Question': row['Question'], 'Marks': row['Marks'], 'Difficulty': difficulty})
            else:
                try:
                    difficulty = int(difficulty)  # Attempt to convert difficulty to integer
                    subject_questions.append({'Question': row['Question'], 'Marks': row['Marks'], 'Difficulty': difficulty})
                except ValueError:
                    # Skip rows with invalid difficulty values
                    continue
        
        # Initialize variables
        selected_questions = []
        remaining_marks = total_marks
        
        # Shuffle subject questions for randomness
        random.shuffle(subject_questions)
        
        # Iterate through subject questions and select randomly to match total marks
        for row in subject_questions:
            # Check if the question difficulty matches and marks are within remaining_marks
            difficulty = classify_difficulty(cgpa)
            if row['Difficulty'] == difficulty and row['Marks'] <= remaining_marks:
                selected_questions.append({'Question': row['Question'], 'Marks': row['Marks']})
                remaining_marks -= row['Marks']
                if remaining_marks <= 0:
                    break
        
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
        for i, q in enumerate(selected_questions):
            question_text = q['Question']
            pdf.multi_cell(0, 10, f"Question {i+1}: {question_text}")
            pdf.multi_cell(0, 10, f"Marks: {q['Marks']}")
        
        # Define output directory and filename
        output_dir = os.path.join(os.path.dirname(csv_file), 'question_papers')
        os.makedirs(output_dir, exist_ok=True)
        pdf_output_file = os.path.join(output_dir, f"Generated_Question_Sets_{datetime.now().year}.pdf")
        
        # Save PDF to file
        pdf.output(pdf_output_file)
        
        return pdf_output_file
    
    except Exception as e:
        print(f"Error generating question paper: {e}")
        return None

# Example usage
# total_marks = 30
# subject = "Compiler Design"
# subject_code = "CS304"
# csv_file = r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\extracted_questions.csv"
# cgpa = 8.5  # Assuming a fixed CGPA for demonstration
# question_paper_pdf = generate_question_paper(total_marks, subject, subject_code, csv_file, cgpa)
# if question_paper_pdf:
#     print(f"Question paper generated: {question_paper_pdf}")
# else:
#     print("Question paper could not be generated.")
