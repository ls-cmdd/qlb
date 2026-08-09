from lexer import TokenType

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarAssign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStmt(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class PrintStmt(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class VarAccess(ASTNode):
    def __init__(self, name):
        self.name = name

class Call(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token().type == token_type:
            token = self.current_token()
            self.pos += 1
            return token
        else:
            raise Exception(f"خطأ نحوي: توقعت {token_type} ولكن وجدت {self.current_token().type} في {self.current_token().line}:{self.current_token().column}")

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        token = self.current_token()
        if token.type == TokenType.IDENTIFIER and self.tokens[self.pos+1].type == TokenType.ASSIGN:
            return self.assign_stmt()
        elif token.type == TokenType.IF:
            return self.if_stmt()
        elif token.type == TokenType.WHILE:
            return self.while_stmt()
        elif token.type == TokenType.PRINT:
            return self.print_stmt()
        else:
            expr = self.expression()
            if self.current_token().type == TokenType.DOT:
                self.eat(TokenType.DOT)
            return expr

    def assign_stmt(self):
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.ASSIGN)
        value = self.expression()
        if self.current_token().type == TokenType.DOT:
            self.eat(TokenType.DOT)
        return VarAssign(name, value)

    def if_stmt(self):
        self.eat(TokenType.IF)
        condition = self.expression()
        self.eat(TokenType.COLON)
        then_branch = []
        while self.current_token().type not in [TokenType.ELSE, TokenType.END, TokenType.EOF]:
            then_branch.append(self.statement())
        
        else_branch = None
        if self.current_token().type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            else_branch = []
            while self.current_token().type not in [TokenType.END, TokenType.EOF]:
                else_branch.append(self.statement())
        
        self.eat(TokenType.END)
        return IfStmt(condition, then_branch, else_branch)

    def while_stmt(self):
        self.eat(TokenType.WHILE)
        condition = self.expression()
        self.eat(TokenType.COLON)
        body = []
        while self.current_token().type not in [TokenType.END, TokenType.EOF]:
            body.append(self.statement())
        self.eat(TokenType.END)
        return WhileStmt(condition, body)

    def print_stmt(self):
        self.eat(TokenType.PRINT)
        expr = self.expression()
        if self.current_token().type == TokenType.DOT:
            self.eat(TokenType.DOT)
        return PrintStmt(expr)

    def expression(self):
        return self.comparison()

    def comparison(self):
        left = self.term()
        while self.current_token().type in [TokenType.GT, TokenType.LT, TokenType.EQ, TokenType.NEQ]:
            op = self.eat(self.current_token().type)
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.eat(self.current_token().type)
            right = self.factor()
            left = BinaryOp(left, op, right)
        return left

    def factor(self):
        left = self.call()
        while self.current_token().type in [TokenType.MUL, TokenType.DIV]:
            op = self.eat(self.current_token().type)
            right = self.call()
            left = BinaryOp(left, op, right)
        return left

    def call(self):
        expr = self.primary()
        while True:
            if self.current_token().type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                arguments = []
                if self.current_token().type != TokenType.RPAREN:
                    arguments.append(self.expression())
                    while self.current_token().type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        arguments.append(self.expression())
                self.eat(TokenType.RPAREN)
                expr = Call(expr, arguments)
            else:
                break
        return expr

    def primary(self):
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Literal(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return Literal(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return VarAccess(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            raise Exception(f"خطأ نحوي: تعبير غير متوقع {token.type} في {token.line}:{token.column}")
