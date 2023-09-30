import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import openpyxl
import os.path
import matplotlib.pyplot as plt
import numpy as np

#Keywords
skills_keywords = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "Git",
    "Docker",
    "Kubernetes",
    "RESTful API",
    "AWS",
    "Azure",
    "Google Cloud",
    "Linux",
    "Unix",
    "Shell Scripting",
    "Data Structures",
    "Algorithms",
    "Object-Oriented Programming",
    "Functional Programming",
    "Frontend Development",
    "Backend Development",
    "Web Development",
    "Mobile App Development",
    "Database Design",
    "NoSQL",
    "Microservices",
    "Agile Development",
    "Scrum",
    "Kanban",
    "Continuous Integration",
    "Continuous Deployment",
    "Test-Driven Development",
    "DevOps",
    "Software Architecture",
    "Design Patterns",
    "Code Review",
    "Unit Testing",
    "Debugging",
    "Performance Optimization",
    "Security",
    "User Experience (UX)",
    "User Interface (UI) Design",
    "Version Control",
    "Dependency Management",
    "Documentation",
    "Problem Solving",
    "Collaboration",
    "Communication",
    "Teamwork",
    "Agile Methodologies",
    "Software Development Lifecycle",
    "Technical Debt Management",
    "Code Optimization",
    "Scalability",
    "Serverless Computing",
    "CI/CD Pipelines",
    "AI and Machine Learning",
    "Blockchain",
    "IoT",
    "Big Data",
    "Data Science",
    "Software Testing",
    "Automation Testing",
    "Containerization",
    "Scripting",
]

qualifications_keywords = [
    "Vocational",
    "Bachelor",
    "Master"
    "Doctoral",
    "PhD"
    "Certification",
    "Diploma"
]



# #--------------------------------------------------------------------------------------------------------

# By Yolanda
#Web scrap starts here
# baseURL = "https://www.jobstreet.com.sg"
# jobName = "/software-developer-jobs"
# location = "/in-Singapore?pg=3" #Can edit base on user input but for now using fixed url
#
# jobTitles = []
# jobPTimes = []
# jobLevel = []
# jobURLList = []
# jobCompany = []
# jobQuali = []
# jobSkill = []
# jobLocation = []
#
#
# print("Retriving data...This might take a while, please hold on...")
# for i in range(3, 5, 1):
#
#     sURL = baseURL + jobName + ("/in-Singapore?pg=%d"%i)
#     response = requests.get(sURL)
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     #Get job title
#     job_titles = soup.find_all("h1", class_="z1s6m00")
#     for t in job_titles:
#         t = t.text.strip()
#         jobTitles.append(t)
#
#     #Get job post time
#     job_pTimes = soup.find_all("time", class_="z1s6m00")
#     for pT in job_pTimes:
#         times = str(pT["datetime"]).split("T")[0]
#         jobPTimes.append(times)
#
#     #Get company name
#     job_Comp = soup.find_all("a", class_="_6xa4xb0")
#     for comps in job_Comp:
#         job_compLink = comps.get('data-automation')
#         if "jobCardCompanyLink" in job_compLink:
#             jobCompany.append(comps.text.strip())
#         elif "jobCardLocationLink" in job_compLink:
#             jobLocation.append(comps.text.strip())
#
#     #For each job link, get job level and job qualification
#     job_links = soup.find_all("a", class_="z1s6m00")
#     for link in job_links:
#         job_link = link.get('href')
#         if "jobId" in job_link:
#             jobURL = baseURL + job_link  # job url
#             jobURLList.append(jobURL)
#             response = requests.get(jobURL)
#             soup = BeautifulSoup(response.text, "html.parser")
#
#             time.sleep(0.5) #May not scrap properly if no wait time
#             try:
#                 #Get job level
#                 job_Level = soup.find(string="Career Level").findNext('span').text.strip()
#                 jobLevel.append(job_Level)
#
#                 #Get job qualifications
#                 job_Qual = soup.find(string="Qualification").findNext('span').text.strip()
#                 jobQuali.append(job_Qual)
#
#                 # Get job skills
#                 job_skills = soup.find_all("li")
#                 mySkills = ""
#                 for s in job_skills:
#                     mySkills = mySkills + s.text.strip() + ","
#                 jobSkill.append(mySkills)
#
#             except:
#                 print("")

#Web scrap ends here

# #--------------------------------------------------------------------------------------------------------

