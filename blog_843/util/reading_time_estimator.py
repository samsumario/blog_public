def count_time(word_list, config):
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
        
        if (t/1000 > 60):
            q, mod = divmod(t/1000, 60)
            return str(int(q)) + "min " + str(int(mod)) + "sec"
        else:
            return str(int(t/1000)) + "sec"