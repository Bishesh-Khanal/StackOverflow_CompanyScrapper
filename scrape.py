from bs4 import BeautifulSoup
import requests
import pandas as pd
import random

def scrapper(companies_dictionary, userAgents, page_start, page_end):
    for page in range (int(page_start), int(page_end)):
        html_text = requests.get('https://stackoverflow.com/jobs/companies?pg=' + str(page), headers = {'User-Agent': random.choice(userAgents)})
        print('Page Status Code: ', html_text.status_code)
        if(html_text.status_code == 403):
            print('Access denied')
            return pd.DataFrame(companies_dictionary)
        soup = BeautifulSoup(html_text.text, 'lxml')

        companies = soup.find_all('div', class_ = 'flex--item fl1 text mb0')
    
        for company in companies:
            Name = company.find('a').text
            companies_dictionary['Name'].append(Name)
            
            location_type = company.find_all('div', class_ = 'flex--item fc-black-500 fs-body1')
            
            companies_dictionary['Location'].append(location_type[0].text)
            companies_dictionary['Type'].append(location_type[1].text)
            
            link = company.find('a')['href']
            companies_dictionary['Link'].append(link)
            company_text = requests.get('https://stackoverflow.com' + link, headers = {'User-Agent': random.choice(userAgents)})
            print('Company Status Code: ', company_text.status_code)
            if(company_text.status_code == 403):
                print('Access denied')
                return pd.DataFrame(companies_dictionary)
            soup = BeautifulSoup(company_text.text, 'lxml')
            
            specialities_container = soup.find('div', class_ = 'd-flex gs4 mb16 fw-wrap')
            specialities = specialities_container.find_all('a')
            
            specialities_text = ''
            for speciality in specialities:
                specialities_text = specialities_text + ', ' + speciality.text
            companies_dictionary['Specialities'].append(specialities_text)
            
            additional = soup.find('div', class_ = 'ba bc-black-100 ps-relative p16 bar-sm')
            website = additional.find('a')['href']
            
            companies_dictionary['Website'].append(website)
            
            size_founded_status_followers = additional.find_all('span')
            
            i = 2
            try:
               size = size_founded_status_followers[i].text
               i = i + 1
            except:
                size = 'N/A'
            try:
                founded = int(size_founded_status_followers[i].text)
                i = i + 1
            except:
                founded = 'N/A'
            try:
                status = int(size_founded_status_followers[i].text)
                status = 'N/A'
            except:
                status = size_founded_status_followers[i].text
                i = i + 1
            try:
                followers = size_founded_status_followers[i].text
                i = i + 1
            except:
                followers = 'N/A'
                
            companies_dictionary['Size'].append(size)
            companies_dictionary['Founded'].append(str(founded))
            companies_dictionary['Status'].append(status)
            companies_dictionary['Followers on Stack Overflow'].append(followers)

    
    return pd.DataFrame(companies_dictionary)