# By Andrea:
#Save scrapped data into an excel
# def excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali, jobLocation, jobSkill,jobURLList,fileName):
#     # creating excel headers
#     columns = ['Job Title', 'Post Time', 'Job Level', 'Company Name', 'Qualifications','Location', 'Skills','Job URL']
#     # Creating dataframe for pandas to convert into excel
#     df = pd.DataFrame(list(zip(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList)), columns=columns)
#     # Convert dataframe into excel
#     newfileName = fileName + ".xlsx"
#     df.to_excel(newfileName)
#
# #calling functions to convert data into dataframe then excel
# excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList, "Jobs")
# print("Done!")

# #--------------------------------------------------------------------------------------------------------

# By Yolanda:
#Split the respective job levels and unfiltered skills
def splitSkillsIntoJobLevel():
    df = pd.read_excel('jobs.xlsx')
    df1 = df[df.duplicated('Job Level', keep=False)].groupby('Job Level')['Skills'].apply(list).reset_index()
    df2 = df[df.duplicated('Job Level', keep=False)].groupby('Job Level')['Qualifications'].apply(list).reset_index()

    with pd.ExcelWriter(
            "./Jobs.xlsx",
            mode="a",
            engine="openpyxl",
            if_sheet_exists='replace'
    ) as writer:
        for index, row in df1.iterrows():
            mys = pd.Series(row[1])
            myf = mys.to_frame()
            df1 = pd.DataFrame(myf)
        for index, row in df2.iterrows():
            mys = pd.Series(row[1])
            myf = mys.to_frame()
            df2 = pd.DataFrame(myf)
            df3 = df1.join(df2,how='right',lsuffix='1', rsuffix='2')
            df3.to_excel(writer, sheet_name=str(row[0]))

# --------------------------------------------------------------------------------------------------------

#By Yolanda:
#Filter skills required
def refineSkillsReq(SheetName):
    xls = pd.ExcelFile('Jobs.xlsx')
    df1 = pd.read_excel(xls,SheetName)
    myList = []
    # myotherList = []
    for index, row in df1.iterrows():
        tryThis = row[1]
        tryThis = str(tryThis).split(",")
        for s in skills_keywords:
            for t in tryThis:
                if s in t:
                    myList.append(s)

        # tryThisToo = row[2]
        # tryThisToo = str(tryThisToo).split(",")
        # for s in tryThisToo:
        #     for t in qualifications_keywords:
        #         s = s.strip()
        #         if t in s:
        #             if s not in myotherList:
        #                 myotherList.append(s)



    with pd.ExcelWriter(
            "./Jobs.xlsx",
            mode="a",
            engine="openpyxl",
            if_sheet_exists='replace'
    ) as writer:
        col = ['Skills']
        df = pd.DataFrame(list(myList),columns=col)
        df.to_excel(writer, sheet_name=SheetName)

# --------------------------------------------------------------------------------------------------------

# By Yolanda:
# Filter skills required
def getPopularSkills():
    SkillsReq = []
    xls = pd.ExcelFile('Jobs.xlsx')
    df1 = pd.read_excel(xls, 'Sheet1')

    for index, row in df1.iterrows():
        tryThis = row[7]
        tryThis = str(tryThis).split(",")
        for s in skills_keywords:
            for t in tryThis:
                if s in t:
                    SkillsReq.append(s)

    df = pd.DataFrame(SkillsReq)
    df_new = df.rename(columns={0: 'Skills'})
    plotGraphAll(df_new)

# --------------------------------------------------------------------------------------------------------

#By Yolanda
#Produce graph of popular skills
def plotGraph(SheetName):
    xls = pd.ExcelFile('Jobs.xlsx')
    df1 = pd.read_excel(xls, SheetName)
    df1.Skills.value_counts().plot(kind='barh')
    plt.title('Popular Skills for %s Software Engineering jobs'%SheetName)
    plt.show()

#--------------------------------------------------------------------------------------------------------

#By Yolanda
#Produce graph of popular skills
def plotGraphAll(df):
    df.Skills.value_counts().plot(kind='barh')
    plt.title('Popular Skills for a software engineer')
    plt.show()

#--------------------------------------------------------------------------------------------------------

#Update all excels with their respective skill requirements
tabs = pd.ExcelFile('Jobs.xlsx').sheet_names

for i in range(1, len(tabs), 1):
    refineSkillsReq(tabs[i])

#--------------------------------------------------------------------------------------------------------


splitSkillsIntoJobLevel()
getPopularSkills()