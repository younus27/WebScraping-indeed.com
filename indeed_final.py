from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


data = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Description","Date","hiring"])
end = 5000

for page in range(0,end,10):
	e = end//10
	p = (page+10)//10
	print(f'Scraping Page {p} / {e} ...')

	source = requests.get('https://www.indeed.co.in/jobs?q=all+types&sort=date&start={}'.format(page)).text
	
	soup = BeautifulSoup(source,'lxml')

	for jobs in soup.find_all(class_ = 'result'):
		flag = 0

		try:
			title = jobs.h2.a.text.strip()
			link = 'https://www.indeed.co.in'+ jobs.h2.a['href']
			flag = 1
		except Exception as e:
			title = None
			link = None

		try:
			location = jobs.find(class_ = 'location').text.strip()
		except Exception as e:
			location = None
		#print('Location:\t',location)

		try:
			company = jobs.find('span',class_ = 'company').text.strip()
		except Exception as e:
			company = None
		#print('Company:\t',company)

		try:
			salary = jobs.find(class_="salary").text.replace("\n", "").strip()
		except Exception as e:
			salary = None
		# print('Salary:\t\t',salary)


		try:
			date = soup.find(class_="date").text.replace("\n", "").strip()
			if date == '30+ days ago':
				break
		except Exception as e:
			date = 'None'

		#print('Date:\t',date)

		try:
			urgent = jobs.find(class_="jobCardShelfItem urgentlyHiring").text.replace("\n", "").strip()
		except Exception as e:
			urgent = 'None'
		#print('Urgent:\t',urgent)

		if (flag):
			s= requests.get(link).text
			desc  = BeautifulSoup(s,'lxml')
		try:
			job_desc = desc.find('div',class_ = 'jobsearch-jobDescriptionText').text.strip()
		except Exception as e:
			job_desc = None


		#print('\n-----------------------------------------------\n')
            
		data = data.append({'Title': title, 'Location': location, "Company": company, "Salary": salary,"Description": job_desc, "Date": date, "hiring": urgent}, ignore_index=True)
		data.to_csv('last.csv',index = False) 
		# print(data)

	time.sleep(2)
