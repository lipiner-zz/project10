from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP_LIST = ['-', '~']


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
        pass

    def compile_class(self):
        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

    def check_keyword_symbol(self, value_list, token_type):
        """
        checks if the current token is from token_type (which is keyword or symbol), and it's value is one of the
        given optional values (in the value_list). If so, writes the token string to the output file
        :param token_type: the wanted type of the current token: keyword of symbol
        :param value_list: a list of optional values for the current token
        :return: True if the current token is from Keyword type, and it's value exists in the keyword list,
          and false otherwise
        """
        if self.__tokenizer.get_token_type() == KEYWORD_TYPE:
            if self.__tokenizer.get_value() in value_list:
                self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
                return True

        return False

    def check_type(self):
        pass

    def check_op(self):
        """
        :return: true iff the current token is a symbol containing an operation
        """
        return self.check_keyword_symbol(OP_LIST, SYMBOL_TYPE)

    def check_unary_op(self):
        """
        :return: true iff the current token is a symbol containing an unary operation
        """
        return self.check_keyword_symbol(UNARY_OP_LIST, SYMBOL_TYPE)

