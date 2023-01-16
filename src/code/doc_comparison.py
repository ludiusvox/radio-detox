# This is a sample Python script.
import nltk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests as Req
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import code.doc_similarity as doc_similarity
import lxml
import scipy
#nltk.download('punkt')
#nltk.download('stopwords')

def doc_comparisons(text1,text2):


    #Req = text1

    #SoupText = BeautifulSoup(Req, features="lxml")
    PageText = str(text1)
    

    #Req1 = text2

   
    #SoupText1 = BeautifulSoup(Req1, features="lxml")
    if text2 != '0':    
        PageText1 = str(text2)
    


        sentence_Detector = nltk.data.load('tokenizers/punkt/english.pickle')
        Punctuation = sentence_Detector.tokenize(PageText.strip())
        Sentences = nltk.tokenize.sent_tokenize((PageText.strip()))
        Punctuation1 = sentence_Detector.tokenize(PageText1.strip())
        Sentences1 = nltk.tokenize.sent_tokenize((PageText1.strip()))
        #Twitter =TweetTokenizer()
        #import sys
        #PageText = Twitter.tokenize(PageText)
        #PageText1 = Twitter.tokenize(PageText1)
        #print(PageText,sys.stderr)
        #print(PageText1,sys.stderr)
        Words =nltk.tokenize.word_tokenize(PageText,language="english", preserve_line=False)
        Words1 = nltk.tokenize.word_tokenize(PageText1,language="english", preserve_line=False)
        Words=  PageText
        Words1= PageText1
        dataset =[]
        #print("\n")
        #for word in stopwords.words('english'):
            #print(word)
        #for d in Words:
        #    dataset.append([d])
        #print(dataset)
        """import gensim
        Model = gensim.models.Word2Vec(dataset, min_count=2)
        vector = Model.wv['industry']"""
        text1 = doc_similarity.countFrequencies(Words)
        text2 = doc_similarity.countFrequencies(Words1)
        cd = doc_similarity.compareDocs(text1,text2)
      
        print(cd)
        
        #cb = doc_similarity.seqdiff(Words,Words1)
        #print(cb)
        (cs, WordVectors1) = doc_similarity.makeDocVec(Words)
        (cs1, WordVectors2) = doc_similarity.makeDocVec(Words1)
        
        cs2= scipy.spatial.distance.cosine(WordVectors1[0], WordVectors2[0])
       
        return cs2
    else:
        return None