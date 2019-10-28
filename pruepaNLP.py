import stanfordnlp

stanfordnlp.download('en')

nlp = stanfordnlp.Pipeline(lang="en")

text= "Hola a todos, buen dia"

result = nlp.annotate(text,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })


for s in result["sentences"]:
    print("{} (Sentiment)", s["sentiment"])