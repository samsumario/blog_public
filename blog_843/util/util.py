from pyverse import Pyverse
import re
import statistics

def count_letters(text):
    count = 0

    for char in text:
        if char.isalpha():
            count += 1

    if count == 0:
        return 1
    else:
        return count

def count_sentences(text):
    text = text.replace("\n", "")
    sentence_end = re.compile('[.:;!?\)\()]')
    sencences=sentence_end.split(text)
    sencences = list(filter(None, sencences))

    if len(sencences) == 0:
        return 1
    else:
        return len(sencences)

def numbers2words(text):
    #e.g. 2 to two

    from util import nal

    new_text = []
    
    for word in text.split():
        formato_numerico = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
        if re.match(formato_numerico, word):
            if type(word) == "int":
                word = int(word)
            else:
                word = float(word)
            word = nal.to_word(word)
        new_text.append(word.lower())
        
    text = ' '.join(new_text)
    return text

def count_words(text):
    text = numbers2words(text)
    
    text = ''.join(filter(lambda x: not x.isdigit(), text))
    clean = re.compile('\W+')
    text = clean.sub(' ', text).strip()
    
    # Prevents zero division
    if len(text.split()) == 0:
        return 1
    else:
        return len(text.split())

def count_syllables(text):
    text = numbers2words(text)
    text = ''.join(filter(lambda x: not x.isdigit(), text))
    syllables = Pyverse(text)

    return syllables.count

if __name__ == '__main__':
    # test
    
    TextoDePrueba = "Tuvo muchas veces competencia con el cura de su lugar (que era hombre docto graduado en Sigüenza), sobre cuál había sido mejor caballero, Palmerín de Inglaterra o Amadís de Gaula; mas maese Nicolás, barbero del mismo pueblo, decía que ninguno llegaba al caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.\
    En resolución, él se enfrascó tanto en su lectura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio, y así, del poco dormir y del mucho leer, se le secó el cerebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamientos, como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles, y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo."
    
    total = count_syllables(TextoDePrueba)
    print(total)