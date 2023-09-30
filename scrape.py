from bs4 import BeautifulSoup
import requests
import pandas as pd
import random

userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.40',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    ]

companies_dictionary = {'Name': [], 'Location': [], 'Type': [], 'Website': [], 'Specialities': [], 'Size': [], 'Founded': [], 'Status': [], 'Followers on Stack Overflow':[]}

def scrape(companies):
    for company in companies:
        Name = company.find('a').text
        companies_dictionary['Name'].append(Name)
        
        location_type = company.find_all('div', class_ = 'flex--item fc-black-500 fs-body1')
        
        companies_dictionary['Location'].append(location_type[0].text)
        companies_dictionary['Type'].append(location_type[1].text)
        
        specialities = company.find_all('a', class_ = 'flex--item s-tag no-tag-menu')
        
        specialities_text = ''
        
        for i in range(0, len(specialities)):
            specialities_text = specialities_text + ', ' + specialities[i].text
            
        companies_dictionary['Specialities'].append(specialities_text)
        
        link = company.find('a')['href']
        company_text = requests.get('https://stackoverflow.com' + link, headers = random.choice(userAgents)).text
        soup = BeautifulSoup(company_text, 'lxml')
        
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

for page in range (1, 12):
    html_text = requests.get('https://stackoverflow.com/jobs/companies?pg=' + str(page), headers = random.choice(userAgents)).text
    soup = BeautifulSoup(html_text, 'lxml')

    companies = soup.find_all('div', class_ = 'flex--item fl1 text mb0')
    
    scrape(companies)

    
companies_dataframe = pd.DataFrame(companies_dictionary)

companies_dataframe['Specialities'] = companies_dataframe['Specialities'].apply(lambda x: x[2:])
companies_dataframe['Size'] = companies_dataframe['Size'].apply(lambda x: x.replace('  ', ''))
companies_dataframe['Founded'] = companies_dataframe['Founded'].apply(lambda x: x.replace('  ', ''))
companies_dataframe['Status'] = companies_dataframe['Status'].apply(lambda x: x.replace('  ', ''))
companies_dataframe['Followers on Stack Overflow'] = companies_dataframe['Followers on Stack Overflow'].apply(lambda x: x.replace('  ', ''))

companies_dataframe.to_csv('companies.csv')