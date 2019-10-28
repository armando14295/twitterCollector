import requests
from elasticsearch import Elasticsearch
import stanfordnlp
from datetime import datetime

def getID(tweets, lista):
	for hit in tweets['hits']['hits']:
		ide= str(hit['_id'])
		if ide in lista:
			continue
		else:
			lista.append(ide)
	return lista

def tweetsData(letra, listaID, oT, oU, hT, txt):
	for hit in letra['hits']['hits']:
		ide= str(hit['_id'])
		if ide in listaID:
			continue
		else:
			listaID.append(ide)
			sT= str(hit['_source']['place']['full_name'])
			sU= str(hit['_source']['user']['location'])
			if "," in sT and "," in sU:
				x= sT.split(",")
				oT.append(x[1])
				x= sU.split(",")
				oU.append(x[1])
			else:
				continue
			hT.append(hit['_source']['created_at'])
			txt.append(hit['_source']['text'])
	return listaID, oT, oU, hT, txt

def getStatistics(lista, total):
	contador= []
	dato= []
	for l in lista:
		if l in dato:
			contador[dato.index(l)]+= 1
		else:
			dato.append(l)
			contador.append(1)
	showResults(dato, contador, total)
	return dato, contador

def showResults(data, count, total):
	c=0
	data, count= sortList(data,count)
	for d in data:
		p= (count[c] * 100) / total
		print("     ", d, ": ", count[c], " -> ", p, "%")
		c+= 1

def sortList(data,count):
	d, c= map(list, zip(*sorted(zip(count, data))))
	return c, d

# Conexion a base de datos
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

ides= []
a= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "cine"}}})
ides= getID(a, ides)

b= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "pelicula"}}})
ides= getID(b, ides)

c= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "netflix"}}})
ides= getID(c, ides)

d= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "hollywood"}}})
ides= getID(d, ides)

e= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "movie"}}})
ides= getID(e, ides)

f= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "cinepolis"}}})
ides= getID(f, ides)

g= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "cinemex"}}})
ides= getID(g, ides)

h= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "cinematografica"}}})
ides= getID(h, ides)

i= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "cinematografia"}}})
ides= getID(i, ides)

j= es.search(index='twitter', body={"size": 10000, "query": {"match": {"text": "oscar"}}})
ides= getID(j, ides)

#total= int(a['hits']['total']) + int(b['hits']['total']) + int(c['hits']['total']) + int(d['hits']['total']) + int(e['hits']['total']) +int(f['hits']['total'])+int(g['hits']['total'])+int(h['hits']['total'])+int(i['hits']['total'])+int(j['hits']['total'])
total= len(ides)

# Se imprime el total de tweets sin repetir
print("Total de Tweets: ", str(total))

# Lista de tweets analizados
nID= []

# Lista para almacenar los lugares de origen del tweet
origenTweet= [] 

# Lista para almacenar los lugares de origen del usuario
origenUser= [] 

# Lista para almacenar los horarios que se tuiteo
horaT= []

# Lista para almacenar los textos que cada tweet
texts= []

# Recorremos los tweets de todos los temas para juntar los datos por lista

nID, origenTweet, origenUser, horaT, texts= tweetsData(a, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(b, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(c, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(d, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(e, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(f, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(g, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(h, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(i, nID, origenTweet, origenUser, horaT, texts)
nID, origenTweet, origenUser, horaT, texts= tweetsData(j, nID, origenTweet, origenUser, horaT, texts)

#print(len(nID))
#print(len(origenTweet))
#print(len(origenUser))
#print(len(horaT))
#print(len(texts))

print("Total de tweets con origen de datos conocido: ", len(origenTweet))

data= []
statistic= []

# Totalizamos los datos y los mostramos
print(" Resultados del origen del tweet:")
data, statistic= getStatistics(origenTweet, total)

# Totalizamos los datos y los mostramos
print(" Resultados del origen del usuario:")
data, statistic= getStatistics(origenTweet, total)

newHT= []

for h in horaT:
	newHT.append(h[11:13]) 

# Totalizamos los datos y los mostramos
print(" Resultados de los horarios:")
data, statistic= getStatistics(newHT, total)


# Analisis de sentimiento de los textos
#sentiments= []
#for text in texts:
#	result = nlp.annotate(text,
#	                   properties={
#	                       'annotators': 'sentiment',
#	                       'outputFormat': 'json',
#	                       'timeout': 1000,
#	                   })
#	
#	for s in result["sentences"]:
#	    sentiments.append(s["sentiment"])

# Totalizamos los datos y los mostramos
#print(" Resultados de los sentimientos:")
#data, statistic= getStatistics(sentiments, total)
