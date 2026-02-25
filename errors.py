"""Error handling"""

class AryanBlockError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format())
    
    def format(self):
        if self.line:
            return f"Error at line {self.line}, column {self.column}: {self.message}"
        return f"Error: {self.message}"

class LexerError(AryanBlockError):
    pass

class ParseError(AryanBlockError):
    pass

class RuntimeError(AryanBlockError):
    pass
