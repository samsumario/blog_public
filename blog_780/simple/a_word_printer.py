import sys
from tkinter import *
import time
import configparser

class App(Frame):
    def __init__(self, master = None, config = None, word_list = []):

        Frame.__init__(self, master)
        self.master = master

        #create label for print a word
        self.text_label = Label(self.master, text = "", font = (config.get("Font", "name"), config.getint("Font", "size")),
                                fg=config.get("Font", "color"), bg=config.get("Font", "bg_color"))

        #set config data
        self.word_threshold = [config.getint("Threshold", "long_word"), config.getint("Threshold", "medium_word"), config.getint("Threshold", "short_word")]
        self.timer_threshold = [config.getint("Timer", "max_update_time"), config.getint("Timer", "long_update_time"), config.getint("Timer", "medium_update_time"),\
                                 config.getint("Timer", "short_update_time"), config.getint("Timer", "min_update_time")]

        #set text data for list
        self.word_list = word_list
        self.words_id = 0

        #total reading time
        self.total_time = 0
        
        #set label for main window
        self.text_label.pack(anchor = "w", expand = 1)

        #app update method
        self.update_word()

    def update_word(self):
        update_time = 0

        if(self.words_id < len(self.word_list)):

            token = self.word_list[self.words_id]
            token_length = len(token)

            #set word in label
            self.text_label.configure(text=" " + token)

            self.words_id = self.words_id + 1

            #change wait time by word length
            if token_length >= self.word_threshold[0]:
            
                update_time = self.timer_threshold[1]
            
            elif ((self.word_threshold[1] <= token_length) and\
                 (token_length < self.word_threshold[0])):
            
                update_time= self.timer_threshold[2]
            
            elif ((self.word_threshold[2] <= token_length) and\
                 (token_length < self.word_threshold[1])):
            
                update_time = self.timer_threshold[3]
            
            else:
                update_time = self.timer_threshold[4]
            
            self.total_time = self.total_time + update_time
        
        #when all word data have printed
        else:
            self.text_label.configure(text="Fin")

            #show result
            print( "{} words per minut".format(round((len(self.word_list) / (self.total_time / 1000) * 60), 1)) )
            print( "total reading time {} sec".format(round((self.total_time / 1000), 1)) )
            print( "total words {}".format(len(self.word_list)) )

            update_time = self.timer_threshold[0]

        #set wait time
        self.after(update_time, self.update_word)

def read_text(text_file):
    words = []

    with open(text_file, encoding = "utf_8", errors = "ignore") as f:
        data = f.read()
        words = data.split()
    
    return words

def main(text_file, config):
    #read config
    window_size = config.get("Window", "size")
    window_color = config.get("Window", "bg_color")
    
    #create root window
    root = Tk()
    root.geometry(window_size)
    root.title('word printer')
    root.configure(bg = window_color)
    
    #read text file
    word_list = read_text(text_file)

    #main setting
    app = App(root, config, word_list)

    #app start
    root.mainloop()

#command example
#python a_word_printer.py sample.txt
if __name__ == '__main__':
    text_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read("conf.ini")
    main(text_file, config)