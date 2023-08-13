# AutoGrader
Problem:  I lose my wife for 1-2 weeks 3x per year (each trimester) to grade assignments across 600+ students from grades 1-6.

Solution: Use AI to automate grading.
 
Inspiration:
https://techcommunity.microsoft.com/t5/educator-developer-blog/empowering-educators-automated-assignment-scoring-via-azure/ba-p/3828127

Source code as reference:  https://github.com/wongcyrus/AzureOpenAIChatGTPAutoGrader


Details:
Since I am using AI, I want to ask ChatGPT-3 to write the code for me.  See chatgpt_grading_program_prompt.txt.
	
The Python program simply takes the docx files in a subdirectory, converts them one at a time to text, then sends the text along with the contents of the instructions.txt file in the subdirectory to ChatGPT.
	
PFA the program (with my api key scrubbed) as grading_chatgpt3_1_edit2_noapi.py.
	
PFA Thanksgiving Writing_grades_chatgpt35-turbo_cleannames.xlsx with the names removed for privacy to see the ChatGPT responses.

 
Notes:
I initially tried to do this with Bard, but the code from Bard was unusable without significant rework.  I kept asking Bard to fix the code and it kept sending me in loops of unusable code so I finally gave up.
	
ChatGPT gave much better code with almost no fixes required.  The amusing part was that the the only part ChatGPT struggled with was the ChatGPT API calls itself.
	
I made another version that uses text-davinci-003 instead of gpt-3.5-turbo, but the results were not as good.
 
Finally, this demonstration is a decent template for any batch analysis that you might want to do with ChatGPT.  It doesn't have to be docx files.  Anything that can reasonably be converted to text (even xlsx files converted to csv) could be evaluated by ChatGPT for a variety of purposes using this as a starting point.
