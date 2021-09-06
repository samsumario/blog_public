'''
Szigriszt Pazos. (1992). Sistemas predictivos de legilibilidad del mensaje escrito: fórmula de perspicuidad.
blog:https://eprints.ucm.es/id/eprint/1785/1/T17773.pdf
'''
import util

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


if __name__ == '__main__':
    TextoDePrueba = "Tuvo muchas veces competencia con el cura de su lugar (que era hombre docto graduado en Sigüenza), sobre cuál había sido mejor caballero, Palmerín de Inglaterra o Amadís de Gaula; mas maese Nicolás, barbero del mismo pueblo, decía que ninguno llegaba al caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.\
    En resolución, él se enfrascó tanto en su lectura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio, y así, del poco dormir y del mucho leer, se le secó el cerebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamientos, como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles, y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo."

    score, judge = szigriszt_pazos(TextoDePrueba)
    
    print(score)
    print(judge)