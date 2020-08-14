import re

class PythonCode(object):
    def __init__(self, file):
        self.file = file
        self.output = ''
        self.color_file()
        print(self.output)
        
    def color_file(self):
        #if there is a string to ignore the coloring inside it
        string_ignore = False
        #if there is a multiline string ignore everything in it
        multiline_string_ignore = False
        #if the multiline is on the same line
        same_line = True
        #type of str ' or "
        str_type = ''
        for line in self.file:
            pos = 0
            for char in line:
                if not string_ignore and not multiline_string_ignore:
                    #begin ignoring text while trying to finish the string
                    if char == '\'' or char == '\"': 
                        str_start = pos
                        str_type = char
                        apostrophe_len = 1
                        string_ignore = True
                    else:
                        self.output += char
                #if we are looking for the end of a string
                elif string_ignore:
                    #do we encounter the the same string type ' or "
                    if char == str_type:
                        # if ''
                        if  pos == (str_start + 1):
                            apostrophe_len += 1
                        # if ''' multistring 
                        elif pos == (str_start + 2):
                            if apostrophe_len == 2:
                                apostrophe_len = 3
                                string_ignore = False
                                multiline_string_ignore = True
                            # 'a'
                            else:
                                string_ignore = False
                                print(1)
                                self.output += self.add_color(line, 'orange', str_start, pos)
                        #'dshd sldsd '
                        else:
                            apostrophe_end += 1
                            if apostrophe_end == apostrophe_len:
                                string_ignore = False
                                print(2)
                                self.output += self.add_color(line, 'orange', str_start, (pos + 1))
                    #'' empty string
                    elif pos >= (str_start + 2) and apostrophe_len == 2:
                        string_ignore = False
                        print(3)
                        self.output += self.add_color(line, 'orange', str_start, pos)
                        self.output += char
                    #' unclosed string so reset apostrophe_end to 0
                    else:
                        apostrophe_end = 0
                #multiline
                elif multiline_string_ignore:
                    #''' fgf ' add 1 to the apostrophe_end
                    if char == str_type:
                        apostrophe_end += 1
                        #'''sefrf'''
                        if apostrophe_end == 3:
                            multiline_string_ignore = False
                            #''' frrer '''
                            if same_line:
                                print(4)
                                self.output += self.add_color(line, 'orange', str_start, pos)
                            #'''derrere \n dere '''
                            else:
                                print(5)
                                self.output += self.multiline_add_color_end(line, 'orange', pos + 1)
                                same_line = True
                    #' unclosed string so reset apostrophe_end to 0
                    else:
                        apostrophe_end = 0
                pos += 1
            #end of line if multistring is open
            if multiline_string_ignore:
                same_line = False
                apostrophe_end = 0
                print(6)
                self.output += self.multiline_add_color_start(line, 'orange', str_start)
            #end of line string is open close it
            if string_ignore:
                print(7)
                self.output += self.add_color(line, 'orange', str_start, pos)

    def add_color(self, line, color, start, end):
        line = '<span id="' + color + '">' + line[start:end] + '</span>'
        return  line

    def multiline_add_color_start(self, line, color, start):
        line = '<span id="' + color + '">' + line[start:]
        return line

    def multiline_add_color_end(self, line, color, end):
        line = line[:end] + '</span>'
        return line


if __name__ == "__main__":
    python = PythonCode(open('test.txt', 'r'))