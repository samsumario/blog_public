import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), './analyze_tool'))

from tkinter import *
import configparser
import wordPrintFrame as wframe
import uiFrame as uiframe

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
    
    #read text file
    word_list = read_text(text_file)

    #frame setting
    word_frame = Frame(root, width=300, height=100, bg = config.get("Font", "bg_color"))
    word_frame.grid_propagate(False)
    ui_frame = Frame(root, width=300, height=300, bg = window_color)
    ui_frame.grid_propagate(False)

    app = wframe.App(word_frame, config, word_list)
    uiframe.Ui(ui_frame, config, word_list, app)
    
    word_frame.grid(row = 0, column = 0)
    ui_frame.grid(row = 1, column = 0)

    #app start
    root.mainloop()

#command example
#python a_word_printer.py sample.txt
if __name__ == '__main__':
    text_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read("conf.ini")
    main(text_file, config)