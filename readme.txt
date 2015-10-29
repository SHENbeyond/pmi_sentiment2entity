说明：
1、car_pmi_corpus.txt 是 car_review_split.txt 和 car_weibo.txt的汇总sort去重结果，原文件大概是100万微博和300万条汽车直接的评论
2、car_entity_property.txt是评价对象（实体词），car_sentiment_dic.txt是评价词（情感词）
3、pmi_sentiment.py是计算pmi的程序，计算主题词和情感词的PMI值，越大则表明匹配度越高
3、pro_sen_pmi_corpus_sort1.txt是两种方式，内容一样，词的排序不同，按照方便程度选择使用即可。
