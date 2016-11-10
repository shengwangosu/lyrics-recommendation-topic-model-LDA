## parse a link url to lyrics in string
## only compatible with lyrics.com html format
## input: url of link
## return lyrics in string
import urllib2, requests, re
from bs4 import BeautifulSoup as BS

def url2string(pageLink):
	
	header_info={'User-Agent': 'My terminal'}
	req = requests.get(pageLink, headers=header_info)
	soup = BS(req.text)
	#lyrics = soup.find_all('div', {'class':re.compile('lyrics')})  	# for genius.om
	#lyrics = soup.find_all('pre', {'id':re.compile('lyric-body-text')}) 	# for lyrics.com
	lyrics = soup.find_all('p', {'id':re.compile('songLyricsDiv')}) 	# for songlyrics.com
	# convert bs object to string
	lyrStr = str(lyrics)
	# remove tags and hyperlinks
	lyrStr=re.sub('<[^>]*>', '', lyrStr)		## remove tags
	lyrStr=re.sub('(\.)?(\\\\[rn])+', '. ', lyrStr)	## remove \\n and \\r
	lyrStr=re.sub('\[','',lyrStr)			## remove [
	lyrStr=re.sub('\]','.',lyrStr)			## remove ] and add . at the end
	lyrStr=re.sub('\\\\u2019','\'',lyrStr)
	lyrStr=re.sub(r';br /&gt;','',lyrStr)
	lyrStr=re.sub(r'&lt','',lyrStr)
	lyrStr=re.sub('\.\s\.', '.',lyrStr)
	lyrStr=re.sub('\?\.','?',lyrStr)
	lyrStr=re.sub('(\.)?(\s)?\\u201[cd]','',lyrStr)
	lyrStr=re.sub(r'\\','',lyrStr)
	lyrStr=re.sub(r'\:\.',':',lyrStr)
	return lyrStr




