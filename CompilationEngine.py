from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE, TAG_CLOSER, TAG_SUFFIX, TAG_PREFIX

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP_LIST = ['-', '~']
CLASS_TAG = "class"
CLASS_VAR_TAG = "classVarDec"
SUBROUTINE_BODY_TAG = "subroutineBody"
PARAMETERS_LIST_TAG = "parameterList"
CLASS_VAR_DEC_KEYWORDS = ["field, static"]
SUBROUTINE_DEC_TAG = "subroutineDec"
SUBROUTINE_DEC_KEYWORDS = ['constructor', 'function', 'method']
TYPE_LIST = ["int", "char", "boolean"]
STATEMENTS_TAG = "statements"
STATEMENTS_LIST = ['let', 'if', 'while', 'do', 'return']
LET_KEYWORD = "let"
IF_KEYWORD = "if"
WHILE_KEYWORD = "while"
DO_KEYWORD = "do"
RETURN_KEYWORD = "return"
EXPRESSION_TAG = "expression"
ADDITIONAL_VAR_OPTIONAL_MARK = ","
END_LINE_MARK = ";"
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
        self.__check_keyword_symbol(KEYWORD_TYPE)  # "class"
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # className
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "{"
        # if not self.__tokenizer.has_more_tokens():
        #     return False  # should have more tokens
        #
        # # checks for optional classVerDec and subroutineDec
        # self.__tokenizer.advance()
        while self.__compile_class_var_dec():  # and self.__tokenizer.has_more_tokens():
            # self.__tokenizer.advance()
            continue
        while self.__compile_subroutine(False):  # and self.__tokenizer.has_more_tokens():
            # self.__tokenizer.advance()
            continue

        # if not self.__tokenizer.has_more_tokens():
        #     return False  # should have more tokens
        # else:
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # block closer "}"

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(CLASS_TAG, TAG_CLOSER))

    def __compile_class_var_dec(self, make_advance=True):
        """
        Compiles a static declaration or a field declaration
        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid class var declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, CLASS_VAR_DEC_KEYWORDS, make_advance, write_to_file=False):
            # It is not a class var dec
            return False

        # writes to the file the class var dec tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG))

        self.__check_keyword_symbol(KEYWORD_TYPE, CLASS_VAR_DEC_KEYWORDS, make_advance=False)

        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):  # "," more varName
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ";"

        # writes to the file the class var dec end tag
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG, TAG_CLOSER))
        return True

    def __compile_subroutine(self, make_advance=True):
        """
        Compiles a complete method, function, or constructor.
        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid subroutine declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, SUBROUTINE_DEC_KEYWORDS, make_advance, write_to_file=False):
            # It is not a subroutine
            return False

        # writes to the file the subroutine tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(SUBROUTINE_DEC_TAG))

        self.__check_keyword_symbol(KEYWORD_TYPE, SUBROUTINE_DEC_KEYWORDS, make_advance=False)

        if not self.__check_keyword_symbol(KEYWORD_TYPE):  # not void
            self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "("

        # advance was made in the compile_parameter_list without use
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ")"
        self.__compile_subroutine_body()

        # writes to the file the subroutine end tag
        self.__output_stream.write(self.__create_tag(SUBROUTINE_DEC_TAG, TAG_CLOSER))
        return True

    def __compile_subroutine_body(self):
        """
        Compiles a subroutine body
        """
        # writes to the file the subroutine body tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(SUBROUTINE_BODY_TAG))

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'

        # compiles and writes all variable declarations
        while self.__compile_var_dec():
            continue
        # compiles the statements of the subroutine
        self.__compile_statements()

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

        # writes to the file the subroutine body end tag
        self.__output_stream.write(self.__create_tag(SUBROUTINE_BODY_TAG, TAG_CLOSER))

    def __compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list, not including the enclosing “()”.
        In any way, the function advance the tokenizer
        :return: True iff there was a valid parameter list
        """
        if not self.__check_type(write_to_file=False):
            # It is not a parameter list
            return False

        # writes to the file the parameter list tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(PARAMETERS_LIST_TAG))

        self.__check_type(make_advance=False)
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName

        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):  # "," more varName
            self.__check_type()
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName

        # writes to the file the parameter list end tag
        self.__output_stream.write(self.__create_tag(PARAMETERS_LIST_TAG, TAG_CLOSER))
        return True

    def __compile_var_dec(self):
        """
        checks if the current token is set to variable declaration, If so, returns true and writes the tokens
        to the stream. Otherwise, doesn't write to the stream, and returns False
        :return: True iff the current token is set to the beginning of variable declaration
        """
        # checks if the current token is set to 'var', which means it is a var declaration
        if not self.__check_keyword_symbol(KEYWORD_TYPE, write_to_file=False):  # 'var'
            return False

        # writes to the file the var declaration tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(SUBROUTINE_BODY_TAG))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'var'
        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # variableName
        # writes all variables
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):
            self.__check_keyword_symbol(IDENTIFIER_TYPE)

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        # writes to the file the var declaration end tag
        self.__output_stream.write(self.__create_tag(SUBROUTINE_BODY_TAG, TAG_CLOSER))
        return True

    def __compile_statements(self):
        """
        compiles the statements inside a subroutine
        """
        # writes to the file the statements tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(STATEMENTS_TAG))

        # compiling all statements
        while self.__check_keyword_symbol(KEYWORD_TYPE, STATEMENTS_LIST, False, False):
            # checking which statement to compile
            if self.__tokenizer.get_value() == LET_KEYWORD:
                self.__compile_let()
            elif self.__tokenizer.get_value() == DO_KEYWORD:
                self.__compile_do()
            elif self.__tokenizer.get_value() == WHILE_KEYWORD:
                self.__compile_while()
            elif self.__tokenizer.get_value() == RETURN_KEYWORD:
                self.__compile_return()
            else:
                self.__compile_if()

        # writes to the file the statements end tag
        self.__output_stream.write(self.__create_tag(STATEMENTS_TAG, TAG_CLOSER))

    def __compile_do(self):
        pass

    def __compile_let(self):
        pass

    def __compile_while(self):
        pass

    def __compile_return(self):
        # writes to the file the return tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(RETURN_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'return'

        if self.__check_keyword_symbol(SYMBOL_TYPE, [END_LINE_MARK]):
            return
        else:
            self.__compile_expression()

        #### SHOULD MAKE ADVANCE???
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)

        # writes to the file the return end tag
        self.__output_stream.write(self.__create_tag(RETURN_KEYWORD, TAG_CLOSER))

    def __compile_if(self):
        pass

    def __compile_expression(self):
        pass

    def __compile_term(self):
        pass

    def __compile_expression_list(self):
        pass

    def __check_keyword_symbol(self, token_type, value_list=None, make_advance=True, write_to_file=True):
        """
        checks if the current token is from token_type (which is keyword or symbol), and it's value is one of the
        given optional values (in the value_list). If so, writes the token string to the output file
        :param token_type: the wanted type of the current token: keyword or symbol
        :param value_list: a list of optional values for the current token
        :param make_advance: whether or not the method should call tokenizer.advance() at the beginning
        :param write_to_file: whether or not the method should write the token to the file
        :return: True if the current token is from Keyword type, and it's value exists in the keyword list,
          and false otherwise
        """
        if make_advance:
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
            else:
                return False
        if self.__tokenizer.get_token_type() == token_type:
            if value_list is None or self.__tokenizer.get_value() in value_list:
                if write_to_file:
                    self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
                return True

        return False

    def __check_type(self, make_advance=True, write_to_file=True):
        """
        checks if the current token is a type. If so, writes the token to the stream
        :param make_advance: whether or not the method should call tokenizer.advance() at the beginning
        :param write_to_file: whether or not the method should write the token to the file
        :return: true iff the current token is a type
        """
        # checks for builtin types
        if self.__check_keyword_symbol(KEYWORD_TYPE, TYPE_LIST, make_advance, write_to_file):
            return True
        # checks for user-defined class types
        if not self.__check_keyword_symbol(IDENTIFIER_TYPE, make_advance=False, write_to_file=write_to_file):
            return False

        return True

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
