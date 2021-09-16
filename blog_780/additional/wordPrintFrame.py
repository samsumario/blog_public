from tkinter import *
import time
import datetime
import configparser

class App(Frame):
    def __init__(self, master = None, config = None, word_list = []):

        Frame.__init__(self, master)
        #create label for print a word
        self.header_space = Label(master, bg=config.get("Font", "bg_color"))
        self.text_label = Label(master, text = "", font = (config.get("Font", "name"), config.getint("Font", "size")),
                                fg=config.get("Font", "color"), bg=config.get("Font", "bg_color"))

        #set config data
        self.word_threshold = [config.getint("Threshold", "long_word"), config.getint("Threshold", "medium_word"), config.getint("Threshold", "short_word")]
        self.timer_threshold = [config.getint("Timer", "max_update_time"), config.getint("Timer", "long_update_time"), config.getint("Timer", "medium_update_time"),\
                                 config.getint("Timer", "short_update_time"), config.getint("Timer", "min_update_time")]

        #set text data for list
        self.word_list = word_list
        self.words_id = 0
        self.stok_list = []
        #total reading time
        self.total_time = 0
        
        #set label for frame
        self.header_space.grid(row = 0, column = 0)
        self.text_label.grid(row = 1, column = 0)

        #app update method
        self.status = 0 #1:start/0:stop
        self.update_word()

    def update_word(self):
        update_time = 10
        if(self.status):
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

                #debug
                #print( "{} words per minut".format(round((len(self.word_list) / (self.total_time / 1000) * 60), 1)) )
                #print( "total reading time {} sec".format(round((self.total_time / 1000), 1)) )
                #print( "total words {}".format(len(self.word_list)) )
                                
                #save check list in text file
                if(len(self.stok_list) > 0):
                    dt_now = datetime.datetime.now()
                    file_name = dt_now.strftime('%Y-%m-%d@%H_%M_%S') + "chek_list.txt"

                    with open(file_name, encoding = "utf_8", mode = "w") as f:
                        for word in self.stok_list:
                            f.write(word+"\n")
                    
                    print( "save check list {}".format(file_name) )
                    
                    self.status = 0
                    update_time = self.timer_threshold[0]



        #set wait time
        self.after(update_time, self.update_word)
    
    def uiListener(self, command):
        #start
        if (command == 1):
            self.status = 1
        #stop
        elif (command == 2):
            self.status = 0
        #back
        elif (command == 3):
            self.status = 0
            print(self.words_id)
            if(self.words_id > 1):
                self.words_id = self.words_id - 1
                
                #set word in label
                self.text_label.configure(text=" " + self.word_list[self.words_id-1])

        #add list
        elif (command == 4):
            if((self.words_id < len(self.word_list)) and \
                self.words_id > 0 ): #id = 1 when first word showed
                
                check = self.word_list[self.words_id - 1]
                print("debug : " + check)
                if(check in self.stok_list):
                    pass
                else:
                    self.stok_list.append(check)
                    print("add word : " + check)
