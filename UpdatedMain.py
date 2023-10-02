import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt

#Keywords
SEskills_keywords = [
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
    "User Experience (UX)",
    "User Interface (UI) Design",
    "Version Control",
    "Dependency Management",
    "Agile Methodologies",
    "Software Development Lifecycle",
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

IEskills_keywords = [
    "Cybersecurity",
    "Information Security",
    "Network Security",
    "Security Architecture",
    "Penetration Testing",
    "Vulnerability Assessment",
    "Incident Response",
    "Security Policies",
    "Risk Assessment",
    "Security Auditing",
    "Firewalls",
    "Intrusion Detection System",
    "IDS",
    "Intrusion Prevention System",
    "IPS",
    "Security Awareness",
    "Encryption",
    "Access Control",
    "Security Compliance",
    "Security Protocols",
    "Security Analysis",
    "Security Incident Management",
    "Security Operations",
    "Identity and Access Management",
    "IAM",
    "Information Security Manager",
    "Certified Ethical Hacker",
    "Information Systems Auditor",
    "Cloud Security Professional",
    "Security Tools",
    "Intrusion Detection and Prevention Systems",
    "IDPS",
    "Antivirus Software",
    "Firewall Management",
    "Network Monitoring",
    "Forensic Analysis",
    "Malware Analysis",
    "Data Loss Prevention",
    "DLP",
    "Security Patch Management",
    "Security Awareness Training",
    "Security Risk Management",
    "Secure Coding Practices",
    "Cloud Security",
    "Mobile Device Security",
    "Wireless Network Security",
    "Physical Security",
    "Business Continuity Planning",
    "Disaster Recovery Planning",
    "Security Consulting",
    "Security Governance",
    "Security Metrics and KPIs",
    "Threat Intelligence",
    "Security Awareness Programs",
    "Security Best Practices",
    "Cybersecurity Frameworks",
    "Security Assessment",
    "Security Compliance",
    "Security Strategy",
]

Q_keywords = [
    "Vocational",
    "Bachelor",
    "Master"
    "Doctoral",
    "PhD"
    "Certification",
    "Diploma"
]


baseURL = "https://www.jobstreet.com.sg"
location = "/in-Singapore?pg=3"

jobTitles = []
jobPTimes = []
jobLevel = []
jobURLList = []
jobCompany = []
jobQuali = []
jobSkill = []
jobLocation = []

# ----------------------------------------FUNCTIONS START HERE----------------------------------------
# ------------------------------------WEB SCRAP FUNCTION STARTS HERE------------------------------------
def scrapData(jobName):

    jobTitles.clear()
    jobPTimes.clear()
    jobLevel.clear()
    jobURLList.clear()
    jobCompany.clear()
    jobQuali.clear()
    jobSkill.clear()
    jobLocation.clear()

    print("Retriving data...This might take a while, please hold on...")


    sURL = baseURL + jobName + location
    response = requests.get(sURL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get job title
    job_titles = soup.find_all("h1", class_="z1s6m00")
    for t in job_titles:
        t = t.text.strip()
        jobTitles.append(t)

    # Get job post time
    job_pTimes = soup.find_all("time", class_="z1s6m00")
    for pT in job_pTimes:
        times = str(pT["datetime"]).split("T")[0]
        jobPTimes.append(times)

    # Get company name
    job_Comp = soup.find_all("a", class_="_6xa4xb0")
    for comps in job_Comp:
        job_compLink = comps.get('data-automation')
        if "jobCardCompanyLink" in job_compLink:
            jobCompany.append(comps.text.strip())
        elif "jobCardLocationLink" in job_compLink:
            jobLocation.append(comps.text.strip())

    # For each job link, get job level and job qualification
    job_links = soup.find_all("a", class_="z1s6m00")
    for link in job_links:
        job_link = link.get('href')
        if "jobId" in job_link:
            jobURL = baseURL + job_link  # job url
            jobURLList.append(jobURL)
            response = requests.get(jobURL)
            soup = BeautifulSoup(response.text, "html.parser")

            time.sleep(0.5)  # May not scrap properly if no wait time
            try:
                # Get job level
                job_Level = soup.find(string="Career Level").findNext('span').text.strip()
                jobLevel.append(job_Level)

                # Get job qualifications
                job_Qual = soup.find(string="Qualification").findNext('span').text.strip()
                jobQuali.append(job_Qual)

                # Get job skills
                job_skills = soup.find_all("li")
                mySkills = ""
                for s in job_skills:
                    mySkills = mySkills + s.text.strip() + ","
                jobSkill.append(mySkills)

            except:
                print("")
# ----------------------------------------WEB SCRAP FUNCTION END HERE----------------------------------------

# By Andrea:
#Save scrapped data into an excel
def excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali, jobLocation, jobSkill,jobURLList,fileName):
    # creating excel headers
    columns = ['Job Title', 'Post Time', 'Job Level', 'Company Name', 'Qualifications','Location', 'Skills','Job URL']
    # Creating dataframe for pandas to convert into excel
    df = pd.DataFrame(list(zip(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList)), columns=columns)
    # Convert dataframe into excel
    newfileName = fileName + ".xlsx"
    df.to_excel(newfileName,index=False)
#--------------------------------------------------------------------------------------------------------

def plotGraphAll(df):
    df.Skills.value_counts().plot(kind='barh')
    plt.title('Popular Skills ')
    plt.show()
#--------------------------------------------------------------------------------------------------------

#By Yolanda
#Clean string to get skills for each position in each excel (job position)
def refineSkillsReq(excelName):
    excelName = excelName + '.xlsx'
    df1 = pd.read_excel(excelName)
    my2ndList = []
    mySkills = []
    for index, row in df1.iterrows():
        myList = []
        jobSkill = row[6]
        if jobSkill != '' :
            jobSkill = str(jobSkill).split(",")
            if excelName == 'SEJobs.xlsx':
                for s in SEskills_keywords:
                    for j in jobSkill:
                        if s in j:
                            mySkills.append(s)
                            if s not in myList:
                                myList.append(s)
            if excelName == 'IEJobs.xlsx':
                for s in IEskills_keywords:
                    for j in jobSkill:
                        if s in j:
                            mySkills.append(s)
                            if s not in myList:
                                myList.append(s)

            my2ndList.append(myList)
        else:
            my2ndList.append("")

    df1['Skills'] = my2ndList
    df1['Skills'] = df1['Skills'].astype(str).str.replace(r'[][]', '', regex=True)
    df1.to_excel(excelName,index=False)
    df = pd.DataFrame(mySkills)
    df_new = df.rename(columns={0: 'Skills'})
    plotGraphAll(df_new)



# -------------------------------------FUNCTIONS END HERE-------------------------------------

# ---------------------------------CALL OF FUNCTIONS STARTS HERE---------------------------------
jobName = "/software-developer-jobs"
scrapData(jobName)
excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList, "SEJobs")
print("Done!")


jobName = "/information-security-jobs"
scrapData(jobName)
excelConveter(jobTitles, jobPTimes, jobLevel, jobCompany, jobQuali,jobLocation, jobSkill, jobURLList, "IEJobs")
print("Done!")

refineSkillsReq('SEJobs')
refineSkillsReq('IEJobs')
# ---------------------------------CALL OF FUNCTIONS ENDS HERE---------------------------------



