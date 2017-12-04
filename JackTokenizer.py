KEYWORD_TYPE = "keyword"
SYMBOL_TYPE = "symbol"
INTEGER_CONST_TYPE = "integerConstant"
STRING_CONST_TYPE = "stringConstant"
IDENTIFIER_TYPE = "identifier"
KEYWORD_LIST = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
SYMBOL_LIST = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
EOF_MARK = ''
TAG_PREFIX = "<"
TAG_SUFFIX = ">"
TAG_CLOSER = "/"
TAG_END_OF_LINE = "\n"
TAG_DELIMITER = " "
NUMBER_OF_READING_BYTES = 1
STRING_CONST_MARK = "\""
COMMENT_SYMBOLS = ["/", "*"]
BLOCK_COMMENT_START_MARK = "/*"
BLOCK_COMMENT_END_MARK = "*/"
LINE_COMMENT_MARK = "//"
SYMBOL_FIX = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}


class JackTokenizer:
    """
    Removes all comments and white space from the input stream and breaks it into Jacklanguage
    tokens, as specified by the Jack grammar.
    """
    def __init__(self, input_stream):
        """
        Creates a tokenizer object with the given input stream
        :param input_stream: a stream contained a jack code
        """
        self.__file = input_stream
        self.__current_token = None
        self.__next_token = None
        self.__token_type = None
        self.__next_token_type = None

    def has_more_tokens(self):
        """
        Checks if the are more tokens
        :return: True iff there is another token to read
        """
        # there is a next token
        if self.__next_token:
            return True

        # Search for the next token which is not an empty line, comment or an EOF.
        while not self.__next_token_type:  # while the next token type is empty
            self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
            while self.__next_token.isspace():  # skips on whitespaces
                self.__next_token = self.__file.read(NUMBER_OF_READING_BYTES)
            if self.__next_token == EOF_MARK:
                return False  # no more tokens
            self.__process_next_token()

        return True

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This method should only
        be called if hasMoreTokens() is true. Initially there is no current token.
        """
        self.__current_token = self.__next_token
        self.__token_type = self.__next_token_type
        self.__next_token = None
        self.__next_token_type = None
        if (self.__token_type != STRING_CONST_TYPE and self.__token_type != SYMBOL_TYPE) or \
                (self.__token_type == SYMBOL_TYPE and len(self.__current_token) > 1):
            # the token contains extra chars
            next_char = self.__current_token[-1]
            self.__current_token = self.__current_token[:-1]
            if not next_char.isspace() and next_char != EOF_MARK:
                # the next char should be ignored- processes it
                self.__next_token = next_char
                self.__process_next_token()

        self.__fix_symbol()  # fix the symbol format in case it is needed

    def __process_next_token(self):
        """
        Processes the next token, checks for its type.
        In case of a string constant - gets its full content and set the next token type
        In case of a integer constant - gets its full content, sets the next token type,
            and includes the next char after the integer constant into the next token value
        In case of a symbol - sets the next token type. The symbol might contain an extra char
        In case of a keyword or an identifier - gets its full content, sets the next token type,
            and includes the next char after the keyword/identifier into the next token value
        """
        if self.__next_token is None:
            return
        if self.__next_token == STRING_CONST_MARK:
            # next token is a string constant
            self.__get_string_constant_value()
            self.__next_token_type = STRING_CONST_TYPE
        elif self.__next_token.isdigit():
            # next token is a int constant
            self.__get_integer_constant_value()
            self.__next_token_type = INTEGER_CONST_TYPE
        elif self.__next_token in SYMBOL_LIST:
            if not self.__process_comment():
                # a symbol that is not a comment
                self.__next_token_type = SYMBOL_TYPE
        else:
            self.__get_keyword_identifier_value()

    def get_token_type(self):
        """
        :return: the token type
        """
        return self.__token_type

    def get_value(self):
        """
        :return: the token value
        """
        return self.__current_token

    def get_token_string(self):
        """
        :return: the token string in the format of: <TYPE> VALUE </TYPE>
        """
        return self.__create_type_tag() + TAG_DELIMITER + self.__current_token + TAG_DELIMITER + \
            self.__create_type_tag(TAG_CLOSER) + TAG_END_OF_LINE

    def __create_type_tag(self, closer=''):
        """
        Creates the type tag in its format
        :param closer: the closer note if there should be one. Otherwise it has default empty value
        :return: the type tag
        """
        return TAG_PREFIX + closer + self.__token_type + TAG_SUFFIX

    def __fix_symbol(self):
        """
        Changes the symbol if it contains XML unsupported notes
        """
        if self.__current_token in SYMBOL_FIX:
            self.__current_token = SYMBOL_FIX[self.__current_token]

    def __get_string_constant_value(self):
        """
        Gets the full string constant value into the next token
        """
        self.__next_token = ""  # clears the string constant mark
        next_char = self.__file.read(NUMBER_OF_READING_BYTES)
        while next_char != STRING_CONST_MARK:  # search for the rest of the string constant
            self.__next_token += next_char
            next_char = self.__file.read(NUMBER_OF_READING_BYTES)

    def __get_integer_constant_value(self):
        """
        Gets the full integer content value into the next token, and includes the next char after the
        integer constant
        """
        next_char = self.__file.read(NUMBER_OF_READING_BYTES)
        while next_char.isdigit():  # search for the rest of the string constant
            self.__next_token += next_char
            next_char = self.__file.read(NUMBER_OF_READING_BYTES)
        # keeps the delimiter char. The next char can't be empty since a valid jack file
        # ends with a bracket and not a digit
        self.__next_token += next_char

    def __get_keyword_identifier_value(self):
        """
        Gets the full keyword/identifier value into the next token, and includes the delimiter next char.
        Sets the token type to be either keyword or an identifier
        """
        next_char = self.__file.read(NUMBER_OF_READING_BYTES)
        # The next char must be a symbol or whitespace. It can't be empty since a valid jack file ends
        # with a bracket
        while next_char not in SYMBOL_LIST and not next_char.isspace():
            self.__next_token += next_char
            next_char = self.__file.read(NUMBER_OF_READING_BYTES)
        if self.__next_token in KEYWORD_LIST:
            self.__next_token_type = KEYWORD_TYPE
        else:
            self.__next_token_type = IDENTIFIER_TYPE
        self.__next_token += next_char  # keeps the delimiter char after identifying the token type

    def __process_comment(self):
        """
        Checks if the next token is a comment, and if so increment the stream to skip the comment
        :return: True if it was a comment, False other wise
        """
        if self.__next_token not in COMMENT_SYMBOLS:
            return False
        # adds byte to check if it is a comment
        self.__next_token += self.__file.read(NUMBER_OF_READING_BYTES)
        if self.__next_token == LINE_COMMENT_MARK:
            self.__file.readline()  # skip the line
            return True
        if self.__next_token == BLOCK_COMMENT_START_MARK:
            # searches for the end of the comment mark
            next_char = self.__file.read(len(BLOCK_COMMENT_END_MARK))
            while next_char != BLOCK_COMMENT_END_MARK:
                next_char = next_char[1:]
                next_char += self.__file.read(NUMBER_OF_READING_BYTES)
            return True
        return False
