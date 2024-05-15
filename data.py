#!/usr/bin/env python
# coding: utf-8
## we are going to create a data cleaning python project for my portfolio, this is a data set that we found on Kaggle and I will post the link to the uncleaned data and my cleaned data in the last cell.
## Remember My intent is to change this data into a dataset that a prospective data scientists can look at and make a descision regarding his empoyment.
## SO we will make changes to this data accordingly. # Let's start by importing the necassary libraries for the project
import pandas as pd
import numpy as np
import datetime  # let's import the dataset that we are about to clean

df = pd.read_csv("DS_JOBS.csv")
# This is a dataset for data analytics jobs in US .#Let's have a look at the dataset huh.
df  # Let's code with cautions.
# let's make a list of what we wanna do to the data in the cleaning process
# Here is the list of action of the cleaning process
# 1) we are going to Remove duplicate records
# 2) we are going to Handle missing values in the dataset if any.
# 3) We are going to trim whitespace in the dataset
# 4) We are going to standrarize text and integer data
# 5) Make sure that each and every columns holds the correct data types.
# 6) Rename columns
# 7) Check for consistensy of the data types
# 8) remove the index column as it serves no proper purpose in this dataset
# 9) we are going to standrize the data type in salary estimate column
# 10) we are also gonna add a column that indicates the age of the company
# 11) we are also going to add a few columns that may be necassary for the data
# 12) As we a re making this a dataset that someone could look at and make a descision about their job hunt we are also gonna be adding some data as well. # Let's remove duplicate from the dataset.
df = df.drop_duplicates()
# Let's check if it worked or not
df  # Now handaling missing values , As this is gonna be a prospective jobs data, we can't have any missing values, so we are gonan drop any row that has even a single missing value
df = df.dropna(how="any")
# Now let's see if our code worked or not
df
# No issues here #now let's trim whitespace in the dataset
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
# Let's check if it works or not
df
# The code seems to work quite alright #let's standrazie text data. As this dataset has pretty standrad text data here. What I wanna do I, I want to remove the 'K' and
# (Glassdoor est.) from the salary estimate column as it doesn't make any sense
# So let's remove them
# df['SL'] = df['SL'].str.replace(r'\$|K|\s*\(Glassdoor est.\)', '', regex=True)
#  looks like the salary estimate column name itself has white space soo the above code didn't work
# let's change that
df.columns = df.columns.str.replace(" ", "")
# Now that the whitespace in columns has been changed, let's rename the column from Salary Estimate to SL so it will be easier
df.rename(columns={"SalaryEstimate": "SL"}, inplace=True)
# let's see if it worked
df
# Okay it worked #Now that the name of the columns has been changed Let's just standrize the data
df["SL"] = df["SL"].str.replace(r"\$|K|\s*\(Glassdoor est.\)", "", regex=True)
# Let's see if it worked or not
df
# Cool it seems to be working #After formatting the salary estimate data we ran into another problem and that is , we dont have the complete number
# we just have salary in thousands. soo let's change the salary to actual numbers
# let's define a function to that splits the data and also multiplies the numbers by thousand.
# def multiply_by_thousand(salary_range):
#   # First, let's Split the range into two numbers
#  low, high = salary_range.split('-')
# # Now we shall Multiply both numbers by 1000 and return the new range
# return f"{int(low) * 1000}-{int(high) * 1000}"
# Now that the function is defined
# let's Apply the function to each row in the 'SL' column
# df['SL'] = df['SL'].apply(multiply_by_thousand)
# let's see if this worked or not
# it didn't work as it seems we still have employers estimate in somewhere in the data in salary field. #let's fix that first
# let's remove the word(employers est. where relevant)
df["SL"] = df["SL"].str.replace(r"\s*\(Employer est.\)", "", regex=True)
# did it worked
df
# Looks like it did #Yeah it did work
df["SL"][310:320]  # Now let's do what we were doing berofre, let's multiply by 1000.
# let's define a function
def multiply_by_thousand(salary_range):
    low, high = salary_range.split("-")
    return f"{int(low) * 1000}-{int(high) * 1000}"


