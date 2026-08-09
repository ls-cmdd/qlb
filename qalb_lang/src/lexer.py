import enum
import re

class TokenType(enum.Enum):
    # Keywords
    IF = "اذا"
    ELSE = "والا"
    WHILE = "طالما"
    FOR = "لكل"
    IN = "في"
    DEF = "دالة"
    CLASS = "صنف"
    RETURN = "ارجع"
    PRINT = "اعرض"
    END = "نهاية"
    IMPORT = "استورد"
    TRY = "حاول"
    CATCH = "امسك"
    NEW = "جديد"
    
    # Symbols
    ASSIGN = "="
    DOT = "."
    COMMA = ","
    COLON = ":"
    LPAREN = "("
    RPAREN = ")"
    VAR_PREFIX = "$"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    EQ = "=="
    NEQ = "!="
    GT = ">"
    LT = "<"
    
    # Literals
    IDENTIFIER = "معرف"
    NUMBER = "رقم"
    STRING = "نص"
    EOF = "نهاية_الملف"

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def error(self, char):
        raise Exception(f"خطأ معجمي: حرف غير معروف '{char}' في السطر {self.line} العمود {self.column}")

    def tokenize(self):
        keywords = {t.value: t for t in TokenType if t not in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING, TokenType.EOF]}
        
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            # Comments
            if char == '#':
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                continue

            # Numbers
            if char.isdigit():
                start_pos = self.pos
                value = ""
                while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
                    value += self.text[self.pos]
                    self.pos += 1
                self.tokens.append(Token(TokenType.NUMBER, float(value) if '.' in value else int(value), self.line, self.column))
                self.column += (self.pos - start_pos)
                continue

            # Identifiers and Keywords
            # Support Arabic letters and English letters
            if char.isalpha() or char == '_' or char == '$':
                start_pos = self.pos
                value = ""
                while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_' or self.text[self.pos] == '$'):
                    value += self.text[self.pos]
                    self.pos += 1
                
                if value.startswith('$'):
                    self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, self.column))
                elif value in keywords:
                    self.tokens.append(Token(keywords[value], value, self.line, self.column))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, self.column))
                
                self.column += (self.pos - start_pos)
                continue

            # Strings
            if char == '"':
                start_pos = self.pos
                self.pos += 1
                value = ""
                while self.pos < len(self.text) and self.text[self.pos] != '"':
                    value += self.text[self.pos]
                    self.pos += 1
                if self.pos >= len(self.text):
                    raise Exception("خطأ: نص غير مغلق")
                self.pos += 1
                self.tokens.append(Token(TokenType.STRING, value, self.line, self.column))
                self.column += (self.pos - start_pos)
                continue

            # Multi-char operators
            if self.text[self.pos:self.pos+2] == "==":
                self.tokens.append(Token(TokenType.EQ, "==", self.line, self.column))
                self.pos += 2
                self.column += 2
                continue
            if self.text[self.pos:self.pos+2] == "!=":
                self.tokens.append(Token(TokenType.NEQ, "!=", self.line, self.column))
                self.pos += 2
                self.column += 2
                continue

            # Single-char symbols/operators
            single_chars = {
                '=': TokenType.ASSIGN,
                '.': TokenType.DOT,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MUL,
                '/': TokenType.DIV,
                '>': TokenType.GT,
                '<': TokenType.LT,
            }

            if char in single_chars:
                self.tokens.append(Token(single_chars[char], char, self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            self.error(char)

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

if __name__ == "__main__":
    code = """
    $س = 10.
    اذا $س > 5:
        اعرض "كبير".
    نهاية
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for t in tokens:
        print(t)
