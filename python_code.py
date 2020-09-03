import re

class PythonCode(object):
    def __init__(self, file):
        self.file = file
        self.blue_words = {
            'and',
            'in',
            'not',
            'or',
            'False',
            'True',
            '__name__',
            'self',
        }
        self.purple_words = {
            'if',
            'else',
            'elif',
            'import',
            'from',
            'as',
            'return',
            'for',
            'in',
            'try',
            'except',
            'while',
            'yield',
            'break'
        }
        #most built in functions
        self.yellow_words = {
            'abs',
            'delattr',
            'hash',
            'memoryview',
            'all',
            'help',
            'min',
            'setattr',
            'any',
            'dir',
            'hex',
            'next',
            'ascii',
            'divmod',
            'id',
            'sorted',
            'bin',
            'enumerate',
            'input',
            'oct',
            'eval',
            'open',
            'breakpoint',
            'exec',
            'isinstance',
            'ord',
            'sum',
            'filter',
            'issubclass',
            'pow',
            'iter',
            'print',
            'callable',
            'format',
            'len',
            'chr',
            'range',
            'vars',
            'getattr',
            'locals',
            'repr',
            'zip',
            'compile',
            'globals',
            'map',
            'reversed',
            '__import__',
            'hasattr',
            'max',
            'round',
        }
        #rest of built in functions
        self.lightgreen_words = {
            'complex',
            'classmethod',
            'frozenset',
            'list',
            'property',
            'type',
            'tuple',
            'super',
            'bytes',
            'float',
            'bytearray',
            'str',
            'int',
            'staticmethod',
            'bool',
            'object',
            'set',
            'dict',
            'slice',
        }
        self.lightblue_words = {
            'targes',
            'args',
        }
        self.output = ''
        self.color_file()

    def output_word(self, word):
        if word in self.blue_words:
            self.output += self.add_color(word, 'blue', 0, len(word))
        elif word in self.purple_words:
            self.output += self.add_color(word, 'purple', 0, len(word))
        elif word in self.yellow_words:
            self.output += self.add_color(word, 'yellow', 0 , len(word))
        elif word in self.lightgreen_words:
            self.output += self.add_color(word, 'lightgreen', 0 , len(word))
        elif word in self.lightblue_words:
            self.output += self.add_color(word, 'lightblue', 0 , len(word))
        elif word.isnumeric():
            self.output += self.add_color(word, 'number', 0, len(word))
        else:
            self.output += escape(word)

        
    def color_file(self):
        #if there is a string to ignore the coloring inside it
        string_ignore = False
        #if there is a multiline string ignore everything in it
        multiline_string_ignore = False
        #if the multiline is on the same line
        same_line = True
        #type of str ' or "
        str_type = ''
        more_args = False
        more_parens = 0
        for line in self.file:
            def_ignore = False
            args = False
            args_done = False
            class_ignore = False
            equals = False
            skip_next = False
            parens = 0
            pos = 0
            word = ''
            for char in line:
                if not string_ignore and not multiline_string_ignore and not def_ignore and not class_ignore:
                    #begin ignoring text while trying to finish the string
                    if char == '\'' or char == '\"': 
                        str_start = pos
                        str_type = char
                        apostrophe_len = 1
                        string_ignore = True
                        if word == 'u':
                            self.output += self.add_color(word, "blue", 0, 1)
                        elif word:
                            output_word(word)
                            word = ''
                    elif char == '#':
                        if word:
                            self.output_word(word)
                            word = ''
                        self.output += self.add_color(line, 'green', pos, len(line) - 1)
                        self.output += '\n'
                        break
                    elif (char == ',' or char == ')') and equals:
                        if char == ')':
                            parens -= 1
                        if parens == 0:
                            def_ignore = True
                            equals = False
                            if '->' not in word:
                                self.output += self.add_color(line, 'lightblue', pos - len(word), pos)
                                self.output += char
                                word = ''
                            else:
                                start = word.index('->') + 2
                                self.output +=  escape(word[:start]) + self.add_color(word, 'lightgreen',  start, len(word))
                                self.output += char
                                word = ''
                        else:
                            self.output_word(word)
                            word = ''
                            self.output += char
                    elif char == ',' or char == ')':
                        if char == ')':
                            parens -= 1
                            if parens + more_parens == 0:
                                more_args = False
                        self.output_word(word)
                        self.output += char
                        word = ''
                    elif char == '(':
                        parens += 1
                        more_args = True
                        self.output_word(word)
                        self.output += char
                        word = ''
                    elif char == '[':
                        self.output_word(word)
                        self.output += char
                        word = ''
                    elif char == ']':
                        self.output_word(word)
                        self.output += char
                        word = ''
                    elif char == '=' and more_args:
                        self.output += self.add_color(word, 'lightblue', 0, len(word))
                        self.output += char
                        word = ''
                    elif char == '.':
                        if word == 'self':
                            self.output += self.add_color(word, 'blue', 0, 4) + char
                            word = ''
                        else:
                            word += char
                    elif char == ':':
                        self.output_word(word)
                        self.output += char
                        word = ''
                    elif char != ' ' and char != '\n':
                        word += char
                    else:
                        if word == 'def':
                            self.output += self.add_color(line, 'blue', pos - 3, pos)
                            def_ignore = True
                        elif word == 'class':
                            self.output += self.add_color(line, 'blue', pos - 5, pos)
                            class_ignore = True
                        elif word == '->' and equals:
                            word += char
                            continue
                        else:
                            self.output_word(word)
                        word = ''
                        self.output += char
                #if we are looking for the end of a string
                elif string_ignore:
                    if skip_next:
                        skip_next = False
                    elif char == '\\':
                        apostrophe_end = 0
                        skip_next = True
                    #do we encounter the the same string type ' or "
                    elif char == str_type:
                        # if ''
                        if  pos == (str_start + 1):
                            apostrophe_len += 1
                        # if ''' multistring 
                        elif pos == (str_start + 2):
                            if apostrophe_len == 2:
                                apostrophe_len = 3
                                string_ignore = False
                                multiline_string_ignore = True
                                apostrophe_end = 0
                            # 'a'
                            else:
                                string_ignore = False
                                self.output += self.add_color(line, 'orange', str_start, pos + 1)
                        #'dshd sldsd '
                        else:
                            apostrophe_end += 1
                            if apostrophe_end == apostrophe_len:
                                string_ignore = False
                                self.output += self.add_color(line, 'orange', str_start, (pos + 1))
                    #'' empty string
                    elif pos >= (str_start + 2) and apostrophe_len == 2:
                        string_ignore = False
                        self.output += self.add_color(line, 'orange', str_start, pos)
                        self.output += escape(char)
                    #' unclosed string so reset apostrophe_end to 0
                    else:
                        apostrophe_end = 0
                #multiline
                elif multiline_string_ignore:
                    if skip_next:
                        skip_next = False
                    elif char == '\\':
                        apostrophe_end = 0
                        skip_next = True
                    #''' fgf ' add 1 to the apostrophe_end
                    elif char == str_type:
                        apostrophe_end += 1
                        #'''sefrf'''
                        if apostrophe_end == 3:
                            multiline_string_ignore = False
                            #''' frrer '''
                            if same_line:
                                self.output += self.add_color(line, 'orange', str_start, pos + 1)
                            #'''derrere \n dere '''
                            else:
                                self.output += self.multiline_add_color_end(line, 'orange', pos + 1)
                                same_line = True
                    #' unclosed string so reset apostrophe_end to 0
                    else:
                        apostrophe_end = 0
                elif def_ignore:
                    if char == '(' and not args:
                        self.output += self.add_color(line, 'yellow', pos - len(word), pos)
                        self.output += escape(char)
                        word = ''
                        parens = 1
                    elif char == '=':
                        self.output += self.add_color(line, 'lightblue', pos - len(word), pos - 1)
                        self.output += ' ='
                        word = ''
                        equals = True
                        def_ignore = False
                    elif char == ',':
                        if '->' not in word:
                            self.output += self.add_color(line, 'lightblue', pos - len(word), pos)
                            self.output += ','
                            word = ''
                        else:
                            start = word.index('->') + 2
                            self.output +=  escape(word[:start]) + self.add_color(word, 'lightgreen',  start, len(word))
                            self.output += ','
                            word = ''
                    elif char == '(':
                        parens += 1
                    elif char == ')':
                        parens -= 1
                        if parens == 0:
                            if '->' not in word:
                                self.output += self.add_color(line, 'lightblue', pos - len(word), pos)
                                self.output += ')'
                                word = ''
                            else:
                                start = word.index('->') + 2
                                self.output += escape(word[:start]) + self.add_color(word, 'lightgreen',  start, len(word) - 1)
                                self.output += ')'
                                word = ''
                        args_done = True
                    elif char == ':':
                        if '->' not in word:
                            self.output += escape(word) + escape(char)
                            word = ''
                        else:
                            start = word.index('->') + 2
                            self.output += escape(word[:start]) + self.add_color(word, 'lightgreen',  start, len(word))
                            self.output += escape(char)
                            word = ''
                        def_ignore = False
                    else:
                        word += char
                elif class_ignore:
                    if char == ':':
                        self.output += self.add_color(line, 'lightgreen', pos - len(word), pos)
                        self.output += escape(char)
                        word = ''
                        class_ignore = False
                    else:
                        word += char
                pos += 1
            
            #end of line if multistring is open
            if multiline_string_ignore:
                same_line = False
                apostrophe_end = 0
                self.output += self.multiline_add_color_start(line, 'orange', str_start)
            #end of line string is open close it
            elif string_ignore:
                self.output += self.add_color(line, 'orange', str_start, pos)
            else:
                self.output += word
                def_ignore = False

    def add_color(self, line, color, start, end):
        line = '<span id="' + color + '">' + escape(line[start:end]) + '</span>'
        return  line

    def multiline_add_color_start(self, line, color, start):
        line = '<span id="' + color + '">' + escape(line[start:])
        return line

    def multiline_add_color_end(self, line, color, end):
        line = escape(line[:end]) + '</span>'
        return line

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')



if __name__ == "__main__":
    python = PythonCode(open('../MVT/simple.py', 'r'))
    template = open('index.html').read()
    open('temp.html', 'w').write(template.replace('PUTCODEHERE', python.output))