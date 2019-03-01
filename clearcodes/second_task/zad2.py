import requests
from bs4 import BeautifulSoup
import difflib

'''
python -m http.server 8000 --bind 127.0.0.1
your command python -m http.server didn't work for me. also replaced ip in examples
unfortunately this script is working on your example
'''


def readingUrl(url):
	'''
	function to getting source code from websites and it's using BeautifulSoup to create object to find required
	information
	:param url: website address
	:return: BeautifulSoup object
	'''
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data, 'lxml')

	return soup

def titleFinding(soup):
	'''
	function to getting title from BeautifulSoup object
	:param soup: BeautifulSoup object
	:return: title
	'''
	title = soup.title
	for i in title:
		return i

def linksFinding(soup, url, state_url):
	'''
	function to getting links from sites
	if url will be with '/' it will cut,
	in every site loop is looking for <a href> and check that, links are similar to our url address.
	addresses that will pass first if, will be checking with requests library
	at the end im looking for duplicat with dfflib library
	:param soup: BeautifulSoup object
	:param url: address of the page that interests us (it's for while loop)
	:param state_url: basic address
	:return: url address of each checking, links is list with all links
	'''
	href = soup.find_all('a')
	links = []
	if state_url[-1] == '/':
		state_url = state_url[:-1]

	for tag in href:
		link = tag.get('href')
		if state_url in link:
			links.append(link)
		else:
			try:
				req = requests.get(state_url + link)
				if req.status_code == 200:
					links.append(state_url + link)
			except ValueError:
				continue
	duplicat = (difflib.get_close_matches(state_url, links, cutoff=0.9))
	if duplicat:
		links.remove(duplicat[0])

	return url, links

def site_map(urls_):
	'''
	function to getting results in dictiorany type, show all things like in pdf
	:param urls_: basic url address
	:return: dictionary with all possibilities, like titles, links, urls
	'''
	state_url = urls_
	list_with_duplicats = []
	url_site = readingUrl(urls_)
	title = titleFinding(url_site)
	url, links = linksFinding(readingUrl(urls_), urls_, state_url)
	list_with_duplicats.append([url, title, links])
	test_list = dict()
	test_list[url] = {'title': title, 'links': set(links)}
	a, b = len(list_with_duplicats), len(test_list)

	while a <= b:
		for line in links:
			url_site = readingUrl(line)
			title = titleFinding(url_site)
			url, links = linksFinding(readingUrl(line), line, state_url)
			test_list[url] = {'title': title, 'links': set(links)}
			list_with_duplicats.append([url, title, links])

		a, b = len(list_with_duplicats), len(test_list)

	print()
	return test_list


url_ = 'http://127.0.0.1:8000'

print(site_map(url_))