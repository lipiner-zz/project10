from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE, TAG_CLOSER, TAG_SUFFIX, TAG_PREFIX

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP_LIST = ['-', '~']
CLASS_TAG = "class"
CLASS_VAR_TAG = "classVarDec"
SUBROUTINE_DEC_TAG = "subroutineDec"
ADDITIONAL_VAR_OPTIONAL_MARK = ","
TAG_OPENER = "\t"


class CompilationEngine:

    def __init__(self, input_stream, output_stream):
        """
        Creates a new compilation engine with the
        given input and output. The next routine
        called must be compileClass().
        """
        self.__prefix = ""
        self.__tokenizer = JackTokenizer(input_stream)
        self.__output_stream = output_stream

    def compile(self):
        """
        Compiles the whole file
        :return: True iff the file was compiled successfully
        """
        return self.__compile_class()

    def __compile_class(self):
        """
        Compiles a complete class
        :return: True iff the class was compiled successfully
        """
        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(CLASS_TAG))

        # checks for the next parts of the class and writes them to the file
        self.__check_keyword_symbol(KEYWORD_TYPE)
        self.__check_keyword_symbol(IDENTIFIER_TYPE)
        self.__check_keyword_symbol(SYMBOL_TYPE)
        if not self.__tokenizer.has_more_tokens():
            return False  # should have more tokens

        # checks for optional classVerDec and subroutineDec
        self.__tokenizer.advance()
        while self.__compile_class_var_dec() and self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
        while self.__compile_subroutine() and self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()

        if not self.__tokenizer.has_more_tokens():
            return False  # should have more tokens
        else:
            self.__check_keyword_symbol(SYMBOL_TYPE)  # block closer

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(CLASS_TAG, TAG_CLOSER))

    def __compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration
        :return:
        """
        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG))

        self.__check_keyword_symbol(KEYWORD_TYPE)
        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)
        self.__check_keyword_symbol(SYMBOL_TYPE)
        while self.__tokenizer.get_value() == ADDITIONAL_VAR_OPTIONAL_MARK:
            self.__check_keyword_symbol(IDENTIFIER_TYPE)
            self.__check_keyword_symbol(SYMBOL_TYPE)

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG, TAG_CLOSER))

    def __compile_subroutine(self):
        pass

    def __compile_parameter_list(self):
        pass

    def __compile_var_dec(self):
        pass

    def __compile_statements(self):
        pass

    def __compile_do(self):
        pass

    def __compile_let(self):
        pass

    def __compile_while(self):
        pass

    def __compile_return(self):
        pass

    def __compile_if(self):
        pass

    def __compile_expression(self):
        pass

    def __compile_term(self):
        pass

    def __compile_expression_list(self):
        pass

    def __check_keyword_symbol(self, token_type, value_list=None):
        """
        checks if the current token is from token_type (which is keyword or symbol), and it's value is one of the
        given optional values (in the value_list). If so, writes the token string to the output file
        :param token_type: the wanted type of the current token: keyword or symbol
        :param value_list: a list of optional values for the current token
        :return: True if the current token is from Keyword type, and it's value exists in the keyword list,
          and false otherwise
        """
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token_type() == token_type:
                if value_list is None or self.__tokenizer.get_value() in value_list:
                    self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
                    return True

        return False

    def __check_type(self):
        pass

    def __check_op(self):
        """
        :return: true iff the current token is a symbol containing an operation
        """
        return self.__check_keyword_symbol(OP_LIST, SYMBOL_TYPE)

    def __check_unary_op(self):
        """
        :return: true iff the current token is a symbol containing an unary operation
        """
        return self.__check_keyword_symbol(UNARY_OP_LIST, SYMBOL_TYPE)

    def __create_tag(self, tag, closer=''):
        """
        Creates the type tag in its format
        :param tag: The actual tag
        :param closer: the closer note if there should be one. Otherwise it has default empty value
        :return: the type tag
        """
        if closer:
            # the closer is not empty - decrementing it and set the prefix to be after the changing
            self.__prefix = self.__prefix[:-len(TAG_OPENER)]
            prefix = self.__prefix
        else:
            # the closer is empty - saves the current prefix before incrementing it for the next tag
            prefix = self.__prefix
            self.__prefix += TAG_OPENER

        return prefix + TAG_PREFIX + closer + tag + TAG_SUFFIX