# let's Apply the function
df["SL"] = df["SL"].apply(multiply_by_thousand)
# let's see if it worked
df
# Yes it did
# God! Data Analysis is Fun. #the data doesn't seem to have any blank values but it does have -1 in place of blank value
# let's delete those rows with -1 values
# but first let's delete the column named compititors which doesn't play any value in the data cleaning adjenda
df = df.drop(columns=["Competitors"])
# let's see if it works
df
# seems like it worked #Now that there aren't many columns to change, let's also drop the index column as it serves no purpdfose
df = df.drop(columns=["index"])
# let's see of ot worked
df
# Cool it worked, This is going really well. #Now that the columns that would make any difference. Let's move to the other part of the analysis.
# As the data doesn't have any blank values but have -1 Let's delte them first.
df = df[df != -1].dropna()
# this ought to remove the rows with values with -1 from the data frame
# let's see if it worked
df
# huh it worked, I was really speculative about the it working. df#Now let's make another column titled 'Age_of_the_company' , the value of the column is the value of column Founded subracted from current year
# let's first find the current year, as we have already imported datetime library we can just use that
current_year = datetime.datetime.now().year
# Now that we have the current date and time let's find the age of the company
df["Age_of_the_company"] = current_year - df["Founded"]
# let's see if this works
df  # Now that we have the age of the company, we can just delete the year the comapany was founded, As it won't play role in further explorative analysis
# soo let's just delete the Founded column
df = df.drop(columns=["Founded"])
# Just some basic drop command, let's see if it worked
df
# Seems like it did work #Now let's see the minimum & maximum salary for each position , that would be really helpful for explorative analysis
df["Min_Salary"] = df["SL"].apply(lambda x: int(x.split("-")[0]))
# This code ought to take care of it, let's see if it worked
df
# Yeah! it worked #let's create another column called Max_salary, this will also be really helpful for the code
# This edi bidie code should take care of that.
df["Max_Salary"] = df["SL"].apply(lambda x: int(x.split("-")[1]))
# Let's see of this worked
df  # now that we have the max and min salary, let's see the average salary offered by the position, which statistically an candidate is likely to get.
# This should take care of that
df["average_salary"] = (df["Min_Salary"] + df["Max_Salary"]) / 2
# let's see if it works
df
# it works, hurray #Now I wanna create a column with the necassary skills for each job roles, For this I will have to find skills required for tje titles
# for that I am gonna need all the distinct values in the JobTitle column
distinct_job_titles = df[
    "JobTitle"
].unique()  # This code should find the distinctive value in the column and save it in a variable.
print(distinct_job_titles)  # This is pretty self-explanatory
# first let's create a key-value-pair table whihc has jobs with their related required skills, so that I can create a new column that has
# the required skills for each jobs.
jobs_skills = {
    "Sr Data Scientist": "Machine Learning, Statistics, Programming (Python, R)",
    "Data Scientist": "Statistics, Programming (Python, R), Data Analysis",
    "Data Scientist / Machine Learning Expert": "Machine Learning, Deep Learning, Programming (Python)",
    "Staff Data Scientist - Analytics": "Data Analysis, SQL, Data Visualization",
    "Data Scientist - Statistics, Early Career": "Statistics, Programming (R, Python), Data Mining",
    "Data Modeler": "Data Modeling, Database Design, SQL",
    "Experienced Data Scientist": "Machine Learning, Big Data, Cloud Computing",
    "Data Scientist - Contract": "Programming (Python, R), Statistics, Data Analysis",
    "Data Analyst II": "SQL, Data Analysis, Business Intelligence",
    "Medical Lab Scientist": "Biology, Chemistry, Laboratory Techniques",
    "Data Scientist/Machine Learning": "Machine Learning, Deep Learning, Programming (Python)",
    "Human Factors Scientist": "Ergonomics, Statistics, Experimental Design",
    "Business Intelligence Analyst I- Data Insights": "SQL, Data Visualization, Business Acumen",
    "Data Scientist - Risk": "Machine Learning, Statistics, Risk Modeling",
    "Data Scientist-Human Resources": "Statistics, Data Analysis, HR Analytics",
    "Senior Research Statistician- Data Scientist": "Statistics, Machine Learning, Research Methods",
    "Data Engineer": "Programming (Python, Java), Big Data, Cloud Computing",
    "Associate Data Scientist": "Programming (Python, R), Statistics, Data Mining",
    "Business Intelligence Analyst": "SQL, Data Visualization, Business Intelligence",
    "Senior Analyst/Data Scientist": "Machine Learning, Statistics, Data Analysis",
    "Data Analyst": "SQL, Data Analysis, Data Visualization",
    "Machine Learning Engineer": "Machine Learning, Deep Learning, Programming (Python)",
    "Data Analyst I": "SQL, Data Analysis, Excel",
    "Scientist - Molecular Biology": "Molecular Biology, Biochemistry, Laboratory Techniques",
    "Computational Scientist, Machine Learning": "Machine Learning, High Performance Computing, Programming (Python)",
    "Senior Data Scientist": "Machine Learning, Big Data, Cloud Computing",
    "Jr. Data Engineer": "Programming (Python, Java), SQL, Data Warehousing",
    "E-Commerce Data Analyst": "SQL, Data Analysis, Marketing Analytics",
    "Data Analytics Engineer": "Programming (Python, Java), SQL, Big Data",
    "Product Data Scientist - Ads Data Science": "Machine Learning, Statistics, Marketing Analytics",
    "Data Scientist - Intermediate": "Programming (Python, R), Statistics, Data Analysis",
    "Global Data Analyst": "SQL, Data Analysis, Business Intelligence",
    "Data & Machine Learning Scientist": "Machine Learning, Deep Learning, Programming (Python)",
    "Data Engineer (Remote)": "Programming (Python, Java), Cloud Computing, Big Data",
    "Data Scientist, Applied Machine Learning - Bay Area": "Machine Learning, Deep Learning, Programming (Python)",
    "Principal Data Scientist": "Machine Learning, Big Data, Leadership",
    "Business Data Analyst": "SQL, Data Analysis, Business Acumen",
    "Purification Scientist": "Chemistry, Chromatography, Laboratory Techniques",
    "Data Engineer, Enterprise Analytics": "Programming (Python, Java), Cloud Computing, Big Data",
    "Data Scientist 3 (718)": "Machine Learning, Statistics, Programming (Python)",
    "Real World Science, Data Scientist": "Statistics, Machine Learning, Clinical Research",
    "Data Scientist - Image and Video Analytics": "Machine Learning, Deep Learning, Computer Vision",
    "Data Science Manager, Payment Acceptance - USA": "Machine Learning, Leadership, Communication",
    "Data Scientist / Applied Mathematician": "Machine Learning, Statistics, Mathematics",
    "Patient Safety- Associate Data Scientist": "Statistics, Data Analysis, Healthcare Analytics",
    "(Sr.) Data Scientist -": "Machine Learning, Statistics, Programming (Python)",
    "Data Scientist, Kinship - NYC/Portland": "Machine Learning, Statistics, Social Network Analysis",
    "Applied Technology Researcher / Data Scientist": "Machine Learning, Research Methods, Programming (Python)",
    "Health Data Scientist - Biomedical/Biostats": "Statistics, Machine Learning, Healthcare Analytics",
    "Staff Data Scientist": "Machine Learning, Big Data, Cloud Computing",
    "Sr Data Engineer (Sr BI Developer)": "Programming (Python, Java), SQL, Data Warehousing",
    "Lead Data Scientist": "Machine Learning, Leadership, Communication",
    "RFP Data Analyst": "SQL, Data Analysis, Business Intelligence",
    "Software Engineer - Data Science": "Machine Learning, Programming (Python, Java), Software Engineering",
    "Data Analyst/Engineer": "Programming (Python, SQL), Data Analysis, Data Visualization",
    "NGS Scientist": "Genetics, Genomics, Laboratory Techniques",
    "Senior Data Engineer": "Programming (Python, Java), Cloud Computing, Big",
}

