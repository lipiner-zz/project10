from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_COST_TYPE, IDENTIFIER_TYPE


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

    def check_keyword(self, keyword_list):
        if self.__tokenizer.token_type() == KEYWORD_TYPE:
            if self.__tokenizer.get_keyword() in keyword_list:
                self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
                return True

    def check_type(self):
        pass

    def check_op(self):
        pass

    def check_unary_op(self):
        pass

