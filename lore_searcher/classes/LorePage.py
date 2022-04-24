import textwrap

class Page(object):
	
	def __init__(self, doc, termHits=[]):
		tmp = doc.split('<>')
		self.termHits = set(termHits)
		self.id = tmp[0]
		self.pageName = tmp[1]
		self.srcURL = tmp[2]
		self.imgURL = tmp[3]
		self.toc = tmp[4].split(',') # table of contents
		self.blurb = tmp[5]
		self.topics = parseTopics(tmp[6])

	def getSummary(self):
		return {
			'id': self.id,
			'name': self.pageName,
			'img': self.imgURL,
			'url': self.srcURL,
			'blurb': self.blurb,
			'topics': self.toc,
			'matched-terms': self.termHits
		}

	def getFull(self):
		return {
			'id': self.id,
			'name': self.pageName,
			'img': self.imgURL,
			'url': self.srcURL,
			'blurb': self.blurb,
			'topics': self.toc,
			'matched-terms': self.termHits,
			'topic-list': self.topics
		}

	# bound = max amount of characters per line
	def printSummary(self, bound):
		print(bound*"*" + "\n")
		title = f"{self.pageName.title()} (id: {self.id})\n"
		print(title.center(bound) + '\n')

		tmpTopics = ', '.join(self.toc)
		topicStr = tmpTopics[:bound - (len("Topics Included:") + 3)] + "..." if len(tmpTopics) > bound else tmpTopics
		print("Topics Included:", topicStr)

		blurb = self.blurb[:bound - 3] + "..." if len(self.blurb) > bound else self.blurb
		print(textwrap.fill(f"Description: {blurb}", width=bound))

		print("\nMatched Terms:", ", ".join(self.termHits))
		print(textwrap.fill(f"Source-URL: {self.srcURL}", width=bound))
		print(textwrap.fill(f"Img-URL: {self.imgURL}", width=bound))
		print("\n" + bound*"*")


	def printFull(self, bound):
		print(bound*"*" + "\n")
		title = f"{self.pageName.title()} (id: {self.id})\n"
		print(title.center(bound))
		print("Table of Contents:")
		print(len("Table of Contents:")*"-")
		for t in self.toc:
			print(f"|- {t.title()}")
		print("\n")

		for topic in self.topics:
			printTopic(topic, bound)

		if len(self.termHits) > 0:
			print("Matched Terms:", ", ".join(self.termHits))
		print(textwrap.fill(f"Source-URL: {self.srcURL}", width=bound))
		print(textwrap.fill(f"Img-URL: {self.imgURL}", width=bound))
		print("\n" + bound*"*")

def printTopic(topic, bound):
	topicName = topic['topic-name']
	topicParas = topic['paras'].strip() + "\n" if 'paras' in topic else ""
	topicLists = topic['lists'] if 'lists' in topic else []
	print(f"{topicName.title()}")
	print(bound*"-")
	
	if len(topicParas):
		print(textwrap.fill(topicParas, width=bound) + "\n")
	
	for tList in topicLists:
		for li in tList:
			print(textwrap.fill(f"- {li.strip()}", width=bound))

		print("\n")

def parseTopics(topicDoc):
	topics = []

	if '<TOPIC>' in topicDoc:
		tmpTopics = topicDoc.split('<TOPIC>')
	else:
		return topics

	for topic in tmpTopics:
		tmpDict = {}

		if '<NAME>' not in topic:
			continue

		tmpDict['topic-name'], docStr = topic.split('<NAME>')
		
		if '<PARAS>' in docStr:
			tmpDict['paras'], docStr = docStr.split('<PARAS>')

		if '<LIST>' in docStr:
			lists = docStr.split('<LIST>')[0:-1]
			tmpDict['lists'] = list(map(lambda x: x.split('<LI>')[0:-1], lists))

		topics.append(tmpDict)

	return topics

