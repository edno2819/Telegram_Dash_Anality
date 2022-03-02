# from nltk.tokenize import TweetTokenizer
# from nltk.stem import WordNetLemmatizer
# import nltk
# import re


stopwords = ['já', 'estávamos', 'quando', 'muito', 'eles', 'meu', 'sou', 'esse', 'teus', 'tive', 'tenha', 'não', 'tenham', 'do', 'entre', 'estejam', 'serei', 'fôramos', 
'estivemos', 'estava', 'minha', 'seriam', 'COELHO', 'estavam', 'vc', 'nossas', 'tém', 'terão', 'hão', 'Comments', 'temos', 'houverei', 'pelo', 'até', '3KE', 'tuas', 'tiverem', 
'nos', 'houveríamos', 'há', 'hajamos', 'tivera', 'que', 'hei', 'tivessem', 'TOCA', 'tinha', 'eram', 'ao', 'fôssemos', 'dele', 'nossa', 'lhe', 'ele', 'estivera', 'Forwarded message',
'estivéramos', 'fora', 'essa', 'tivemos', 'a', 'por', 'aqueles', 'hajam', 'seria', 'dela', 'https', 'Os', 'este', 'estamos', 'tenho', 'houve', 'teria', 'tem', 'dos', 'à', 'lhes', 
'será', 'for', 'da', 'fui', 'terá', 'plotlygraphs', 'estivessem', 'vcs', 'esteve', 'somos', 'delas', 'teu', 'elas', 'qual', 'aquelas', 'serão', 'aquilo', '4k', 'sua', 'e', 'pelas',
'pra', 'houver', 'para', 'nas', 'aquela', 'estas', 'houveriam', 'estive', 'esta', 'nem', 'estejamos', 'havemos', 'era', 'teve', 'as', 'fosse', 'isto', 'eu', 'o', 'estes', 'houvesse',
'estiver', 'DE', 'haja', 'Forwarded', 'na', 'aquele', 'seremos', 'é', 'éramos', 'uma', 'mas', 'me', 'esteja', 'houveria', '2k', 'das', 'tu', 'no', 'houverem', 'num', 'tinham', 'vos',
'estou', 'houvemos', 'você', 'estiverem', 'terei', 'estivermos', 'pelos', 'meus', 'houveram', 'formos', 'NA', 'houverão', 'numa', 'com', 'como', 'também', 'nossos', 'deles', 
'houvéssemos', 'foram', 'br', 'né', 'seu', 'tínhamos', 'houverá', 'só', 'nosso', 'em', 'depois', 'os', 'tiveram', 'tivéramos', 'sem', 'nós', 'tivesse', 'está', 'vocês', 'houvéramos', 
'tivermos', 'seus', 'mais', 'essas', 'teriam', 'minhas', 'sejamos', 'O', 'forem', 'um', 'estivéssemos', 'houvessem', 'se', 'estiveram', 'fossem', 'tiver', 'seríamos', '3k', 'foi', 
'de', 'mesmo', 'teremos', 'seja', 'aos', 'isso', 'suas', 'são', 'n', 'message', 'tenhamos', 'tivéssemos', 'estão', 'fomos', 'sejam', 'tua', 'houvera', 'estivesse', 'te', 'às', 'quem', 
'ela', 'ou', 'esses', 'houvermos', 'houveremos', 'Não', 'pela', 'q', 'teríamos', 'HTTPS', 'HTTP', 'http']



def RemoveStopWords(instance):
    palavras = [i for i in instance.split() if not i in stopwords]
    instance = del_word(" ".join(palavras), 'https')
    return (instance)

def del_word(instance, word):
    while instance.find(word)!=-1:
        instance  = instance.replace(word, '')
    return instance


# stopwords = set(nltk.corpus.stopwords.words('portuguese'))
# # stopwords.remove('não')
# # stopwords.remove('mas')
# # stopwords.remove('nem')
# stopwords.update([
# "https", "plotlygraphs", 'não', 'mas', 'nem', 'vc', 'vcs', 'a', 'o', 'na', 'né', 'q', 'Os', 'de',
# 'e', 'se', 'na', 'pra','que','3k','Forwarded', 'message','Forwarded message','4k','da','2k','DE','br','n','Comments','NA','3K'
# 'E','TOCA', 'COELHO','de','O','Não'
# ])


# wordnet_lemmatizer = WordNetLemmatizer()
# tweet_tokenizer = TweetTokenizer()


# def Stemming(instancia):
#     stemmer = nltk.stem.RSLPStemmer()
#     palavras = []
#     for w in instancia.split():
#         palavras.append(stemmer.stem(w))
#     return (" ".join(palavras))

# def Limpeza_dados(instancia):
#     remove = ['.', ';', '-', ':', ')', '(', '_', '@', '!', "?"]
#     instancia = re.sub(r"http\S+", "", instancia).lower()
#     for item in remove:
#         instancia = instancia.replace(item, '')
#     return instancia

# def Lemmatization(instancia):
#   palavras = []
#   for w in instancia.split():
#     palavras.append(wordnet_lemmatizer.lemmatize(w))
#   return (" ".join(palavras))

# def To_negation(texto):# PARAR A ADIÇÃO DO NEG EM UM .
#     negacoes = ['não','not']
#     negacao_detectada = False
#     resultado = []
#     palavras = texto.split()
#     for p in palavras:
#         p = p.lower()
#         if negacao_detectada == True:
#             p = p + '_neg'
#         if p in negacoes:
#             negacao_detectada = True
#         resultado.append(p)
#     return (" ".join(resultado))

# def Preprocessing_neg(instancia, split=False):
#    if split:
#        instancia = instancia[0].split('.') 

#    stemmer = nltk.stem.RSLPStemmer()
#    instancia = Limpeza_dados(instancia)
#    instancia = RemoveStopWords(instancia)
#    instancia = Lemmatization(instancia)
#    instancia = To_negation(instancia)
 
#    return instancia

# def Preprocessing(instancias):
#     lista = []
#     for instancia in instancias:
#         instancia = Limpeza_dados(instancia)
#         instancia = RemoveStopWords(instancia)
#         instancia = Lemmatization(instancia)
#         lista.append(instancia)

#     return lista

# def pop_indexs(data, exclud):
#     count=0
#     for c in sorted(exclud):
#         data.pop(c+count)
#         count-=1
#     return data

# def remove_itens_x(data, item, qtd):
#     for c in range(qtd):
#         data.remove(item)
#     return data

#remove_itens_x([1,2,3,1,5,47,8,4,1,31,5,'sd'], 1, 2)

#print(Preprocessing(['teste amiga! dessa função de expliti e tambem:']))