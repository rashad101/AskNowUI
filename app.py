# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, url_for, jsonify, Response, redirect, session
import json, sys
import requests
import os

app = Flask(__name__, static_url_path='/static')
#bootstrap = Bootstrap(app)


#Autocomplete part...... 
@app.route('/_autocomplete', methods=['POST'])
def autocomplete():  
    #SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    #json_url = os.path.join(SITE_ROOT, "data", "qa.json")
    #data = json.load(open(json_url))
    results=[]
    #for item in data:
    #    results.append(item["question"])
    return Response(json.dumps(results), mimetype='application/json')


def processEarlResult(earlResult, question):
    resultResourceDict = {
      "question": question,
      "answer": "No result found",
      "entity": "No result found",
      "type": "No result found",
      "abstract": "No result found",
      "summary":"No result found",
      "recommendations":"No result found",
      "related_entities":"No result found",
      "similar_entities":"No result found",
      "question_type":"resource"
    }
    resultListDict =  {
      "question": question,
      "answer": { "0": "No result found"
      },
      "abstract":{ "0": "No result found"
      },
      "question_type":"list"
    }
    resultBolDict = {
      "question": question,
      "answer": "No result found",
      "question_type":"bol"
    }
    resultLiteralDict = {
      "question": question,
      "answer": "No result found",
      "question_type":"literal"
    }
    count = 0
    for item in earlResult:
        for k,v in item[0].iteritems():
            uri = v['value']
            q = """select ?label ?abstract where {
                   <%s> rdfs:label ?label .
                   <%s> dbo:abstract ?abstract .
                   }"""%(uri,uri)
            url = "http://dbpedia.org/sparql"
            p = {'query': q}
            h = {'Accept': 'application/json'}
            try:
                r = requests.get(url, params=p, headers=h)
                d =json.loads(r.text)
            except Exception,e:
                print e
            try:
                for row in d['results']['bindings']:
                    if 'abstract' in row and 'label' in row:
                        if row['abstract']['xml:lang'] == 'en' and row['label']['xml:lang'] == 'en':
                            #print row,count
                            resultListDict['answer'][str(count)] = row['label']['value']
                            resultListDict['abstract'][str(count)] = row['abstract']['value']
                            count += 1
            except Exception,e:
                print e 

    #print resultListDict 
    return resultListDict
    

#get resource json
@app.route('/_getJSON', methods=['POST', 'GET'])
def getJSON():
    if request.method == 'POST':
        question = request.form.get('question')
        global QUESTION
        QUESTION = question
    print(QUESTION)
    inputDict = {'nlquery':QUESTION}
    r = requests.post("http://localhost:4999/processQuery", data=json.dumps(inputDict), headers={"content-type": "application/json"})
    earlResult = json.loads(r.text)
    resourceDict = processEarlResult(earlResult, QUESTION)
    return Response(json.dumps(resourceDict), mimetype='application/json')   


# index part
# question name
@app.route('/', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')



@app.route('/resource', methods=['GET', 'POST'])
def showResource(): 
    if request.method == 'GET':
        question=request.args.get('question')
        global QUESTION
        QUESTION=question
        return render_template('resource.html') 
    return render_template('resource.html')


@app.route('/list')
def showList():
    if request.method == 'GET':
        question=request.args.get('question')
        global QUESTION
        QUESTION=question
        return render_template('list.html') 
    return render_template('list.html')

@app.route('/literal')
def showLiteral():
    if request.method == 'GET':
        question=request.args.get('question')
        global QUESTION
        QUESTION=question
        return render_template('literal.html') 
    return render_template('literal.html')

@app.route('/bol')
def showBoolean():
    if request.method == 'GET':
        question=request.args.get('question')
        global QUESTION
        QUESTION=question
        return render_template('bol.html') 
    return render_template('bol.html')

@app.route('/404')
def showNothing():
    return render_template('none.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('none.html')



if __name__ == '__main__':
    app.run(debug = True, port=5001)

