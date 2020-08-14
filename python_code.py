class PythonCode(object):
    def __init__(self, file=None):
        self.file = file
        self.output = ""
        self.color_file()
        print(self.output)
        
    def color_file(self):
        for line in self.file:
            comment = line.index('#')
            string_ignore = False
            pos = 0
            for char in line:
                if not string_ignore:
                    if char == '\'' or char == '\"': 
                        str_start = pos
                        str_type = char
                        comma_len = 1
                        string_ignore = True
                    else:
                        self.output += char
                else:
                    if  pos == str_start + 1 and char == str_type:
                        comma_len += 1
                    elif pos == str_start + 2 and char == str_type:
                        if comma_len == 2:
                            comma_len = 3
                        else:
                            string_ignore = False
                            self.output += self.add_color(line, 'orange', str_start, pos + 1)
                    elif char == str_type:
                        comma_end += 1
                        if comma_end == comma_len:
                            string_ignore = False
                            self.output += self.add_color(line, 'orange', str_start, pos + 1)
                    else:
                        comma_end = 0
                pos += 1
                        

    def add_color(self, line, color, start, end):
        line = line[:end] + '</span>' + line[end:]
        line = line[:start] + '<span id="' + color + '">' + line[start:]
        return  line


if __name__ == "__main__":
    python = PythonCode(open('test.txt', 'r'))