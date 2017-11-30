KEYWORD_TYPE = "keyword"
SYMBOL_TYPE = "symbol"
INTEGER_CONST_TYPE = "integerConstant"
STRING_COST_TYPE = "StringConstant"
IDENTIFIER_TYPE = "identifier"
KEYWORD_LIST = []
SYMBOL_LIST = []

EOF_NOTE = ''


class JackTokenizer:

    def __init__(self, input_stream):
        self.__file = input_stream
        self.__current_tokens = []

    def has_more_tokens(self):
        if len(self.__current_tokens) == 0:
            line = self.__file.readline()
            if line == EOF_NOTE:
                return False
        else:
            return True

    def advance(self):
        pass

    def token_type(self):
        pass

    def get_keyword(self):
        pass

    def get_symbol(self):
        pass

    def get_identifier(self):
        pass

    def get_int_val(self):
        pass

    def get_string_val(self):
        pass
