#!/usr/bin/python

import os

# opens every file for a given category (pol is either negative or positive)
# formats the data and saves in one large txt file
def open_format_save(pol):
    path = "/users/Lizz/Downloads/review_polarity/txt_sentoken/%s" % pol
    for filename in os.listdir(path):
        #open the file
        with open(path + "/" + filename) as f:
            # read the file
            l = f.read()
            destination = "/Users/Lizz/Documents/Projects/Bot/Datasets/%s.txt" % pol
            with open(destination, "a") as destfile:
                destfile.write(l)

            # split the text on new line 
            
                    

        

# if __name__ = '__main__':
#     main()