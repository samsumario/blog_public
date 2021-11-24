from deep_translator import GoogleTranslator, MyMemoryTranslator
import time

search_list = ["look", "run", "again"]

for word in search_list:
    translated = GoogleTranslator(source='en', target='es').translate(word)
    print("google result : " + translated)

    time.sleep(2)

for word in search_list:
    translated = MyMemoryTranslator(source='en', target='es').translate(word)
    print("MyMemory result : " + translated)

    time.sleep(2)
