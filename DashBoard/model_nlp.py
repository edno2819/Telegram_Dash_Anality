from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from keras.models import model_from_json
import pickle


file = open("Functions_to_nlp.obj",'rb')
configs = pickle.load(file)
tokenizer = configs['Tokenizer']


vocab_size = configs['vocab_size']
max_length = configs['max_length']
trunc_type = configs['trunc_type']
padding_type = configs['padding_type']
oov_tok = configs['oov_tok']


def load_model_nlp(path_json, path_peso):    
    loaded_model = load_model(path_json)
    loaded_model.load_weights(path_peso)
    return loaded_model

def predict(texts):
    if texts==[]:
        return []
    sentences = tokenizer.texts_to_sequences(texts)
    sentences_ = pad_sequences(sentences, maxlen = max_length,
                                    padding = padding_type,
                                    truncating=trunc_type,
                                    )
    result = [1 if c>=0.43 else 0 for c in model.predict(sentences_)]
    return result


model = load_model_nlp('Model_NLP.h5', 'Weights_NLP.h5')
