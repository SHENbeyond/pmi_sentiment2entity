#coding:utf-8
import math
import os,sys
import re
from operator import itemgetter

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer,SementicRoleLabeller
ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
#sys.path.append(os.path.join(ROOTDIR, "lib"))
# 设置模型文件的路径
MODELDIR=os.path.join(ROOTDIR, "ltp_data")


def getPMI(corpus, srcTerms, destTerms):
    srcTermsFre = {term:0 for term in srcTerms}
    destTermsFre = {term:0 for term in destTerms}
    coFre = {}
    coPMI = {}
    lineCount = 0
    inputCorpus = open(corpus,'r').readlines()
    corpus_sen = []
    for line in inputCorpus:
        #line = re.sub('？|!|；|','。',line.strip())
        line  = re.sub('！|。|#|\?|？|!|；|;|，|,', ' ', line)
        #line  = line.split('。')
        line = re.sub('[\s]+', '。',line)
        line = line.split('。')
        corpus_sen.extend(line)
    for sen in corpus_sen:
        sen = sen.strip()
        print sen,len(sen)
        if len(sen) > 5:
            lineCount += 1
            sen = segmentor.segment(sen)
        temp = []
        for srcTerm in srcTerms:
            if srcTerm in sen:
                srcTermsFre[srcTerm] += 1
                temp.append(srcTerm)
        for destTerm in destTerms:
            if destTerm in sen:
                destTermsFre[destTerm] += 1
                for t in temp:
                    if t+"\001"+destTerm in coFre.keys():
                        coFre[t+"\001"+destTerm] += 1
                    else:
                        coFre[t+"\001"+destTerm] = 1


    for k,v in coFre.items():
        key = k.split("\001")
        value = math.log(lineCount*float(v)/(float(srcTermsFre[key[0]])*float(destTermsFre[key[1]])), 2)
        coPMI[k] = round(value, 6)
    return coPMI

#属性词
def fun_property_set(path):
    property_set = []
    for line in path.readlines():
        property_set.append((line.strip().split('\t')[0]))
    return property_set

#情感词
def fun_emotion_set(path):
    emotion_set = []
    for line in path.readlines():
        emotion_set.append((line.strip().split('\t')[0]))
    return emotion_set

def sortByPMI(coPMI):
    sorted_tuple =[]
    for item in coPMI:
        items = item.split('\001')
        #print 'item:',items,type(items)
        #print coPMI[item],type(coPMI[item])
        sorted_tuple.append((items[0],items[1],coPMI[item]))
    return sorted(sorted_tuple,key =itemgetter(0,2)),sorted(sorted_tuple,key= itemgetter(1,2))


segmentor = Segmentor()
segmentor.load_with_lexicon(os.path.join(MODELDIR,"cws.model"),"/data0/dm/dict/dict.txt")


if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    path_property = open(path+"/car_entity_property.txt",'r')
    pro_words = fun_property_set(path_property)
    path_sentiment = open(path+"/car_sentiment_dic.txt",'r')
    sen_words = fun_emotion_set(path_sentiment)
    path_corpus = path+"/car_pmi_corpus.txt"
    path_out1 = open(path+"/pro_sen_pmi_corpus_sort1.txt",'w')
    
    path_out2 = open(path+"/pro_sen_pmi_corpus_sort2.txt",'w')
    
    posPmi = getPMI(path_corpus, pro_words, sen_words)
    sorted_tuple1,sorted_tuple2 = sortByPMI(posPmi)
    for ll in sorted_tuple1:
        path_out1.write(ll[0]+'\t'+ll[1]+'\t'+str(ll[2])+'\n')
    
    for lll in sorted_tuple2:
        path_out2.write(lll[1]+'\t'+lll[0]+'\t'+str(lll[2])+'\n')
    
    path_out1.close()
    path_out2.close()
