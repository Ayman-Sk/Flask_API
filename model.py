import pickle

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


def load_our_models():
    loaded_model = load_model('saved_model4.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        loaded_tokenizer = pickle.load(handle)
    return loaded_model, loaded_tokenizer


def predict_prob(sentence, loaded_model, loaded_tokenizer):
    sentence_seq = loaded_tokenizer.texts_to_sequences(sentence)
    sentence_pad_seq = pad_sequences(sentence_seq, maxlen=1000)
    res = loaded_model.predict(sentence_pad_seq)
    y_hat = res.ravel()
    return y_hat[0]


def predict_class(y_hat):
    o_threshold = 0.5
    if y_hat >= o_threshold:
        y_hat = 1
    else:
        y_hat = 0
    return y_hat


l1, l2 = load_our_models()
pred_prob = predict_prob(['بتمنا اني ما انولدت بهالحياة يلي دمرتني بس ثريبا لح موا حالي وارتاح'], l1, l2)
the_class = predict_class(pred_prob)
print('the prob: ' + str(pred_prob))
print('the class: ' + str(the_class))
