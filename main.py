import requests
from bs4 import BeautifulSoup
import time
# ---------------------------------

#Can edit base on user input but for now using fixed url
baseURL = "https://www.jobstreet.com.sg"
jobName = "/software-developer-jobs"
location = "/in-Singapore"

jobTitles = []
jobPTimes = []
jobLevel = []
jobURLList = []
jobCompany = []
jobQuali = []
jobLocation = []

sURL = baseURL + jobName + location
response = requests.get(sURL)
soup = BeautifulSoup(response.text, "html.parser")

#Get job title
job_titles = soup.find_all("h1", class_="z1s6m00")
for t in job_titles:
    t = t.text.strip()
    jobTitles.append(t)

#Get job post time
job_pTimes = soup.find_all("time", class_="z1s6m00")
for pT in job_pTimes:
    times = str(pT["datetime"]).split("T")[0]
    jobPTimes.append(times)

#Get company name
job_Comp = soup.find_all("a", class_="_6xa4xb0")
for comps in job_Comp:
    job_compLink = comps.get('data-automation')
    if "jobCardCompanyLink" in job_compLink:
        jobCompany.append(comps.text.strip())
    elif "jobCardLocationLink" in job_compLink:
        jobLocation.append(comps.text.strip())

#For each job link, get job level and job qualification
job_links = soup.find_all("a", class_="z1s6m00")
for link in job_links:
    job_link = link.get('href')
    if "jobId" in job_link:
        jobURL = baseURL + job_link  # job url
        jobURLList.append(jobURL)
        response = requests.get(jobURL)
        soup = BeautifulSoup(response.text, "html.parser")

        time.sleep(1)
        try:
            job_Level = soup.find(string="Career Level").findNext('span').text.strip()
            jobLevel.append(job_Level)

            job_Qual = soup.find(string="Qualification").findNext('span').text.strip()
            jobQuali.append(job_Qual)
        except:
            print("")

#Total should be 30 jobs (1 page) but some how job location keeps coming back 29 (its ignoring 1)
#Can use range to 30 to loop through and add each into excel
print(len(jobTitles))
print(len(jobPTimes))
print(len(jobLevel))
print(len(jobURLList))
print(len(jobCompany))
print(len(jobQuali))
print(len(jobLocation))

