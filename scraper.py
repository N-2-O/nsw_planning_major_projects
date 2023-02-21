# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html
import os
import requests
import cssselect
import datetime

base_html = "http://www.planningportal.nsw.gov.au"

#get html from source
def get_applications():
	#pretend to be an ipad to bypass cloudflare protection with user-agent
	userAgent = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
	return scraperwiki.scrape("http://www.planningportal.nsw.gov.au/major-projects/projects?status=Exhibition","",userAgent) #on exhibition only!

#extract needed data from html
def get_data(data):
	root = lxml.html.fromstring(data).find('body')
	applications = root.cssselect("div[class='card__content']")
	for i in applications:
		refId = i.cssselect("div[class='field field-field-case-id field-type-string field-label-hidden']")
		address = i.cssselect("div")
		council = i.cssselect("span[class='card__sub']")
		name = i.cssselect("h3[class='card__title']")
		link = i.cssselect("a[href]")
		time = datetime.datetime.now().strftime("%x")
		thisApplication = {
			"council_reference" : ''.join(refId[0].itertext()).strip(),
			"address" : ''.join(address[6].itertext()).strip(),
			"council" : ''.join(council[0].itertext()).strip(),
			"description" : ''.join(name[0].itertext()).strip(),
			"info_url" : base_html + ''.join(link[0].items()[0][1]),
			"date_scraped" : time
		}
		try:
			store_data(thisApplication)
		except Exception as e:
			print("Could not save\n")
			raise e

def store_data(application):
	scraperwiki.sql.save(unique_keys=['council_reference'], data=application, table_name="data")

# def store_db(data):
# 	for application in data:
# 		print(application)
# 		scraperwiki.sql.save(unique_keys=['council_reference'], data=application, table_name="data")
	
def main():
	html = get_applications()
	get_data(html)
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
