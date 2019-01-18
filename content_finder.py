import requests
from urllib import request
import re
from bs4 import BeautifulSoup
from general import *

class Content:

    NUM = 1  # index of the articles
    SUM = 0  # the number of crawled paragraphs in total

    def __init__(self, project_name):
        Content.project_name = project_name
        self.get_url(Content.project_name)


    def get_url(self, proj_name):
        data_file = proj_name + "/data.txt"
        with open(data_file) as t:
            for line in t:
                currenturl = line.strip('\n')
                text = Content.get_web(currenturl)
                Content.get_para(currenturl, text, project_name)
            t.close()


    def get_web(currenturl):    
        try:
            res=requests.get(currenturl)
            res.raise_for_status()
            return res.content  
        except requests.RequestException as e:
            print(e)
            return ''


    def get_para(currenturl, text, project_name):
        soup = BeautifulSoup(text,'html.parser')
        para_list = []
        pattern_para = []
        para_list=soup.find_all('p') # all paragraphs
        pattern_para = Content.write_to_sentence(para_list)

        # once the pattern paragraph exists in the article, write down the url, the paragraphs and full text
        if pattern_para != None:
            sentences_file = project_name + "sentences.txt"
            f=open(sentences_file,"a",encoding='utf-8')

            # print the index of current articles
            index = "NO. " + str(Content.NUM) + '\n'
            f.writelines(index)
            Content.NUM += 1

            # print the url which includes time and title
            f.write(currenturl)
            f.writelines('\n')

            # print the paragraphs that satisfy the patterns
            for x in pattern_para:
                # once the pattern exist, write down the paragraph
                if len(x[0]) > 0:
                    for num in x[0]:            
                        f.write("%i " % num)
                    f.writelines('\n')
                    xx = re.sub(' +\s*\t*\n*', ' ', x[1])
                    xxx = re.sub('\t*\n*', '', xx)
                    f.writelines(xxx + '\n')
                f.writelines('\n')

            #print the sum of crawled paragraph
            Content.SUM += len(pattern_para)
            sec = "The sum: " + str(Content.SUM) + '\n'  # sum of crawled paragraph so far (includes the current article)
            f.write(sec)
            

            # print the full article
            f.write("The full paragraph:\n")
            for i in range(len(para_list)):
                pp = re.sub(' +\s*\t*\n*', ' ', para_list[i].get_text())
                ppp = re.sub('\t*\n*', '', pp)
                f.writelines(ppp)
            f.writelines('\n\n')

            print('finished article' + str(Content.NUM-1) + '\n')
            f.close()


    def write_to_sentence(para_list):
        pattern_para = []
        para = ''
        
        for i in range(len(para_list)):
            para = para_list[i].get_text()    
            pattern = Content.isObeyRules(para)
            if pattern != []:
                pattern_para.append([pattern, para])
        
        if len(pattern_para) > 0:
            return pattern_para
        else:
            return None
                
                
    def isObeyRules(sentence):
        '''pattern_definition'''
        key = []

        match = re.search(" (i|I)f ", sentence)  # 1: (I)if
        if match:
            key.append(1)

        match2 = re.search(" (w|sh|c)ould ", sentence)   # 2: would / should /could
        if match2:
            key.append(2)

        match3 = re.search(" (s|S)uggest", sentence)  # 3: (S)suggest/sugesting/suggestion
        if match3:                    
            key.append(3)

        match4 = re.search(" (as|so) long as ", sentence)  # 4: (as|so) long as...
        if match4:                    
            key.append(4)

        match5 = re.search(" (u|U)less ", sentence)  # 5: (U)unless...
        if match5:                    
            key.append(5)

        match6 = re.search(" (I|i)n case ", sentence) # 6: (I|i)n case
        if match6:
            key.append(6)

        match7 = re.search(" (s|S)uppos", sentence)  # 7: (U)suppose/supposing/supposed/supposedly/supposition
        if match7:
            key.append(7)
        
        return key


    

    

    