from tkinter import *
from newspaper import Article
import string
import re
import nltk 
import heapq
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

xls = pd.ExcelFile(r'C:\Users\Allan Ngo\Desktop\金融創新\專案\LoughranMcDonald_SentimentWordLists_2018.xlsx')
df1 = xls.parse(0, header=None)
df2 = xls.parse(1, header=None)
df3 = xls.parse(2, header=None)
df4 = xls.parse(3, header=None)
df5 = xls.parse(4, header=None)
df6 = xls.parse(5, header=None)
df7 = xls.parse(6, header=None)

#輸入要分析的英文新聞網址
# url = 'https://www.cnbc.com/2020/10/08/nvidia-and-huawei-face-uncertain-future-in-britains-high-tech-capital.html'
# https://www.nytimes.com/2020/10/07/us/politics/vice-presidential-debate.html?action=click&module=Spotlight&pgtype=Homepage
# https://www.cnbc.com/2020/08/18/stockton-california-mayor-michael-tubbs-on-his-success.html
# https://www.cnbc.com/2020/10/08/nvidia-and-huawei-face-uncertain-future-in-britains-high-tech-capital.html
# https://edition.cnn.com/2020/10/07/economy/women-workforce-coronavirus/index.html
# https://edition.cnn.com/2020/10/05/tech/smic-us-sanctions-hnk-intl/index.html
# https://www.federalreserve.gov/monetarypolicy/beigebook202009.htm



def press():
    url = str(e1.get())        #####
    if url == "":
        area_label_1['text'] = str("")
        area_label_2['text'] = str("")
        area_label_3['text'] = str("")
        area_label_4['text'] = str("")
        area_label_5['text'] = str("")
        area_label_6['text'] = str("")
        area_label_7['text'] = str("")
        area_label_8['text'] = str("")

    else:
        article = Article(url)

        #把網站的內容爬下來
        article.download()
        article.parse()
        # nltk.download('punkt')
        article.nlp

        text = (article.text)

        # print(article.text)

        #把爬下來的內容去除特殊符號和多餘空位
        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', text)
        article_text = re.sub(r'\s+', ' ', text)

        #去除特別的註解號碼和特殊文字
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)



        #把所有文字斷詞，也把沒詞性的文字去掉
        nltk.download('punkt')
        nltk.download('stopwords')


        #把所有句子斷句
        sentence_list = nltk.sent_tokenize(article_text)
        # print(sentence_list)
        stopwords = nltk.corpus.stopwords.words('english')

        #把剩餘的文字計算次數
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())


        #從出現最多次的文字當成最重要的字，再去看哪個斷出來句子權重最大，來決定那句的重要性，來作為summary的選擇
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)


        area_label_1['text'] = (article.title)              ##############
        area_label_2['text'] = (article.authors[0])
        area_label_3['text'] = (article.publish_date.strftime('%Y-%m-%d'))

        summary_list = nltk.sent_tokenize(summary)

        area_label_4['text'] =  str("1. ") + summary_list[0]
        area_label_5['text'] =  str("2. ") + summary_list[1]
        area_label_6['text'] =  str("3. ") + summary_list[2]
        area_label_7['text'] =  str("4. ") + summary_list[3]
        area_label_8['text'] =  str("5. ") + summary_list[4]

 
def graph():
    url = str(e1.get())        #####
    article = Article(url)

    #把網站的內容爬下來
    article.download()
    article.parse()
    # nltk.download('punkt')
    article.nlp

    text = (article.text)

    # print(article.text)

    #把爬下來的內容去除特殊符號和多餘空位
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    article_text = re.sub(r'\s+', ' ', text)

    #去除特別的註解號碼和特殊文字
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


    #把所有文字斷詞，也把沒詞性的文字去掉
    nltk.download('punkt')
    nltk.download('stopwords')

    #把所有句子斷句
    sentence_list = nltk.sent_tokenize(article_text)
    # print(sentence_list)
    stopwords = nltk.corpus.stopwords.words('english')

    #把剩餘的文字計算次數
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())


    #從出現最多次的文字當成最重要的字，再去看哪個斷出來句子權重最大，來決定那句的重要性，來作為summary的選擇
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    
    #把前面斷過的字去和情緒字典作比較，找出哪個情緒程度比較重
    lower_text = text.lower()
    cleaned_text = lower_text.translate(str.maketrans('','',string.punctuation))
    tokenized_words = cleaned_text.split()

    negative = []
    positive = []
    uncertainty = []
    litigious = []
    strongmodal = []
    weakmodal = []
    constraining = []

    qq = []
    for line in (df1[0].tolist()):
        qq.append(line)
    for line1 in qq:
        negative.append(line1.lower())

    qq = []
    for line in (df2[0].tolist()):
        qq.append(line)
    for line1 in qq:
        positive.append(line1.lower())

    qq = []
    for line in (df3[0].tolist()):
        qq.append(line)
    for line1 in qq:
        uncertainty.append(line1.lower())

    qq = []
    for line in (df4[0].tolist()):
        qq.append(line)
    for line1 in qq:
        litigious.append(line1.lower())

    qq = []
    for line in (df5[0].tolist()):
        qq.append(line)
    for line1 in qq:
        strongmodal.append(line1.lower())

    qq = []
    for line in (df6[0].tolist()):
        qq.append(line)
    for line1 in qq:
        weakmodal.append(line1.lower())

    qq = []
    for line in (df7[0].tolist()):
        qq.append(line)
    for line1 in qq:
        constraining.append(line1.lower())

    emotion_list = []

    for i in tokenized_words:
        if i in negative:
            emotion_list.append("Negative")
        elif i in positive:
            emotion_list.append("Positive")
        elif i in uncertainty:
            emotion_list.append("Uncertainty")
        elif i in litigious:
            emotion_list.append("Litigious")
        elif i in strongmodal:
            emotion_list.append("StrongModal")
        elif i in weakmodal:
            emotion_list.append("WeakModal")
        elif i in constraining:
            emotion_list.append("Constraining")

    times = Counter(emotion_list)
    # print(times)

    fig, ax1 = plt.subplots()
    ax1.bar(times.keys(),times.values())
    fig.autofmt_xdate()
    plt.show()