# Let's create a column called required_skills , and then match jobt titles with their required skills in the job_skills dictionary,
# Man i can;t remeber all the technical terms
df["required_skills"] = df["JobTitle"].map(jobs_skills)  # This should do it
# Let's see if I succeedded
# let's just print those two columns
print(
    df[["JobTitle", "required_skills"]]
)  # Cool it worked, let's see the whole data frame
df  # Let's move the required_skills column next to job title so that it would be easier for our analysis and any prospective job seeker
# For that we need to first get the index of job title column
job_title_index = df.columns.get_loc("JobTitle")
# Now that we have the index, let's move the required_skills column next to the job title column
df.insert(job_title_index + 1, "required_skills", df.pop("required_skills"))
# Let's see if this works or not, let's just print first few rows of the data frame
print(df.head())
# It works, Damn i am on fire today coding like crazy. #[Sighs] the data ceaning part is over. we should move on to the explorative data analysis part.
# i am gonna upload this code to GITHUB and maybe continue later from here or with completly different dataset for analysis part.
# Even if I did with this dataset I would continue from here
# And I know there are a lots of useless comments here, but this is how i talk and comment like these makes me feel like i am talkingto the dataset.
# Sounds really sill, but it helps me code better.
# I can be extemly professional just coding is like my personal meditation and I like to be mylself while coding.
# If my girlfriend is watching this.
# I love you alot my angel, I will soon be with you yo bug you all day and night, See ya soon princess.
# For all my audience.
# See Ya in my next analysis code repo.
