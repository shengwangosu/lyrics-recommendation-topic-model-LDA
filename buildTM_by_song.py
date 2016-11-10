# topic model by song, read data from MySQL database
import MySQLdb, gensim
from gensim import corpora, models, similarities
from url2string import url2string
from stringClean import stringClean

##===========================parameters-===========================
lda_num_topics=8
lda_pass=20
dataBaseName ='lyrics'
tableName='lyricsBody'
# ===========================read MySQL and get all lyrics===========================
db = MySQLdb.connect(host='localhost', user='root',passwd='2099', db=dataBaseName)
cursor = db.cursor()
cursor.execute("SELECT lyric FROM " + tableName)
rawText=[t[0] for t in cursor.fetchall()]	
cursor.execute("SELECT COUNT(DISTINCT artist) FROM " + tableName)
numArtist=cursor.fetchall()[0][0]
print "Num of songs:   %d" %len(rawText)
print "Num of artists: %d" %numArtist 
# ===========================process: clean, dictionary (word to id), corpus (bag of words)===========================
cleanText=stringClean(rawText)						# clean and tokenize, now the list of string =>list of list of words
dictionary= corpora.Dictionary(cleanText)				# build a map of word -> id 
print "---Size of vocabulary:  %i" %len(dictionary)
corpus=[dictionary.doc2bow(i) for i in cleanText]	# encode by bag of words
#===========================train LDA Model===========================
lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=lda_num_topics, id2word = dictionary, passes=lda_pass)
index = similarities.MatrixSimilarity(lda[corpus])
# ========================print the topic dist========================================
"""
#for i in range(lda.num_topics-1):
#	print(lda.print_topics(i))
"""
# ==========================get the topic dist for each song=======================
"""
#corpus_lda = lda[corpus]
#print corpus_lda[0]
"""
#===========================save model=================================
"""
dictionary.save('./data/dicionary.dict')
index.save('./data/simIndex.index')
corpora.MmCorpus.serialize('./data/corpus.mm', corpus)
lda.save('./data/model.lda')
""" 
#============================make a query================================
user_lyric = url2string('http://www.songlyrics.com/coldplay/adventure-of-a-lifetime-lyrics/')
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





