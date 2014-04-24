import urllib3
from bs4 import BeautifulSoup
import textwrap

connect = urllib3.PoolManager()

def extractor(webpage, structure=True, Title=True, Text=True, linelength=70):
	try:
		soup = BeautifulSoup(webpage)

		if Title:
			print "_"*20+"\n"+"Here is the title :\n","_"*20+"\n"+(soup.title.string).encode("utf-8")

		if Text:
			try:
				print "_"*20+"\n"+"Here is the Text :\n","_"*20+"\n"
				informal_structure = []
				reduced_structure = []
				max = 0
				most_important = ""
				for text in soup.find_all(["p","h1","h2","span"]):
					informal_structure.append([text.parent.attrs.items(), len(("".join(text.findAll(text=True))).encode("utf-8"))])
				for keys in informal_structure:
					if str(keys[0]) in str(reduced_structure) :
						reduced_structure[reduced_structure.index(str(keys[0]))+1] += keys[1]
					else:
						reduced_structure.append(str(keys[0]))
						reduced_structure.append(keys[1])
				for items in xrange(1,len(reduced_structure),2):
					if reduced_structure[items] > max and "comment" not in str(reduced_structure[items-1]) and not\
						reduced_structure[items-1] == "[]":
						max = reduced_structure[items]
						most_important = str(reduced_structure[items-1])

				for text in soup.find_all(["p","h1","h2","span"]):
					# print "debug : "+most_important
					# print "text : \n",text
					if most_important in str(text.parent.attrs.items()):
						for element in textwrap.wrap(("".join(text.findAll(text=True))).encode("utf-8"),linelength):
							print "final : "+str(element)

			except Exception, e:
				print "There was an error in the Text Field",e

		if structure:
			print "_"*20+"\n"+"Here is the file structure :\n",(soup.prettify()).encode("utf-8")
	except Exception, error:
		print ("There was an error in the extractor function : ",error)



urls = ("http://www.lefigaro.fr/politique/2014/04/24/01002-20140424ARTFIG00355-plan-d-economies-le-ps-menace-de-sanctionner-les-deputes-frondeurs.php",
	"http://www.bloomberg.com/news/2014-04-24/e-cigarettes-to-fall-under-fda-review-as-popularity-grows.html",
	"http://www.reuters.com/article/2014/04/24/us-amazoncom-results-idUSBREA3N20J20140424")

for url in urls:
	http = connect.request("GET", url)
	extractor(http.data, structure=False, Text=True)