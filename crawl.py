from bs4 import BeautifulSoup
import urllib2
import csv

url = 'https://www.usa.gov/federal-agencies/a'
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html,"lxml")

urls=[]

#finding all list of agencies in <a> tag

list_of_agencies = soup.find("ul", {"class":"one_column_bullet"}).find_all('a')

for agencie in list_of_agencies:
	urls.append("https://www.usa.gov"+(agencie.get('href')))

writer = csv.writer(open('crawl.csv', 'wb'))

for url in urls:
	response = urllib2.urlopen(url)
	html = response.read()
	new_soup = BeautifulSoup(html,"lxml")
	
	

#finding all Names of the agencies

	name = new_soup.find("div",{"class":"col-md-9"}).find('h1').string
	
#finding Agencies who have acronyms

	if new_soup.find("h3", text="Acronym:") is not None:
		acronym = new_soup.find("h3", text="Acronym:").find_parent("section").find('p').get_text(" ", strip=True)
	else :
		acronym = "none"


#finding Agencies who have websites

	if new_soup.find("h3", text="Website:") is not None:
		website = new_soup.find("h3", text="Website:").find_parent("section").find('a').get('href')
	else:
		website = new_soup.find("h3", text="Official Name:").find_parent("section").find('a').get('href')

#finding address first using class:street-address but all pages dont have that so again searched using text

	if new_soup.find('p',{'class':'street-address'}) is not None:
		address = new_soup.find('p',{'class':'street-address'}).get_text(" ", strip=True)
	elif new_soup.find("h3", text="Main Address:") is not None:
	 	address = new_soup.find("h3", text="Main Address:").find_parent("section").find('p').get_text(" ", strip=True)
	else :
		address ="none"

#finding phone first using class:tel but all pages dont have that so again searched using text

	if new_soup.find('p',{'class':'tel'}) is not None:
		phone = new_soup.find('p',{'class':'tel'}).get_text(" ", strip=True)
	elif new_soup.find("h3", text="Phone Number:") is not None:
		phone = new_soup.find("h3", text="Phone Number:").find_parent("section").find('p').get_text("|", strip=True)
	else :
		phone ="none"


#finding Agencies who have contacts

	if new_soup.find("h3", text="Contact:") is not None:
		all_contacts = new_soup.find("h3", text="Contact:").find_parent("section").find_all('a')
#as contacts are more than one
		contact = []
		for contacts in all_contacts:
			contact.append(contacts.get_text(" ", strip=True))
			contact.append(contacts.get('href'))
	else:
		contact.append('none')
	writer.writerow([name,url,acronym,website,address,phone,contact])
