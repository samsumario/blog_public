'''
Fernández Huerta J. (1959). Medidas sencillas de lecturabilidad. Consigna, 214, 29–32.
'''
from util import util

def Pval(text):
    # Syllables-per-word mean (P value)
    
    syllables = util.count_syllables(text)
    words = util.count_words(text)
    return round(syllables / words,2)

def Fval(text):
    # Words-per-sentence mean (F value)
    
    sencences = util.count_sentences(text)
    words = util.count_words(text)
    return round(words / sencences,2)

def interpreta(L):
    if L < 30:
        return "muy difícil"
    elif L >= 30 and L < 50:
        return "difícil"
    elif L >= 50 and L < 60:
        return "bastante difícil"
    elif L >= 60 and L < 70:
        return "normal"
    elif L >= 70 and L < 80:
        return "bastante fácil"
    elif L >= 80 and L < 90:
        return "fácil"
    else:
        return "muy fácil"

def fernandez_huerta(text):

    text = util.numbers2words(text)
    fernandez_huerta = 206.84 - 60*Pval(text) - 1.02*Fval(text)
    
    score = round(fernandez_huerta, 2)
    judge = interpreta(score)

    return score, judge