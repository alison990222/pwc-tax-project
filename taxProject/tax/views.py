from django.shortcuts import render
from tax.models import itemDatabase, TaxDatabase
from django.http import HttpResponse, HttpResponseRedirect
import time
import random
import json
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
import pandas
from django.db import connection
import jieba as jb
import re
import pickle
import joblib
import numpy as np
import pandas as pd

def remove_punctuation(line):
    line = str(line)
    if line.strip()=='':
        return ''
    rule = re.compile(u"[^\u4E00-\u9FA5]")
    line = rule.sub('',line)
    return line
 
def stopwordslist(filepath):  
    try:
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords  
    except:
        data = {"error": "error"}

def secondPredict(select,i,data):
    cat_id_df2 = data[['secondCategory', 'SecondCategoryID']].drop_duplicates().reset_index(drop=True)
    cat_to_id2 = dict(cat_id_df2.values)
    id_to_cat2 = dict(cat_id_df2[['SecondCategoryID', 'secondCategory']].values)

    select = select.dropna(subset=['info'])

    count_vect2 = CountVectorizer()
    X_train_counts2 = count_vect2.fit_transform(select['info'])
    tfidf_transformer2 = TfidfTransformer()
    X_train_tfidf2 = tfidf_transformer2.fit_transform(X_train_counts2)

    clf2 = LinearSVC().fit(X_train_tfidf2, select['SecondCategoryID'])
    pred_cat_id2=clf2.predict(count_vect2.transform([i]))
    print(id_to_cat2[str(pred_cat_id2[0])])
    return id_to_cat2[str(pred_cat_id2[0])]
    
    

def algorithm(productName):
    query = str(TaxDatabase.objects.all().query)
    data = pandas.read_sql_query(query, connection)
    query = str(itemDatabase.objects.all().query)
    itemData = pandas.read_sql_query(query, connection)
    itemData.columns=["id","info","code","firstCategory","FirstCategoryID","secondCategory","SecondCategoryID"]
    itemData = itemData[["id","code","firstCategory","FirstCategoryID","secondCategory","SecondCategoryID","info"]]
    frames = [data, itemData]
    data = pandas.concat(frames)
    data = data.reset_index(drop=True)

    stopwords = stopwordslist("chineseStopWords.txt")
    data['info'] = data['info'].apply(remove_punctuation)
    data['info'] = data['info'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))

    with open('model/linearSVC.pickle', 'rb') as f:
        clf = pickle.load(f)

    cat_id_df = data[['firstCategory', 'FirstCategoryID']].drop_duplicates().reset_index(drop=True)
    cat_to_id = dict(cat_id_df.values)
    id_to_cat = dict(cat_id_df[['FirstCategoryID', 'firstCategory']].values)
    # print(cat_id_df2)
    count_vect = joblib.load("model/vectorizer.pkl")

    cut = [w for w in list(jb.cut(remove_punctuation(productName))) if w not in stopwords]
    print(cut)
    # print(id_to_cat)
    allCategory = []
    recommendation = []
    for i in cut:
        X_new_counts = count_vect.transform([i])
        tfidf_transformer = TfidfTransformer()
        X_new_tfidf = tfidf_transformer.fit_transform(X_new_counts)
        pred_cat_id=clf.predict(X_new_tfidf)
        
        pred_cat_id=clf.predict(count_vect.transform([i]))
        print(id_to_cat[str(pred_cat_id[0])])
        select = data[data["firstCategory"]==id_to_cat[str(pred_cat_id[0])]]
        allCategory.append(id_to_cat[str(pred_cat_id[0])])
        recommendation.append(secondPredict(select,i,data))

    return allCategory,recommendation

    # # #删除除字母,数字，汉字以外的所有符号
    # data['clean_info'] = data['info'].apply(remove_punctuation)
    # # # #分词，并过滤停用词
    # data['cut_info'] = data['clean_info'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))
    # # data

    # cat_id_df = data[['firstCategory', 'categoryID']].drop_duplicates().sort_values('categoryID').reset_index(drop=True)
    # cat_to_id = dict(cat_id_df.values)
    # id_to_cat = dict(cat_id_df[['categoryID', 'firstCategory']].values)


    # X_train, X_test, y_train, y_test = train_test_split(data['cut_info'], data['categoryID'], random_state = 20)
    # count_vect = CountVectorizer()
    # X_train_counts = count_vect.fit_transform(X_train)
    
    # tfidf_transformer = TfidfTransformer()
    # X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    
    # clf = LinearSVC().fit(X_train_tfidf, y_train)

    # format_sec=" ".join([w for w in list(jb.cut(remove_punctuation(productName))) if w not in stopwords])
    # pred_cat_id=clf.predict(count_vect.transform([format_sec]))
    # categoryName = id_to_cat[pred_cat_id[0]]

    # return categoryName #, data[data[firstCategory==categoryName]]



def insert(request):
    
    if request.method == 'POST':

        try:
            productName = request.POST.get('item')
            secondCategory = request.POST.get('secondCategory')
            firstCategory = request.POST.get('firstCategory')
            code = request.POST.get('code')
            
            query = str(TaxDatabase.objects.all().query)
            data = pandas.read_sql_query(query, connection)
            tar = data[data["firstCategory"]==firstCategory]["FirstCategoryID"].reset_index(drop=True)
            itemFirstcategoryID = tar[0]
            tar = data[data["secondCategory"]==secondCategory]["SecondCategoryID"].reset_index(drop=True)
            itemSecondCategoryID = tar[0]

            itemDatabase.objects.create(item=productName, itemSecondCategory=secondCategory, 
                                        itemFirstCategory=firstCategory,itemSecondCategoryID=itemSecondCategoryID,
                                        itemCode=code, itemFirstCategoryID=itemFirstcategoryID)

            data = {
                "status":"success",
            }

        except:
            data = {"status": "error"}
    else:
        data = {
            "error": "the method should be POST"
        }
    return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json")


def search(request):
    if request.method == 'GET':

        try:
            productName = request.GET['productName']
            category, recommendation  = algorithm(productName)
            objList = []
            for i in category:
                categoryList = TaxDatabase.objects.filter(firstCategory=i)
                for obj in categoryList:
                    if(recommendation == obj.secondCategory):
                        objList.append({
                            'code': obj.code,
                            'firstCategory': obj.firstCategory,
                            'secondCategory': obj.secondCategory,
                            'info':obj.info
                        })
                    else:
                        objList.append({
                            'code': obj.code,
                            'firstCategory': obj.firstCategory,
                            'secondCategory': obj.secondCategory,
                            'info':obj.info
                        })
  
            data = {
                "status":"推："+str(recommendation),
                "category": category,
                "objList":objList,
            }
        except:
            data = {"status": "error"}
    else:
        data = {
            "error": "the method should be GET"
        }
    return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json")

def showDatabase(request):

    if request.method == 'GET':
        data = itemDatabase.objects.all()
        return render(request, 'tax.html', {'data': data})

def showEncoding(request):
    if request.method == 'GET':
        data = TaxDatabase.objects.all()
        return render(request, 'encoding.html', {'data': data})


