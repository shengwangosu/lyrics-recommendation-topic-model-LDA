import MySQLdb, gensim
from gensim import corpora, models, similarities
from url2string import url2string
from stringClean import stringClean
#-------------------------------------get lyric---------------------------------------
user_lyric = url2string('http://www.songlyrics.com/coldplay/adventure-of-a-lifetime-lyrics/')
# -------------------------------------load the model------------------------------------
dictionary = corpora.Dictionary.load("./data/dictionary.dict")
corpus = corpora.MmCorpus("./data/corpus.mm")
lda = models.LdaModel.load("./data/model.lda") #result from running online lda (training)
index=similarities.MatrixSimilarity.load("./data/simIndex.index")
#-----------------------------------set up mysql database--------------------
dataBaseName ='lyrics'
tableName='lyricsBody'
# read MySQL and get all lyrics
db = MySQLdb.connect(host='localhost', user='root',passwd='2099', db=dataBaseName)
cursor = db.cursor()
#----------------------------------process and get most similar---------
# clean and bag of word encoding
user_bow=dictionary.doc2bow(stringClean(user_lyric))
# get user's topic dist
user_lda=lda[user_bow]
# find similarity of user's lyric with each of the lyrics in the database
sims = index[user_lda]
# find the most similar 
ans= max([j,i] for i,j in enumerate(sims))
print "the greatest similarity is %f,  with id:  %d" %(ans[0], ans[1]) 
cursor.execute("""SELECT artist, title, year FROM """+tableName +""" WHERE id=%s""", (ans[1],))	# Must make 2nd arg of cursor.execute() a tuple
query_db = cursor.fetchall()
print query_db[0]
