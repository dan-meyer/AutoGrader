#written by Gemini Pro
#edited by Dan Meyer
import os
import pandas as pd
from docx2txt import process
import google.generativeai as genai
import argparse


# Replace with your actual API key
GOOGLE_API_KEY = "<ENTER_YOUR_API_KEY_HERE>"
block_safety = 0

def grade_answers(dataframe, instructions_file):
    with open(instructions_file, "r") as f:
        grading_instructions = f.read()

    grades = []
    for index, row in dataframe.iterrows():
        student_name = row["student_name"]
        student_text = row["text"]
        grade = grade_answer(student_name, student_text, grading_instructions)
        grades.append(grade)

    return grades

def grade_answer(student_name, student_text, grading_instructions):
    model = genai.GenerativeModel('gemini-pro')
    data={ grading_instructions, student_name, student_text }

    print('grade ', student_name)
#    print(data)

    try:
        if block_safety == 1:
            response = model.generate_content(data)
        else:
            response = model.generate_content(data, safety_settings={'HARASSMENT':'block_none'})
    except:
        print('generate_content failed')

    if response.prompt_feedback.block_reason != 0:
        print(student_name, 'blocked')

    try:
        return response.text
    except:
        return student_name+' not graded.  ', response.prompt_feedback

def main():
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # Parse the directory argument
    parser = argparse.ArgumentParser(description='Grade student answers in docx format.')
    parser.add_argument('directory', help='Directory containing docx files')
    args = parser.parse_args()

    directory = args.directory

    docx_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".docx")
    ]

    data = []
    for file in docx_files:
        student_name, _ = os.path.splitext(os.path.basename(file))[0].split("-")
        text = process(file)
        data.append({"student_name": student_name, "text": text})

    dataframe = pd.DataFrame(data)
    instructions_file = os.path.join(directory, "instructions.txt")
    grades = grade_answers(dataframe, instructions_file)

    dataframe["grade"] = grades
    dataframe.to_excel(f"{directory}_grades.xlsx", index=False)

if __name__ == "__main__":
    main()
