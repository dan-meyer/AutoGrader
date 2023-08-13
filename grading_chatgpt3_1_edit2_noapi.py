#written by chatgpt3
#edited by Dan Meyer
import os
import argparse
import docx2txt
import pandas as pd
import openai
import openpyxl

# Set up OpenAI API credentials
openai.api_key = 'Your-API-Key'
dataframes = []

# Function to grade an answer using OpenAI GPT-3.5
def grade_answer(student_name, answer, grading_instructions):
    messages=[
        {"role": "system", "content": f"You are a grader providing feedback to {student_name}."},
        {"role": "user", "content": answer},
        {"role": "assistant", "content": grading_instructions}
    ]
    # Your grading logic goes here
    # Example: Use OpenAI API to grade the answer
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1600,
        n=1,
        stop=None,
        temperature=0.9
    )
    grade = response.choices[0].message.content.strip()
    return grade

# Function to grade all answers in the dataframe
def grade_answers(dataframe, grading_instructions):
    grades = []
    for index, row in dataframe.iterrows():
        student_name = row['Student Name']
        answer = row['Answer']
        grade = grade_answer(student_name, answer, grading_instructions)
        grades.append(grade)
    dataframe['Grade'] = grades
    return dataframe

# Parse the directory argument
parser = argparse.ArgumentParser(description='Grade student answers in docx format.')
parser.add_argument('directory', help='Directory containing docx files')
args = parser.parse_args()

directory = args.directory

# Get the grading instructions from the file
with open(os.path.join(directory, 'instructions.txt'), 'r') as instructions_file:
    grading_instructions = instructions_file.read()

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=['Student Name', 'Answer'])

# Iterate through the docx files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.docx'):
#        file_path = os.path.join(directory, filename)
        student_name, assignment_name = os.path.splitext(filename)[0].split(' - ')
        # Convert docx to text using docx2txt
        text = docx2txt.process(directory + filename)
        dataframes.append(pd.DataFrame({'Student Name': [student_name], 'Answer': [text]}))

# Concatenate all dataframes into a single dataframe
df = pd.concat(dataframes, ignore_index=True)

# Grade the answers
graded_df = grade_answers(df, grading_instructions)

# Save the grades to an Excel file
output_file = f'{assignment_name}_grades.xlsx'
graded_df.to_excel(output_file, index=False)
print(f"Grades saved to {output_file}.")
