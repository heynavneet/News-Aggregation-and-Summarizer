from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
def news_url(URL):
	# URL = 'https://news.google.com/topstories'
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	content = soup.findAll('article')
	url = []

	for article in content:
		u = article.find('a', href=True)
		u1 = u['href']
		u2 = 'https://news.google.com'+u1[1:]
		url.append(u2)
	return(url)	

from newspaper import Article
def scrap_summary(urls):
# url = 'https://news.google.com/articles/CBMiPmh0dHBzOi8vd3d3LnNub3Blcy5jb20vZmFjdC1jaGVjay9jZGMtaGFsdHMtdXMtamotY292aWQtc2hvdHMv0gEA?hl=en-IN&gl=IN&ceid=IN%3Aen'
	dec = {}
	for url in urls:
		article = Article(url)
		article.download()
		article.html
		article.parse()
		article.nlp()
		# print(article.text,"\n")
		# print("title:")
		# print(article.title )
		# print("---- Summary ----")
		# print(article.summary)
		title = article.title
		summ = article.summary
		img = article.top_image
		dec.update({title:{'summary':summ, 'img':img, 'url':url}})
	return(dec)

s_url = news_url('https://news.google.com/topstories')
s_summary = scrap_summary(s_url)
# print(s_summary)




from main import db, News

for k,v in s_summary.items():
	t=k
	s=v['summary']
	i=v['img']
	u=v['url']

	q=News(title=t, context=s, imag=i, url=u)
	news = News.query.all()
	for i in news:
		if i.title == t:
			pass
		else:	
			db.session.add(q)
			db.session.commit()