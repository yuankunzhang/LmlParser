class LmlParser:
    '''
    AWS's API gateway does some black magic to perfectly mess up our JSON data.
    That's why we need this parse_valuer to save the world.

    It parse_values a source string to a Python dictionary. Format of the source
    string is defined below.

    * The source string begins with a '{', leading white spaces are allowed.
    * Each '{' has an enclosing '}', otherwise the source string is malformed.
    * Two data types are allowed:
        * Strings are specified by a sequence of raw characters.
        * Objects are specified by a pair of '{' and '}'.
    * Elements of an object is specified by this format: key=value.
    * Elements of an object is split by ',', a trailing ',' after the last
      element is allowed: {key1=value1, key2=value2,}.

    For example, this is a valid source string:

    '{product1={id=gold1, price=13}, product2={id=gold2, price=26}}'
    '''

    def __init__(self, source):
        # the source string
        self.source = source
        # current position
        self.at = 0
        # current character
        self.ch = source[0] if len(source) > 0 else ''

    def error(self, msg):
        '''Print an error message and raise an exception'''

        print '-- Parser abort due to a fatal error: \n-- %s' % msg
        raise ValueError()

    def check_char(self, expected):
        '''
        Check if current character is same as the given character.
        If not, raise an exception.
        '''

        if self.at >= len(self.source):
            self.error('At position %d: %c expected, but reached string end' % (self.at, expected))
        elif self.ch != expected:
            self.error('At position %d: %c expected, but %c given' % (self.at, expected, self.ch))

    def next_char(self):
        '''Move on to next character in source string.'''

        self.at += 1
        self.ch = self.source[self.at] if len(self.source) > self.at else ''
        return self.ch

    def eat_spaces(self):
        '''Eat up white spaces.'''

        while self.ch == ' ':
            self.next_char()

    def parse_string(self):
        '''Parse a string value.'''

        s_list = []
        while self.ch not in ('=', ',', '}') and self.at < len(self.source):
            s_list.append(self.ch)
            self.next_char()
        s = ''.join(s_list)
        return s.strip()

    def parse_object(self):
        '''Parse an object value.'''

        obj = {}

        # eat '{'
        self.next_char()
        self.eat_spaces()

        while self.ch != '}':
            if self.at >= len(self.source):
                self.error('Malformed source string')

            key = self.parse_string()
            # eat '='
            self.check_char('=')
            self.next_char()
            val = self.parse_value()
            obj[key] = val
            # eat ','
            if self.ch == ',':
                self.next_char()
            self.eat_spaces()

        # eat '}'
        self.next_char()

        return obj

    def parse_value(self):
        '''Parse a value.'''

        self.eat_spaces()
        if self.ch == '{':
            return self.parse_object()
        else:
            return self.parse_string()

    def parse(self):
        '''Let the game begin.'''

        self.eat_spaces()
        if self.ch != '{':
            self.error('Source string must begin with \'{\'')
        else:
            return self.parse_value()
