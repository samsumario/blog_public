'''
Szigriszt Pazos. (1992). Sistemas predictivos de legilibilidad del mensaje escrito: fórmula de perspicuidad.
blog:https://eprints.ucm.es/id/eprint/1785/1/T17773.pdf
'''
from util import util

def interpreta(P):
    if P <= 15:
        return "muy difícil"
    elif P > 15 and P <= 35:
        return "árido"
    elif P > 35 and P <= 50:
        return "bastante difícil"
    elif P > 50 and P <= 65:
        return "normal"
    elif P > 65 and P <= 75:
        return "bastante fácil"
    elif P > 75 and P <= 85:
        return "fácil"
    else:
        return "muy fácil"

def szigriszt_pazos(text):
    score = round(206.835 - 62.3 * ( util.count_syllables(text) / util.count_words(text)) - \
                                            (util.count_words(text) / util.count_sentences(text)),2)
    judge = interpreta(score)

    return score, judge