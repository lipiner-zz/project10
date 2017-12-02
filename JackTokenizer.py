KEYWORD_TYPE = "keyword"
SYMBOL_TYPE = "symbol"
INTEGER_CONST_TYPE = "integerConstant"
STRING_CONST_TYPE = "StringConstant"
IDENTIFIER_TYPE = "identifier"
KEYWORD_LIST = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
SYMBOL_LIST = ['{', '}', '(', ')', '[', ']', '. ', ', ', '; ', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
EOF_NOTE = ''
TAG_PREFIX = "<"
TAG_SUFFIX = ">"
TAG_CLOSER = "/"
NUMBER_OF_READING_BYTES = 1
STRING_CONST_MARK = "\""
BLOCK_COMMENT_START_MARK = "/*"
BLOCK_COMMENT_END_MARK = "*/"
LINE_COMMENT_MARK = "//"


class JackTokenizer:

    def __init__(self, input_stream):
        self.__file = input_stream
        # self.__current_tokens = []
        self.__current_token = None
        self.__next_token = None
        self.__has_token = False  # marks if a full token has found for the next token
        self.__token_type = None
        self.__next_token_type = None

    def has_more_tokens(self):
        # if self.__next_token is not None:
        #     return True
        #
        # if len(self.__current_tokens) == 0:
        #     line = self.__file.readline()
        #     if line == EOF_NOTE:
        #         return False
        # else:
        #     return True

        # if not self.__next_token_type:
        #     return True

        while not self.__next_token:  # as long as the next token is not None
            self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
            while not self.__next_token.isspace():  # skips on whitespaces
                self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
            if self.__next_token == EOF_NOTE:
                return False  # no more tokens
            if self.__next_token == STRING_CONST_MARK:
                # next token is a string constant
                next_char = self.__file.read(NUMBER_OF_READING_BYTES)
                self.__next_token = ""
                while next_char != STRING_CONST_MARK:  # search for the rest of the string constant
                    self.__next_token += next_char
                    next_char = self.__file.read(NUMBER_OF_READING_BYTES)
                # self.__has_token = True  # a full token was read
                self.__next_token_type = STRING_CONST_TYPE
            elif self.__next_token in SYMBOL_LIST:
                # self.__has_token = True  # a full token was found
                self.__next_token_type = SYMBOL_TYPE
            elif self.__next_token.isdigit():
                # next token is a int constant
                next_char = self.__file.read(NUMBER_OF_READING_BYTES)
                while next_char.isdigit():  # search for the rest of the string constant
                    self.__next_token += next_char
                    next_char = self.__file.read(NUMBER_OF_READING_BYTES)
                # self.__has_token = True  # a full token was read
                self.__next_token += next_char  # adds also the delimiter char for not missing it
                self.__next_token_type = INTEGER_CONST_TYPE
            else:
                # not a a symbol - # adds another byte
                self.__next_token += self.__file.read(NUMBER_OF_READING_BYTES)
                # checks if there is a comment
                if self.__next_token == LINE_COMMENT_MARK:
                    self.__next_token = None  # nullify the token since this is a comment
                    self.__file.readline()  # skip the line
                elif self.__next_token == BLOCK_COMMENT_START_MARK:
                    self.__next_token = None  # nullify the token since this is a comment
                    # searches for the end of the comment mark
                    next_char = self.__file.read(len(BLOCK_COMMENT_END_MARK))
                    while next_char != BLOCK_COMMENT_END_MARK:
                        next_char = next_char[1:]
                        next_char += self.__file.read(NUMBER_OF_READING_BYTES)
                # self.__has_token = False  # the token was not completed

        return True

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This method should only
        be called if hasMoreTokens() is true. Initially there is no current token.
        """
        # if self.__next_token is not None:
        #     self.__current_token = self.__next_token
        #     self.__next_token = None
        # else:
        #     self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
        #     while self.__next_token != EOF_NOTE and self.__next_token != " " and \
        #                             self.__next_token is not in SYMBOL_LIST:
        #         pass
        #
        # self.__current_token = self.__next_token
        # self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
        # while self.__next_token != EOF_NOTE and self.__next_token != " " and self.__next_token is not in SYMBOL_LIST:
        #     self.__current_token += self.__next_token

        self.__current_token = self.__next_token
        self.__next_token = None
        if not self.__next_token_type:
            next_char = self.__file.read(NUMBER_OF_READING_BYTES)
            while next_char not in SYMBOL_LIST and not next_char.isspace():
                self.__current_token += next_char
                next_char = self.__file.read(NUMBER_OF_READING_BYTES)
            if next_char in SYMBOL_LIST:
                self.__next_token = next_char
                self.__next_token_type = SYMBOL_TYPE
                # self.__has_token = True
            if self.__current_token in KEYWORD_LIST:
                self.__token_type = KEYWORD_TYPE
            else:
                self.__token_type = IDENTIFIER_TYPE
        else:
            # self.__has_token = False  # the token has been used
            self.__token_type = self.__next_token_type
            self.__next_token_type = None
            if self.__token_type == INTEGER_CONST_TYPE:
                # should remove an extra char
                self.__next_token = self.__current_token[-1]
                self.__current_token = self.__current_token[:-1]
                if self.__next_token not in SYMBOL_LIST:
                    self.__next_token = None
                else:
                    self.__next_token_type = SYMBOL_TYPE

    # def __set_type(self):
    #     pass

    def get_token_type(self):
        return self.__token_type

    # def get_keyword(self):
    #     pass
    #
    # def get_symbol(self):
    #     pass
    #
    # def get_identifier(self):
    #     pass
    #
    # def get_int_val(self):
    #     pass
    #
    # def get_string_val(self):
    #     pass

    def get_value(self):
        return self.__current_token

    def get_token_string(self):
        return self.__create_type_tag() + self.__current_token + self.__create_type_tag(TAG_CLOSER)

    def __create_type_tag(self, closer=''):
        return TAG_PREFIX + closer + self.__token_type + TAG_SUFFIX
