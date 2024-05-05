import PyPDF2
import re
import csv

def extract_questions_from_pdf(pdf_path):
    questions = []

    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)

        # Iterate through each page of the PDF
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()

            # Split the text into lines
            lines = text.strip().split('\n')
                

            # Extract questions using regular expressions
            count=0
            q=''
            mark=0
            for line in lines:
                # Define a regular expression pattern to match questions
                # Modify this pattern according to the structure of your questions
                #print("Line: ",line,"course code" in line.lower())
                if "course code" in line.lower():
                    course_code1=line.upper().split("COURSE CODE: ",1)
                    course_code=course_code1[1]
                    
                if "course name" in line.lower():
                    course_name1=line.upper().split("COURSE NAME:",1)
                    course_name=course_name1[1]  
                    
                    
                pattern=r'([0-9].+[A-Z][a-z]+s*.+)'

                    # Search for the pattern in the line
                if line.find("PART") == -1 and line.find("Answer") == -1 and line.find("Module")==-1:
                    matches = re.findall(pattern, line)           

                    if matches:
                        #Add the matched question to the list
                        #questions.extend(matches)   
                        count+=1
                    if count==1:
                        #q+=str(line[:-1])
                        c=line.strip().split(" ")
                        #print("c",c)
                        if c[-1].isnumeric():
                            mark+=int(c[-1])
                            line=line.replace(c[-1],'')
                            #print("yes: ",c)
                        elif c[-1].startswith('('):
                            mark+=int(c[-1][1])
                            line=line.replace(c[-1],'')
                            #print("yes yes: ",c)
                        q+=str(line)
                        #print("q:",q)
                    elif count==2:
                        questions.append({q:mark})
                        count=1
                        q=''
                        mark=0
                        c=line.strip().split(" ")
                        #print("c",c)
                        if c[-1].isnumeric():
                            mark+=int(c[-1])
                            line=line.replace(c[-1],'')
                            #print("yes: ",c)
                        elif c[-1].startswith('('):
                            #mark+=int(s)
                            j=c[-1].partition(")")
                            k=j[0]
                            mark=int(k[1:])
                            line=line.replace(c[-1],'')
                            #print("yes yes: ",c[-1],"line: ",line)
                        q+=str(line)
    return questions,course_code,course_name

def exist_question(csv_file, question):
    count = 1
    q_text = list(question.keys())[0]
    
    # Check if the question already exists in the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as read_file:
        reader = csv.reader(read_file)
        next(reader)  # Skip header row
        for row in reader:
            if row[0] == q_text:
                count += 1
                # No need to continue searching once the question is found
                break
    return count

    

def save_to_csv(questions,code,course, csv_file):
    with open(csv_file, 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow(['Question','CourseCode','CourseName'])
        for question in questions:
            q1=list(question.keys())[0]
            q2=q1.strip().split(" ")
            if (q2[0].isdigit()) and question[q1]>0:
                c=exist_question(csv_file, question)
                #writer.writerow([question[3:],code,course])
                #print([q1, code, course,question[q1]])
                writer.writerow([q1, code, course,question[q1]])      

# Example usage
#pdf_path =r"C:\Users\harsha anand\Downloads\CDT305-A.pdf"  # Replace 'example.pdf' with the path to your PDF file
#questions,code,name = extract_questions_from_pdf(pdf_path)
#csv_file = r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\extracted_questions.csv"

#for idx, question in enumerate(questions, start=1):
 #   print(f"Question {idx}: {question}")
#save_to_csv(questions,code,name, csv_file)

#"C:\Users\harsha anand\Desktop\Miniproject\btech-cs-6-sem-compiler-design-f1031-may-2019.pdf"
#"C:\Users\harsha anand\Desktop\Miniproject\2021 Dec. CST301-A.pdf"
#"C:\Users\harsha anand\Downloads\CDT305-A.pdf"
#"C:\Users\harsha anand\Downloads\CDT307-A.pdf"