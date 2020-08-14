import re

class PythonCode(object):
    def __init__(self, file):
        self.file = file
        self.output = ''
        self.color_file()
        
    def color_file(self):
        
        string_ignore = False
        multiline_string_ignore = False
        same_line = True
        str_type = ''
        for line in self.file:
            pos = 0
            for char in line:
                if not string_ignore and not multiline_string_ignore:
                    print("U")
                    if char == '\'' or char == '\"': 
                        str_start = pos
                        str_type = char
                        comma_len = 1
                        string_ignore = True
                    else:
                        self.output += char
                elif string_ignore:
                    if char == str_type:
                        if  pos == (str_start + 1):
                            comma_len += 1
                        elif pos == (str_start + 2):
                            if comma_len == 2:
                                comma_len = 3
                                string_ignore = False
                                print('M')
                                multiline_string_ignore = True
                            else:
                                string_ignore = False
                                print(1)
                                self.output += self.add_color(line, 'orange', str_start, pos)
                        else:
                            comma_end += 1
                            if comma_end == comma_len:
                                string_ignore = False
                                print(2)
                                self.output += self.add_color(line, 'orange', str_start, (pos + 1))
                    elif pos >= (str_start + 2) and comma_len == 2:
                        string_ignore = False
                        print(3)
                        self.output += self.add_color(line, 'orange', str_start, pos)
                        self.output += char
                    else:
                        comma_end = 0
                elif multiline_string_ignore:
                    if char == str_type:
                        comma_end += 1
                        if comma_end == 3:
                            print("X")
                            multiline_string_ignore = False
                            if same_line:
                                print(4)
                                self.output += self.add_color(line, 'orange', str_start, pos)
                            else:
                                print(5)
                                self.output += self.multiline_add_color_end(line, 'orange', pos + 1)
                    else:
                        comma_end = 0
                pos += 1
            if multiline_string_ignore:
                same_line = False
                comma_end = 0
                print(6)
                print("EXTRA",self.output)
                print("END")
                self.output += self.multiline_add_color_start(line, 'orange', str_start)
                print("EXTRA",self.output)
                print("END")
            if string_ignore:
                print(7)
                self.output += self.add_color(line, 'orange', str_start, pos)
        
            print(self.output)

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