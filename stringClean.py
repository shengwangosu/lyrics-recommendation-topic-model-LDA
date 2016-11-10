from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
#----------------------------------------------
def stringClean(raw):
	# input: a list of strings
	# output: a list of list of words
	#tokenizer=RegexpTokenizer(r'\w+')
	tokenizer = RegexpTokenizer('\w+\'?\w*') 	# match " We've "
	stopWords=get_stop_words('en')
	stopWords+=['ye','u','la','da','can','gonna','get','yo','na','oh','go','get','got','round',"ain't" ,'yeah','ya']
	stemmer=PorterStemmer()
	if type(raw) is list:
		ans=[]
		# operate on string and have it cleaned
		for r in raw:
			tokens=tokenizer.tokenize(r.lower())
			stopped = [t for t in tokens if not t in stopWords]		# remove common words such as: a, the, is, are
			stemmed = [stemmer.stem(t) for t in stopped] 			# reduces word to its root 
			ans.append(stemmed)
	else: # input is single string
		raw.lower()
		tokens=tokenizer.tokenize(raw.lower())
		stopped=[t for t in tokens if not t in stopWords]
		stemmed = [stemmer.stem(t) for t in stopped]
		ans=stemmed
	return ans
