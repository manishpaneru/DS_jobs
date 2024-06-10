import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# First let's read the data into the data frame , the csv is named DS_JOBs.csv, we are going to read is from pandas
df = pd.read_csv("DS_JOBS.csv")


# Let's see the overview of the data
df.head()


# Let's see some brief information about the dataset we have
df.describe()


# Let's see some more information about the dataset
df.info


# now let's have a look at the name of the columns in the dataset
print(df.columns)


# Let's remove 'Glassdoor est' from the salary estimation column , while we are at it let's remove '$' sign from the salary estimate
df["Salary Estimate"] = (
    df["Salary Estimate"]
    .astype(str)
    .str.replace("(Glassdoor est.)", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.replace("K", "", regex=False)
    .str.replace("-", " ", regex=False)
)


# let's see if the dataset has any duplicate and if so let's delete them
df.drop_duplicates(inplace=True)


# Let's check for the null values in the dataset, we will have a better idea of how much null value are in teh dataset
print(
    f"Missing values before dropping rows:\n{df.isnull().sum().to_markdown(numalign='left', stralign='left')}"
)


# let's drop the rows with null values in the `Job Title`, `Company Name`, and `Location` columns as they are most useful columns and having null values in these columns makes the row completly useless
df.dropna(subset=["Job Title", "Company Name", "Location"], inplace=True)


# Let's see first 5 rows of the data after all the cleaning steps
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))


df.head()


# It seems like the company name isn't properly formatted, there is \n in the Company Name column and we are gonna reamove this
df["Company Name"] = df["Company Name"].str.split("\n").str[0]


# Let's remove index column as they are not necassary at all for our data cleaning project
df.drop(columns=["index"], inplace=True)


