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
	print(html.prettify())
	article = html.find_all("div", class_="article")[0]
	article.decompose()
	print(html.prettify())
	return html.prettify()

def generateArticlesContent():
	ret = '<div class="articles">\n'

	path = "content/articles/"

	for filename in os.listdir(path):
		if filename.endswith(".html"):
			ret += '	<div class="article">\n'
			content = open(os.path.join(path, filename), 'r').read()
			preview = createArticlePreview(content)
			ret += preview
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