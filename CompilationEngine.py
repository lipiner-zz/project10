from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE, TAG_CLOSER, TAG_SUFFIX, TAG_PREFIX

OP_LIST = ['+', '-', '*', '/', '&amp', '|', '&lt', '&gt', '=']
UNARY_OP_LIST = ['-', '~']
COMPILER_TAG = "tokens"
CLASS_TAG = "class"
CLASS_VAR_TAG = "classVarDec"
SUBROUTINE_BODY_TAG = "subroutineBody"
VAR_DEC_TAG = "varDec"
PARAMETERS_LIST_TAG = "parameterList"
CLASS_VAR_DEC_KEYWORDS = ["field", "static"]
SUBROUTINE_DEC_TAG = "subroutineDec"
SUBROUTINE_DEC_KEYWORDS = ['constructor', 'function', 'method']
VAR_KEYWORDS = ['var']
TYPE_LIST = ["int", "char", "boolean"]
STATEMENTS_TAG = "statements"
STATEMENTS_LIST = ['let', 'if', 'while', 'do', 'return']
LET_KEYWORD = "let"
IF_KEYWORD = "if"
ELSE_KEYWORD = "else"
WHILE_KEYWORD = "while"
DO_KEYWORD = "do"
RETURN_KEYWORD = "return"
EXPRESSION_TAG = "expression"
TERM_TAG = "term"
EXPRESSION_LIST_TAG = "expressionList"
ADDITIONAL_VAR_OPTIONAL_MARK = ","
END_LINE_MARK = ";"
OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OPEN_ARRAY_ACCESS_BRACKET = '['
CALL_CLASS_METHOD_MARK = "."
FUNCTION_CALL_MARKS = [OPEN_BRACKET, CALL_CLASS_METHOD_MARK]
KEYWORD_CONSTANT_LIST = ["true", "false", "null", "this"]
TAG_OPENER = "\t"
TAG_END_OF_LINE = "\n"


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
        """
        self.__create_tag(COMPILER_TAG)
        self.__compile_class()
        self.__create_tag(COMPILER_TAG, TAG_CLOSER)

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
        while self.__compile_subroutine(False):
            self.__advance_tokenizer()

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
            self.__check_type(False)
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "("

        self.__compile_parameter_list()
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
        if not self.__check_keyword_symbol(KEYWORD_TYPE, VAR_KEYWORDS, write_to_file=False):  # 'var'
            return False

        # writes to the file the var declaration tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(VAR_DEC_TAG))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'var'
        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # variableName
        # writes all variables
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):
            self.__check_keyword_symbol(IDENTIFIER_TYPE)

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        # writes to the file the var declaration end tag
        self.__output_stream.write(self.__create_tag(VAR_DEC_TAG, TAG_CLOSER))
        return True

    def __compile_statements(self):
        """
        compiles the statements inside a subroutine.
        Assumes the tokenizer is advanced for the first call.
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
        """
        Compiles a do statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end
        """
        # writes to the file the do tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(DO_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'do'

        # advance the tokenizer for the subroutine call
        self.__advance_tokenizer()
        self.__check_subroutine_call()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        self.__advance_tokenizer()

        # writes to the file the do end tag
        self.__output_stream.write(self.__create_tag(DO_KEYWORD, TAG_CLOSER))

    def __compile_let(self):
        """
        Compiles a let statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        # writes to the file the let tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(LET_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'let'

        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
        if self.__check_keyword_symbol(SYMBOL_TYPE, OPEN_ARRAY_ACCESS_BRACKET):  # '['
            # advance the tokenizer for the expression
            self.__advance_tokenizer()
            self.__compile_expression()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ']'
            self.__check_keyword_symbol(SYMBOL_TYPE)  # '='
        else:  # without calling advance
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '='

        # advance the tokenizer for the expression
        self.__advance_tokenizer()
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        self.__advance_tokenizer()

        # writes to the file the let end tag
        self.__output_stream.write(self.__create_tag(LET_KEYWORD, TAG_CLOSER))

    def __compile_while(self):
        """
        Compiles a while statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        # writes to the file the while tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(WHILE_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'while'

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '('
        # advance the tokenizer for the expression
        self.__advance_tokenizer()
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
        # advance the tokenizer for the statements
        self.__advance_tokenizer()
        self.__compile_statements()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

        self.__advance_tokenizer()

        # writes to the file the while end tag
        self.__output_stream.write(self.__create_tag(WHILE_KEYWORD, TAG_CLOSER))

    def __compile_return(self):
        """
        Compiles a return statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        # writes to the file the return tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(RETURN_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'return'

        if not self.__check_keyword_symbol(SYMBOL_TYPE, [END_LINE_MARK]):
            self.__compile_expression()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)

        self.__advance_tokenizer()

        # writes to the file the return end tag
        self.__output_stream.write(self.__create_tag(RETURN_KEYWORD, TAG_CLOSER))

    def __compile_if(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        # writes to the file the if tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(IF_KEYWORD))

        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'if'

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '('
        # advance the tokenizer for the expression
        self.__advance_tokenizer()
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
        # advance the tokenizer for the statements
        self.__advance_tokenizer()
        self.__compile_statements()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

        if self.__check_keyword_symbol(KEYWORD_TYPE, [ELSE_KEYWORD]):  # 'else'
            self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
            # advance the tokenizer for the statements
            self.__advance_tokenizer()
            self.__compile_statements()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'
            self.__advance_tokenizer()

        # writes to the file the if end tag
        self.__output_stream.write(self.__create_tag(IF_KEYWORD, TAG_CLOSER))

    def __compile_expression(self):
        """
        compiles an expression
        """
        # writes to the file the expression tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(EXPRESSION_TAG))

        # compiles the first term
        self.__compile_term()

        # compiles all the op + term that exists
        while self.__check_op(False):
            self.__advance_tokenizer()
            self.__compile_term()

        # writes to the file the expression end tag
        self.__output_stream.write(self.__create_tag(EXPRESSION_TAG, TAG_CLOSER))

    def __compile_term(self):
        """
        compiles a term
        """
        # writes to the file the term tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(TERM_TAG))

        # checks for all the term options:
        # integer/string constant
        if self.__tokenizer.get_token_type() in [INTEGER_CONST_TYPE, STRING_CONST_TYPE]:
            self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
            self.__advance_tokenizer()
        # keyword constant
        elif self.__check_keyword_symbol(KEYWORD_TYPE, KEYWORD_CONSTANT_LIST, False):
            self.__advance_tokenizer()
        # (expression)
        elif self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_BRACKET], False):
            self.__advance_tokenizer()
            self.__compile_expression()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
            self.__advance_tokenizer()
        # unaryOp + term
        elif self.__check_unary_op(False):
            self.__advance_tokenizer()
            self.__compile_term()
        # varName / varName[expression] / subroutineCall- in any case, starts with identifier
        else:
            if not self.__check_subroutine_call():  # anyway writes the identifier
                # checks for varName[expression]
                if self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_ARRAY_ACCESS_BRACKET], False):
                    self.__advance_tokenizer()
                    self.__compile_expression()
                    self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ']'
                    self.__advance_tokenizer()

        # writes to the file the term end tag
        self.__output_stream.write(self.__create_tag(TERM_TAG, TAG_CLOSER))

    def __check_subroutine_call(self):
        """
        checks if the next tokens are subroutine call. In any case, writes to the stream the first identifier:
        subroutine/class/variable name
        :return: true iff the next tokens are subroutine calls
        """
        self.__check_keyword_symbol(IDENTIFIER_TYPE, make_advance=False)  # subroutine/class/var name

        # checks if the next token is '(' : regular subroutine call
        if self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_BRACKET]):
            self.__compile_expression_list()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
        # checks if the next token is '.' : method call
        elif self.__check_keyword_symbol(SYMBOL_TYPE, [CALL_CLASS_METHOD_MARK], False):
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
            self.__check_keyword_symbol(SYMBOL_TYPE)  # ')'
            self.__compile_expression_list()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '('
        # if the next token is not ( or . : not a subroutine call
        else:
            return False

        self.__advance_tokenizer()
        return True

    def __compile_expression_list(self):
        """
        compiles an expression list
        """
        # writes to the file the expression list tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(EXPRESSION_LIST_TAG))

        self.__advance_tokenizer()

        # if the expression list is not empty: compile all the expression
        if self.__tokenizer.get_value() != CLOSE_BRACKET:
            # compiles the first expression
            self.__compile_expression()

            # checks for more expressions separated with comma
            while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK], False):
                # advances the tokenizer
                self.__advance_tokenizer()
                # compiles the next expression
                self.__compile_expression()

        # writes to the file the expression list end tag
        self.__output_stream.write(self.__create_tag(EXPRESSION_LIST_TAG, TAG_CLOSER))

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

    def __check_op(self, make_advance=True):
        """
        :return: true iff the current token is a symbol containing an operation
        """
        return self.__check_keyword_symbol(SYMBOL_TYPE, OP_LIST, make_advance)

    def __check_unary_op(self, make_advance=True):
        """
        :return: true iff the current token is a symbol containing an unary operation
        """
        return self.__check_keyword_symbol(SYMBOL_TYPE, UNARY_OP_LIST, make_advance)

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

        return prefix + TAG_PREFIX + closer + tag + TAG_SUFFIX + TAG_END_OF_LINE

    def __advance_tokenizer(self):
        """
        advances the inner tokenizer in case when there must be more tokens
        """
        self.__tokenizer.has_more_tokens()  # when there must be more tokens, otherwise the input is invalid
        self.__tokenizer.advance()
