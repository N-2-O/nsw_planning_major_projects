# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import datetime
from bs4 import BeautifulSoup

base_html = "http://www.planningportal.nsw.gov.au"

#get html from source
def get_applications(page):
	#pretend to be an ipad to bypass cloudflare protection with user-agent
	userAgent = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
	return scraperwiki.scrape("http://www.planningportal.nsw.gov.au/major-projects/projects?status=Exhibition&page={}".format(page),"",userAgent) #on exhibition only!

#extract needed data from html
def get_data(data):
	page = BeautifulSoup(data, "html.parser")
	applications = []
	for table in page.find_all(class_="card__content"):
		refId = table.find(class_ = "field field-field-case-id field-type-string field-label-hidden").get_text().strip()
		address = table.find(class_ = "card__title").find_next_sibling().get_text().strip()
		council = table.find(class_ = "card__sub").get_text().strip()
		name = table.find(class_ = "card__title").get_text().strip()
		link = table.find("a", href = True)["href"]
		time = datetime.datetime.now().strftime("%x")
		# print("Reference ID:\t", refId)
		# print(">\tAddress:\t", address)
		# print(">\tCouncil:\t", council)
		# print(">\tDescription:\t", name)
		# print(">\tLink:\t", link)
		# print(">\tTime:\t", time)
		# print("-------------------------------")
		thisApplication = {
			"council_reference" : refId,
			"address" : address,
			"council" : council,
			"description" : name,
			"info_url" : base_html + link,
			"date_scraped" : time
		}
		applications.append(thisApplication)
	return applications

def store_data(application):
	scraperwiki.sql.save(unique_keys=['council_reference'], data=application, table_name="data")

def visit_pages():
	applications = []
	page = 0
	html = get_applications(page)
	apps = get_data(html)
	while apps:
		applications.extend(apps)
		page = page + 1
		html = get_applications(page)
		apps = get_data(html)
	return applications

def main():
	applications = visit_pages()
	
	for app in applications:
		print(app)
	quit()

main()

#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".