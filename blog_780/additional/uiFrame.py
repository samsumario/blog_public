from tkinter import *
import time
import configparser
from analyze_tool import fernandez
from analyze_tool import util

class Ui(Frame):
    def __init__(self, master = None, config = None, word_list = [], app = None):

        Frame.__init__(self, master)
        conf_font = (config.get("Font", "name"), config.getint("Font", "s_size"))

        #create button
        start = Button(master, text = "comienzo", font = conf_font, bg = config.get("Ui","bg_button"), command = lambda: app.uiListener(1))
        stop = Button(master, text = "parada", font = conf_font, bg = config.get("Ui","bg_button"), command = lambda: app.uiListener(2))
        back = Button(master, text = "←", font = conf_font, bg = config.get("Ui","bg_button"), command = lambda: app.uiListener(3))
        ad_list = Button(master, text = "cheque", font = conf_font, bg = config.get("Ui","bg_button"), command = lambda: app.uiListener(4))

        #set button
        start.grid(row = 1, column = 0, sticky = "w")
        stop.grid(row = 1, column = 1, sticky = "w")
        back.grid(row = 1, column = 2, sticky = "w")
        ad_list.grid(row = 1, column = 3, sticky = "w")

        #create label
        total_sec = self.total_time_sec(word_list, config)
        self.time = Label(master, text = "tiempo " + str(total_sec)+ " sec", font = conf_font, bg = config.get("Ui","bg_color"))

        t = len(word_list)
        total_words = Label(master, text = str(t) + " parabras", font = conf_font, bg = config.get("Ui","bg_color"))

        self.wps = Label(master, text = str(round((t / total_sec * 60), 1)) + " wps", font = conf_font, bg = config.get("Ui","bg_color"))
        
        score, judge = self.fernandez_score(word_list)
        difficulty = Label(master, text = "score " + str(score) + " " + judge, font = conf_font, bg = config.get("Ui","bg_color")) 
        
        sm = self.syllables(word_list)
        syllables = Label(master, text = str(round((sm / total_sec * 60), 1)) + " syllables/Min", font = conf_font, bg = config.get("Ui","bg_color")) 
        
        #set label
        self.wps.grid(row = 2, column = 0, columnspan = 4, sticky = "w")
        self.time.grid(row = 3, column = 0, columnspan = 4, sticky = "w")
        total_words.grid(row = 4, column = 0, columnspan = 4, sticky = "w")
        difficulty.grid(row = 5, column = 0, columnspan = 4, sticky = "w")
        syllables.grid(row = 6, column = 0, columnspan = 4, sticky = "w")
    
    def fernandez_score(self, word_list):
        text = " ".join(x for x in word_list)
        return fernandez.fernandez_huerta(text)
    
    def syllables(self, word_list):
        text = " ".join(x for x in word_list)
        return util.count_syllables(text)
    
    def total_time_sec(self, word_list, config):
        #same logic in wordPrintFrame.py 16-17
        word_threshold = [config.getint("Threshold", "long_word"), config.getint("Threshold", "medium_word"), config.getint("Threshold", "short_word")]
        timer_threshold = [config.getint("Timer", "max_update_time"), config.getint("Timer", "long_update_time"), config.getint("Timer", "medium_update_time"),\
                                 config.getint("Timer", "short_update_time"), config.getint("Timer", "min_update_time")]
        t = 0
        #same logic in wordPrintFrame.py 48-66
        for word in word_list:
            token_length = len(word)
            if token_length >= word_threshold[0]:
                
                update_time = timer_threshold[1]
                
            elif ((word_threshold[1] <= token_length) and\
                (token_length < word_threshold[0])):
            
                update_time= timer_threshold[2]
            
            elif ((word_threshold[2] <= token_length) and\
                (token_length < word_threshold[1])):
            
                update_time = timer_threshold[3]
            
            else:
                update_time = timer_threshold[4]
            
            t = t + update_time
        
        return t/1000