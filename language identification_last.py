#!/usr/bin/env python
# coding: utf-8

# In[138]:


#coding:utf-8


import sys

from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

def calculate_ratios(text):

    """
    Calculate the ratio of given text to be written in several languages and returns a list that looks 
    like [{'french': 2,'english': 4},{'Frensh': {'de', 'la', 'au'}, 'english': {'on', 'you', 'in', 'the'}})
    
    """
    
    ratios_dict = {}
    words_dict ={}
    
    #nltk.wordpunct_tokenize() splits all punctuations into separate tokens
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    #loop on the languages in stopwords
    for langue in stopwords.fileids():
        # oget stopwords from the selected language
        stopwords_set = set(stopwords.words(langue))
        #add the words of our text to a set
        words_set = set(words)
        # get the list intersection between the words of our text and the stopwords of the language
        common_words = words_set.intersection(stopwords_set)
        # add the number of the intersection list words
        ratios_dict[langue] = len(common_words)
        #add the intersection list of words
        words_dict[langue] = common_words

    return ratios_dict, words_dict


def calculate_probability(most, secode_most) :
    
    """
    Calculate probability of the two most rated languages found.
    """
    
    #calculate the probability of the language "most" to be the language in which the text is written
    proba = (float(most) /(most + secode_most) * 100)
    return round(proba)


def detect_language(text):

    """
    Detect the language of the text by using a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text and calculate the probability of the two most rated languages
    
    """
    # get the ratio and stopwords lists
    ratios = calculate_ratios(text)
    
    #get the first most rated language
    first_rated_language = max(ratios[0], key=ratios[0].get)
    most_common_words = ratios[0][first_rated_language]
    
    #get the second most rated language
    sorted_language_list = sorted(ratios[0].items(), key=lambda item: item[1], reverse=True)
    second_rated_language = list(sorted_language_list)[1][0]
    second_most_common_words = ratios[0][second_rated_language]
    
    #print the probability
    print("\nThere is {0}% chances for this text to be writen in {1}\n" .format(calculate_probability(most_common_words, second_most_common_words), first_rated_language))

    

def language_details(text, number):
    
    """
     printing the probability of language which the text can be written in and
     the most rated four languages found in the text with there stopwords
    """
    
    print("Text %d" %number)
    
    detect_language(text)
    
    #  get text ratios and it's stopwords
    langlist=calculate_ratios(text)
    
    #sort the language list by ratio to print the most rated four languages 
    lang_list_sort=sorted(langlist[0].items(), key=lambda item: item[1], reverse=True)
    
    # print the ratio and the stopwords of the languages found
    for lang in lang_list_sort[0:4]:
        if lang[1] != 0 :
            print("\t{0} has {1} word(s)" .format(lang[0],lang[1]))
            print("\t\t{0} words list : {1}".format(lang[0],langlist[1][lang[0]]))
             
    

    
    
if __name__=='__main__':

    
    text1 = '''
    check if your able to understand the image bellow, it contains arabic text 
    that says "ماذا سيحدث لك إذا توقفت عن التدخين لمدة يوم؟".
    '''
    
    text2 = '''
    il faut utiliser l'article A devant un nom commençant par un son "consonne" et 'AN' devant un nom commençant par un son "voyelle".
    Exemples :
    - door (porte) > a door (une porte)
    /d/ est un son consonne
    - apple (pomme) > an apple (une pomme)
    /a/ est un son voyelle
    - kitchen (cuisine) > a kitchen (une cuisine)
    /k/ est un son consonne.
    '''
    
    text3 = '''
    ارتفعت حصيلة ضحايا فيروس كورونا في العالم إلى 600 ألف وفاة منذ ظهور الوباء في الصين في كانون الأول/ديسمبر 2019.
    وأحصيت 100 ألف وفاة جديدة خلال 21 يوما فقط أي منذ 28 حزيران/يونيو. أغلب هذه الوفيات  شهدتها أوروبا بـ205,065 وفا
    ة، تليها أمريكا اللاتينية بـ160 ألفا. فيما تم إحصاء أكثر من 14 مليون إصابة بالفيروس في 196 دولة ومنطقة.
    وتجدر الإشارة إلى أن هذه الأرقام لا تعكس إلا جزءا من العدد الحقيقي للإصابات.
    '''
    
    #*******************************************************
    print("Detects the probability of the text's languages \n")
    
    language_details(text1, 1)
    language_details(text2, 2)
    language_details(text3, 3)
    
    
    

    
    


# In[139]:


import nltk.data
from nltk.classify import textcat


def Text_sentence_tokenizer(text):
    
    """
    Punkt Sentence Tokenizer
    This tokenizer divides a text into a list of sentences
    by using an unsupervised algorithm to build a model for abbreviation
    words, collocations, and words that start sentences.  It must be
    trained on a large collection of plaintext in the target language
    before it can be used.

    The NLTK data package includes a pre-trained Punkt tokenizer for
    English.
    """
    
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences_list=sent_detector.tokenize(text.strip())
    return sentences_list
    
def detect_language(list):
    """
    using TextCat to detect language an implementation of the text categorization algorithm
    """
    
    #using textcat to categorize the text
    text_cat = textcat.TextCat()
    
    #print language of each sentence
    for sentence in list:
        print("the sentence:\n\t '{0}' => is written in {1}".format(sentence,text_cat.guess_language(sentence)) )

 
if __name__=='__main__':
    
    
    Text4 = '''
    Beautiful is better than ugly. 
    Açık, örtük olmaktan iyidir. 
    البساطة أفضل من التعقيد.
    '''
    Text5='''
    il faut utiliser l'article A devant un nom commençant par un son "consonne".
        Exemples :
        - door (porte) > a door (une porte)
        /d/ est un son consonne
        - apple (pomme) > an apple (une pomme)
        /a/ est un son voyelle
        - kitchen (cuisine) > a kitchen (une cuisine)
        /k/ est un son consonne.'''
    
    #*******************************************************
    
    detect_language(Text_sentence_tokenizer(Text4))
    detect_language(Text_sentence_tokenizer(Text5))
    
   


# In[ ]:




