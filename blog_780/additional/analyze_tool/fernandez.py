'''
Fernández Huerta J. (1959). Medidas sencillas de lecturabilidad. Consigna, 214, 29–32.
'''
import util

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

if __name__ == '__main__':
    TextoDePrueba = "Tuvo muchas veces competencia con el cura de su lugar (que era hombre docto graduado en Sigüenza), sobre cuál había sido mejor caballero, Palmerín de Inglaterra o Amadís de Gaula; mas maese Nicolás, barbero del mismo pueblo, decía que ninguno llegaba al caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.\
    En resolución, él se enfrascó tanto en su lectura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio, y así, del poco dormir y del mucho leer, se le secó el cerebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamientos, como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles, y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo."
    
    score, judge = fernandez_huerta(TextoDePrueba)
    print(score)
    print(judge)