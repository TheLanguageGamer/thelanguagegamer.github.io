import re
import os
from bs4 import BeautifulSoup

def addContent(name, content, template):

	return re.sub(r"\{ *\{ *" + name + r" *\} *\}", content, template)

def generateProjectsContent():
	ret = '<div class="projects">\n'

	path = "content/projects/"

	for filename in os.listdir(path):
		if filename.endswith(".html"):
			ret += '	<div class="project">\n'
			content = open(os.path.join(path, filename), 'r').read()
			ret += content
			ret += '\n	</div>'

	ret += '\n</div>'

	return ret

def createArticlePreview(text):
	html = BeautifulSoup(text, "html.parser")
	article = html.find_all("div", class_="article")[0]
	article.decompose()
	return html.prettify()

class Article(object):

	def __init__(self, text):
		self.html = BeautifulSoup(text, "html.parser")

		dates = self.html.find_all("div", class_="date")
		if len(dates) > 0:
			self.date = dates[0].text
		else:
			self.date = ""

	def preview(self):
		bodies = self.html.find_all("div", class_="article")
		if (len(bodies) > 0):
			bodies[0].decompose()
		return self.html.prettify()


def generateArticlesContent():
	ret = '<div class="articles">\n'

	path = "content/articles/"

	articles = []

	for filename in os.listdir(path):
		if filename.endswith(".html"):
			content = open(os.path.join(path, filename), 'r').read()
			article = Article(content)
			articles.append(article)

	articles.sort(key=lambda a : a.date)
	articles.reverse()

	for article in articles:
		ret += '	<div class="article">\n'
		ret += article.preview()
		ret += '\n	</div>'



	ret += '\n</div>'
	return ret

def run():

	indexTemplate = open("content/index.html", 'r').read()
	indexTemplate = addContent("projects", generateProjectsContent(), indexTemplate)
	indexTemplate = addContent("articles", generateArticlesContent(), indexTemplate)

	indexOutput = open("index.html", 'w')
	indexOutput.write(indexTemplate)
	indexOutput.close()

if __name__ == "__main__":
	run()