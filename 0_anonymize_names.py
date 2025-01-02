import csv
from openai import OpenAI
from openai import AsyncOpenAI
import time
import os


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

input_file = 'names.csv'
output_file = 'names_with_alternates.csv'

# Function to query OpenAI API for an alternate name
def get_alternate_name(oldname):
    client = OpenAI()

    prompt = (
        f"Please provide an alternate full name for {oldname}. Change all parts, i.e. first name, last name, and all further parts."
        "Always maintain the same language/country and the same gender."
        "Try to choose names in a way that the name's character in terms of geographical and demographic distribution, age of person, and socio-cultural background remains the same."
        "As an answer, only provide the full name, nothing else."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    newname = response.choices[0].message.content.strip()
    print(f'{oldname} >> {newname}')
    return newname

# Read the CSV file and process each first name and last name pair
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    sourcelist = csv.reader(infile, delimiter=';')
    newlist = csv.writer(outfile, delimiter=';')
    
    # Write header to the output file
    newlist.writerow(['oldname', 'newname'])
    
    # Track used names to ensure uniqueness
    used_names = set()
        
    # Skip the header row in the input file if it exists
    next(sourcelist, None)
    
    # Process each row in the input file
    for row in sourcelist:
      
        oldname = row
        try:
            newname = get_alternate_name(oldname)
            
            # Ensure uniqueness
            while (newname in used_names):
                newname = get_alternate_name(oldname)
                used_names.add(newname)

        except Exception as e:
            print(f"Error fetching alternate names for {oldname}: {e}")
            newname = "Unknown"
        
        # Write the result to the output file
        newlist.writerow([oldname, newname])
        
        # To avoid hitting rate limits, add a short delay between requests
        # time.sleep(1)  # Adjust the sleep time as necessary

print("Processing complete. Results saved to names_with_alternates.csv.")
