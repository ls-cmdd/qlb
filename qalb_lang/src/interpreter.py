from lexer import TokenType
from parser import *
from stdlib import get_stdlib

class Interpreter:
    def __init__(self):
            self.variables = get_stdlib()

    def interpret(self, node):
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.interpret(stmt)
            return result
        
        elif isinstance(node, VarAssign):
            value = self.interpret(node.value)
            self.variables[node.name] = value
            return value
        
        elif isinstance(node, VarAccess):
            if node.name in self.variables:
                return self.variables[node.name]
            raise Exception(f"خطأ في التنفيذ: المتغير '{node.name}' غير معرف")
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, BinaryOp):
            left = self.interpret(node.left)
            right = self.interpret(node.right)
            
            if node.op.type == TokenType.PLUS: return left + right
            if node.op.type == TokenType.MINUS: return left - right
            if node.op.type == TokenType.MUL: return left * right
            if node.op.type == TokenType.DIV: return left / right
            if node.op.type == TokenType.GT: return left > right
            if node.op.type == TokenType.LT: return left < right
            if node.op.type == TokenType.EQ: return left == right
            if node.op.type == TokenType.NEQ: return left != right
            
        elif isinstance(node, PrintStmt):
            value = self.interpret(node.expression)
            print(value)
            return value
            
        elif isinstance(node, IfStmt):
            condition = self.interpret(node.condition)
            if condition:
                for stmt in node.then_branch:
                    self.interpret(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self.interpret(stmt)
            return None
            
        elif isinstance(node, WhileStmt):
            while self.interpret(node.condition):
                for stmt in node.body:
                    self.interpret(stmt)
            return None
            
        elif isinstance(node, Call):
            callee = self.interpret(node.callee)
            arguments = [self.interpret(arg) for arg in node.arguments]
            if callable(callee):
                return callee(*arguments)
            raise Exception(f"خطأ في التنفيذ: '{node.callee}' ليس دالة قابلة للاستدعاء")
            
        raise Exception(f"عقدة غير معروفة: {type(node)}")
