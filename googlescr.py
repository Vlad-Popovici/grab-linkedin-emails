#PY script to get emails from linkedin specific URLs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#import re
import time
import csv

#regex for getting emails in case we need to use regex
#regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
#                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
#                   "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

driver = webdriver.Firefox()

#Open csv and read emails
with open('emaillist.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        adresa_mail = str(row['Email'].strip())

#Define the google search       
		all_urls = ['https://www.google.com/?gws_rd=ssl#q=%22' +adresa_mail+'%22']
		

		for url in all_urls:
			try:
				driver.get(url)
				time.sleep(2)
#Look for all links on the page
				link_from_google = driver.find_elements(By.XPATH, '//div/h3/a/@href')

#Stop if there are no more pages to check				
				if len(link_from_google.text) > 0 or not link_from_google.text[0].startswith('/'): 

					#Check if each address is shown 
					for link in link_from_google:
						driver.get(link_from_google[link])
						verifica_adresa = driver.find_element(By.XPATH, '//*[contains(text(),'%s')]' % adresa_mail)
						if adresa_mail in verifica_adresa.text:
							print adresa_mail + " <- Address was found on page %s" % link 
				  
				else:
					print adresa_mail + '<- This address was not found'	
			except:
				pass


	driver.close()
