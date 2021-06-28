import emoji
import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import re
import time

nltk.download('stopwords')
nltk.download('punkt')

def clean_tweets(df,content,col_name,
                general_clean=True,lemma=True,stem=False,remove_tag=True,remove_mention=True,
                remove_emoji=False, remove_stopword=True,min_length=2, untokenized_return=True
                ):
    '''
    This function gives multiple options for cleaning tweets
    df: Dataframe that you will be changing
    col_name: New column name that will be added to the dataframe with the cleaned tweets
    general_clean: A bool that can be used to remove links/images/punctuation it will remove all things
    lemma: a bool that will lemmatize your text
    stem: a bool that will stem your text
    remove_tag: a bool that will remove the entire tag from your text
    remove_mention: a bool that will remove the entire mention from your text
    remove_emoji: a bool that will remove Hex Emojis
    remove_stopword = a bool that will remove stopwords from your text
    min_length: an integer determining the shortest word and is defaulted to length=2
    untokenized_return: a bool that returns the text in string format
    '''
    
    start = time.time()    
    df1=df.copy()
    
    df1.loc[:,col_name] = df1[content].apply(lambda x: min_word_length(str(x),min_length=2))
  
    if remove_mention:
        df1.loc[:,col_name] = df1[col_name].apply(lambda x: remove_mentions(x))
    if remove_tag:
        df1.loc[:,col_name] = df1[col_name].apply(lambda x: remove_tags(x))
    if remove_stopword:
         df1.loc[:,col_name] = df1[col_name].apply(lambda x: remove_stopwords(x))
    if general_clean:
        df1.loc[:,col_name] = df1[col_name].apply(lambda x: format_body(x))
    if remove_emoji:
        df1.loc[:,col_name] = df1[col_name].apply(lambda x: remove_emojis(x))
    if lemma:
         df1.loc[:,col_name] = df1[col_name].apply(lambda x: lemmatize(x))
    if stem:
         df1.loc[:,col_name] = df1[col_name].apply(lambda x: stemmer(x))
    if untokenized_return:
        df1.loc[:,col_name] = df1[col_name].apply(lambda x: untokenize(x))
      
    print("time taken to clean tweets: {}s. Use the [{}] column to perform your analysis/modeling on".format(time.time()-start,col_name))   
    return df1.copy()

def min_word_length(text,min_length):
    '''
    This function will remove all words less than or equal to the min_length specified
    text: input text to function
    min_length: an integer specifying the length of words to remove
    
    eg: if min_length = 2
        Before: "Hello this is a tweet"
        After: "Hello this tweet"
    '''
    # Remove single characters from tweets
    text = ' '.join(i for i in text.split() if not (i.isalpha() and len(i)<=min_length))
    return text

def lemmatize(text):
    '''
    This will lemmatize the text using the WordNetLemmatizer using 
    parts of speech tagging for better lemmatizing and 
    return in a tokenized format
    '''
    lemmatizer = nltk.WordNetLemmatizer()
    lemma = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text)]
    return lemma

def stemmer(text):
    '''
    This will stem the text using the Porter Stemmer from NLTK
    and returns in a tokenized format
    '''
    stemmer = nltk.PorterStemmer()
    stem = [stemmer.stem(w) for w in nltk.word_tokenize(text)]
    return stem

def remove_tags(text):
    '''
    This will remove the entire tag including the word
    returns string format of the text
    '''
     # Remove mentions since there is a column for this [This below removes the entire tag completely]
    text = re.sub('\s([#][\w_-]+)','',text)
    return text

def remove_mentions(text):
    '''
    This will remove the entire mention including the word
    returns string format of the text
    '''
    # Remove mentions since there is a column for this [This below removes the entire mention completely]
    text = re.sub(r"@(\w+)",' ',text,flags=re.MULTILINE)
    return text

def remove_emojis(text):
    '''
    Removes the hex styled emojis
    returns a string format of the text
    '''
    # Remove EMojis from the tweets
    allchars = [word for word in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    no_emoji = ([word for word in text.split() if not any(i in word for i in emoji_list)])
    
    no_emoji_utf =  ' '.join([word.encode("ascii", "ignore").decode() for word in no_emoji])
    return no_emoji_utf

def remove_stopwords(text):
    '''
    Remove stopwords from the text
    returns a string format of the text
    '''
    stopwords_eng = stopwords.words('english')
    tokenized_doc = text.lower().split()
    no_stopwords = " ".join([item for item in tokenized_doc if item not in stopwords_eng])
    return no_stopwords

def untokenize(text):
    '''
    Untokenizes the tokenized text 
    returns a string format of the text
    '''
    untokenized = " ".join([item for item in text])
    return untokenized

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def format_body(text):    
    '''
    This provides general required cleaning from the text:
        - Links
        - Images
        - Funny characters that are uniquely looking punctuation
        - Normal Punctuation
        - Removes ellipsis
        - Removes \xa0 which is left over from the removal of some links
        - Drops everything to lower case
    Returns the text in a string format
    '''
    # Remove links
    text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text, flags=re.MULTILINE)
    text = re.sub('pic.twitter(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text, flags=re.MULTILINE)


    text = text.replace('-',' ')
    text = text.replace('’','')
    text = text.replace('“','')
    text = text.replace('−','')
    text = text.replace('”','')
    text = text.replace('‘','')
    
     
    # Remove punctuation
    text =text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    #     df.loc[:,'CLEAN_CONTENT'] = df['CLEAN_CONTENT'].apply(lambda x :re.sub(r'[^\w\s]','',x))
    
    # Remove Ellipsis
    text = text.replace('…','')
    # Remove weird part at the end of the URL
    text = text.replace('\xa0','')
    # Remove new lines
    text = re.sub('\r\n|\r|\n',r' ',text)
    # Make all lower case
    text = text.lower()
    
    return text