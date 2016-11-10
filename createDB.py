# webscraping songlyrics.com to create dictionary of dictionaries
# {'artist':{'song_name':'lyric_contents'}}
import urllib2, requests, re,io
from bs4 import BeautifulSoup as BS
from url2string import url2string
import MySQLdb

def get_Artist_Title_Lyric(link='http://www.songlyrics.com/adele/someone-like-you-lyrics/'):
	return link.rsplit('/')[-3], link.rsplit('/')[-2][:-7], url2string(link)

chart='http://www.songlyrics.com/news/top-songs/'

yearRange=[]
for y in range(2010,1989,-1):
	yearRange.append(str(y))
	
dataBaseName ='lyrics'

db = MySQLdb.connect(host='localhost', user='root',passwd='?????', db=dataBaseName)

cursor = db.cursor()

for year in yearRange:
	r = requests.get(chart+year+'/')
	soup = BS(r.content)
	# now find all href of the form: http://www.songlyrics.com/artist-name/song-name-lyrics/
	for (i, link) in enumerate(soup.find_all('a', title=True, href=re.compile('http\:\/\/www.songlyrics\.com\/.+\/.+\-lyrics\/'))):
		try:
			artist, title, content = get_Artist_Title_Lyric(link['href'])
			print year, i, artist, title
			# must use %s for all fields, even those not string
			cursor.execute("""INSERT INTO lyricsBody (artist, title, year, lyric) VALUES (%s,%s,%s,%s)""", (artist, title, int(year), content))
		except:
			pass

db.commit()

cursor.execute("SELECT lyric FROM lyricsBody WHERE year='2011' AND artist='coldplay' AND title='paradise' ")
s= cursor.fetchall() 	# return a tulpe of tuple
s[0][0]					# give the correct string


		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
