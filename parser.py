class LmlParser:

    def __init__(self, source):
        self.source = source
        self.at = 0
        self.ch = source[0] if len(source) > 0 else ''

    def error(self, msg):
        print '-- Parser abort due to a fatal error: \n-- %s' % msg
        raise ValueError()

    def check_char(self, expected):
        if self.at >= len(self.source):
            self.error('At position %d: %c expected, but reached string end' % (self.at, expected))
        elif self.ch != expected:
            self.error('At position %d: %c expected, but %c given' % (self.at, expected, self.ch))

    def next_char(self):
        self.at += 1
        self.ch = self.source[self.at] if len(self.source) > self.at else ''
        return self.ch

    def eat_spaces(self):
        while self.ch == ' ':
            self.next_char()

    def parse_string(self):
        s = ''
        while self.ch != '=' and self.ch != ',' and self.ch != '}' and self.at < len(self.source):
            s += self.ch
            self.next_char()
        return s.strip()

    def parse_object(self):
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
            val = self.parse()
            obj[key] = val
            # eat ','
            if self.ch == ',':
                self.next_char()
            self.eat_spaces()

        # no need to handle with the tailing '}'
        return obj

    def parse(self):
        self.eat_spaces()
        if self.ch == '{':
            return self.parse_object()
        else:
            return self.parse_string()
