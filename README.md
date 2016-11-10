# lyrics-recommendation-topic-model-LDA
===============================Main==================================================
 To train:  	buildTM_by_song.py:			load lyrics from MySQL table, train, save, and query similarity of user provided lyric
 To query: 		find_similar_lyric:			stand-along script to load LDA model, index, and corpus, and make a query
 
 ==============================Other======================================
 crateDB.py:  		call web scrape to get lyric and save to MySQL database
 stringClean.py:	clean and tokenize
 url2string:		web scrape: turn URL to String
 
 =============================================================================