def graphcloud():
    url = str(e1.get())        #####
    article = Article(url)

    #把網站的內容爬下來
    article.download()
    article.parse()
    # nltk.download('punkt')
    article.nlp

    text = (article.text)

    # print(article.text)

    #把爬下來的內容去除特殊符號和多餘空位
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    article_text = re.sub(r'\s+', ' ', text)

    #去除特別的註解號碼和特殊文字
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


    #把所有文字斷詞，也把沒詞性的文字去掉
    nltk.download('punkt')
    nltk.download('stopwords')

    #把所有句子斷句
    sentence_list = nltk.sent_tokenize(article_text)
    # print(sentence_list)
    stopwords = nltk.corpus.stopwords.words('english')

    #把剩餘的文字計算次數
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())


    #從出現最多次的文字當成最重要的字，再去看哪個斷出來句子權重最大，來決定那句的重要性，來作為summary的選擇
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    # {k: v for k, v in sorted(word_frequencies.items(), key=lambda item:item[1], reverse=True)}
    wordclouduse = {}
    for i in word_frequencies:
        if len(i)>1:
            wordclouduse.update({i:word_frequencies[i]})

    wordclouduse = {k: v for k, v in sorted(wordclouduse.items(), key=lambda item:item[1], reverse=True)}
    # wordclouduse

    wc = WordCloud(background_color="#fff", max_words=200,width=200,height=130,
                relative_scaling=1,normalize_plurals=False).generate_from_frequencies(wordclouduse)
    plt.figure(figsize=(6,4), facecolor='k')
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=1)
    plt.show()


def e_delete():
    e1.delete(first=0,last=10000)


master = Tk()
master.title('News-Summarizer.exe')
master.geometry('1000x480')

Label(master, text="News Website\t:", font=('Arial',12,'bold')).grid(row=0, sticky=W, pady=6)
e1 = Entry(master, justify = LEFT, font = ('Arial', 12), width = 80)
e1.grid(row = 0, column=1)
Button(master, text="Search", command = press, width = 15).grid(row=0,column=2, sticky=W, pady=6)
Button(master, text="Sentiment", command = graph, width = 15).grid(row=1,column=2, sticky=W, pady=6)
Button(master, text="WordCloud", command = graphcloud, width = 15).grid(row=2,column=2, sticky=W, pady=6)
Button(master, text="Clear", command = e_delete, width = 15).grid(row=3,column=2, sticky=W, pady=6)
Button(master, text="Quit", command = master.quit, width = 15).grid(row=9,column=2, sticky=W, pady=6)

Label(master, text="Title\t\t:", font=('Arial',12,'bold')).grid(row=1, sticky=W)
area_label_1 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_1.grid(row= 1, column=1, sticky=W, pady=6)


Label(master, text="Author\t\t:", font=('Arial',12,'bold')).grid(row=2, sticky=W)
area_label_2 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_2.grid(row= 2, column=1, sticky=W, pady=6)



Label(master, text="Publish Date\t:", font=('Arial',12,'bold')).grid(row=3, sticky=W)
area_label_3 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_3.grid(row= 3, column=1, sticky=W, pady=6)

Label(master, text="Summary\t:", font=('Arial',12,'bold')).grid(row=4, sticky=W)
area_label_4 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_4.grid(row= 4, column=1, sticky=W, pady=6)


area_label_5 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_5.grid(row= 5, column=1, sticky=W, pady=6)


area_label_6 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_6.grid(row= 6, column=1, sticky=W, pady=6)


area_label_7 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_7.grid(row= 7, column=1, sticky=W, pady=6)


area_label_8 = Label(master, font = ('Arial', 12), wraplength=700, justify = LEFT)
area_label_8.grid(row= 8, column=1, sticky=W, pady=6)


mainloop()