# Let's convert the Founded year and Rating column to numeric data types so that it will be easier to perform analysis later
df["Founded"] = pd.to_numeric(df["Founded"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")


# let's fill the missing values in foudned column with median of the columns values
df["Founded"] = df["Founded"].fillna(df["Founded"].median())


# Let's do something similar with Rating columns , let's fill the Rating columns with mean value of the columns
df["Rating"] = df["Rating"].fillna(df["Rating"].mean())


# As the Competitors columns is filled with string value , we can't fill null value with mean or medain , we are gonna fill null values in this columns with 'No value listed'.
# also let's replace '-1' in the Competitors columns as they also mean 'No competitors Listed'
df["Competitors"] = df["Competitors"].fillna("No Competitors Listed")
df["Competitors"] = df["Competitors"].replace("-1", "No Competitors Listed")


# Now we are gonna replace Unknown/Non-applicable with just unknown in the Revenue columns, Also replacing '-1' With unknown as they mean the same thing
df["Revenue"] = (
    df["Revenue"]
    .astype(str)
    .str.replace("Unknown / Non-Applicable", "Unknown", regex=False)
)
df["Revenue"] = df["Revenue"].replace("-1", "Unknown")


# Now that's done , let's change all the values of 'Job description' to lowercase
df["Job Description"] = df["Job Description"].astype(str).str.lower()


# Let's create a new column called 'Word Count' Which will tell us how many word count are there in the 'job Description' Columns
df["Word Count"] = df["Job Description"].str.split().str.len()


# Now let's extract 'City' and 'state' of a job from 'Location' Column
df["City"] = df["Location"].astype(str).str.split(", ").str[0]
df["State"] = df["Location"].astype(str).str.split(", ").str[1]


# Now let's create a new column called 'Company Age' by subtracting 'Founded' Year from 2024
df["Company Age"] = 2024 - df["Founded"]


# Let's create another columns that holds the word count of the 'Job title' and save it as 'Job Length'
df["Job Length"] = df["Job Title"].astype(str).str.len()


df.head()


# now that's done we can move on to something else,
# Let's create a few columns , let's see which key words are listed in the job description as it will make it easier for someone who uses this list
# This will show if the 'Job Description' has Key skills listed or not.
df["Python"] = df["Job Description"].str.contains("python", case=False)
df["R"] = df["Job Description"].str.contains(" r ", case=False)
df["SQL"] = df["Job Description"].str.contains("SQL|sql", case=False)
df["Spark"] = df["Job Description"].str.contains("spark", case=False)
df["AWS"] = df["Job Description"].str.contains("AWS|aws", case=False)
df["Excel"] = df["Job Description"].str.contains("excel", case=False)


df.head()


# Now let's standrarize columns with text datas , we can do that by simply change them to lowecase
df["Job Title"] = df["Job Title"].str.lower()
df["Company Name"] = df["Company Name"].str.lower()
df["Location"] = df["Location"].str.lower()


# Let's write code to simplify Job Title and save it into new column called 'Job Title Simplified' So that person looking for a job will have it easier
df["Job Title Simplified"] = df["Job Title"].str.replace(r"sr.|jr.|\s+", "", regex=True)


# Now let's create a new column that holds the data of the seniority of the job in the dataset, it seems for that we need to import re library
import re

seniority_pattern = r"\b(sr|jr|lead|manager)\b"
df["Seniority"] = (
    df["Job Title"]
    .str.extract(seniority_pattern, flags=re.IGNORECASE, expand=False)
    .fillna("na")
)


# Now that's done so now we can remove the seniority level from the job title
df["Job Title"] = (
    df["Job Title"].str.replace(seniority_pattern, "", regex=True).str.strip()
)


# let's create a new column that will count the number of competitors in the dataset
df["Num_Competitors"] = (
    df["Competitors"]
    .astype(str)
    .str.split(",")
    .apply(lambda x: len(x) if x != ["No Competitors Listed"] else 0)
)


# let's cerate 2 new columns that will show us minimum and maximum employees in the company provided in the dataset
df["Min Employees"] = (
    df["Size"]
    .astype(str)
    .str.split(" to ")
    .str[0]
    .str.replace("employees", "", regex=False)
    .str.replace("+", "", regex=False)
    .str.replace("Unknown", "0", regex=False)
)
df["Max Employees"] = (
    df["Size"]
    .astype(str)
    .str.split(" to ")
    .str[1]
    .str.replace("employees", "", regex=False)
    .str.replace("+", "", regex=False)
    .str.replace("Unknown", "0", regex=False)
)


# Now let's convert the data type of the newly created columns into numeric and let's fill the null value in those newly created columns with zero.
df["Min Employees"] = pd.to_numeric(df["Min Employees"], errors="coerce").fillna(0)
df["Max Employees"] = pd.to_numeric(df["Max Employees"], errors="coerce").fillna(0)


# Now let's create a new column that holds if the job in the dataset is Remote or not
df["Remote"] = df["Location"].astype(str).str.contains("remote", case=False)


# Now that we are done with the Data cleaning, I will create some data visualization so that I can better understand the dataset,
# and I will have some fun too


# Let's create a bar chart that will show us which cities have the most job posting.
plt.figure(figsize=(12, 6))
plt.bar(top_cities.index, top_cities.values)
plt.xlabel("City", fontsize=12)
plt.ylabel("Number of Job Postings", fontsize=12)
plt.title("Top 10 Cities with Most Job Postings", fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.show()


# Now let's create a pie chart, that will show us Which skills are included in the most proportion so I will know which Programming Languages are most necassary for Data Jobs
filtered_df = df[(df["Python"] == True) | (df["R"] == True) | (df["SQL"] == True)]
language_counts = filtered_df[["Python", "R", "SQL"]].sum()
plt.figure(figsize=(8, 8))
plt.pie(
    language_counts, labels=language_counts.index, autopct="%1.1f%%", startangle=140
)
plt.title("Distribution of Programming Languages in Job Postings", fontsize=14)
plt.show()


# Let's create a histogram that will show us
plt.figure(figsize=(10, 6))
plt.hist(df["Company Age"], bins=20, alpha=0.7, rwidth=0.85)
plt.xlabel("Company Age", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Distribution of Company Age", fontsize=14)
plt.show()


# Now let's create another data visualization , a sideways barchart that shows us which are the top 10 companies with the most Data job posting
top_companies = df["Company Name"].value_counts().head(10)
plt.figure(figsize=(12, 6))
plt.barh(top_companies.index, top_companies.values, color="skyblue")
plt.xlabel("Number of Job Postings", fontsize=12)
plt.ylabel("Company Name", fontsize=12)
plt.title("Top 10 Companies with Most Job Postings", fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()


# Now let's create a bar chart that shows us top 10 sector that have the most data jobs posting.
sector_counts = df["Sector"].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(sector_counts.index, sector_counts.values, color="salmon")
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Number of Job Postings", fontsize=12)
plt.title("Distribution of Job Postings by Sector", fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.show()
