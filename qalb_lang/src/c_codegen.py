from lexer import TokenType
from parser import *

class CGenerator:
    def __init__(self):
        self.indent_level = 0
        self.variables = set()

    def indent(self):
        return "    " * self.indent_level

    def collect_variables(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.collect_variables(stmt)
        elif isinstance(node, VarAssign):
            self.variables.add(node.name.replace('$', ''))
            self.collect_variables(node.value)
        elif isinstance(node, BinaryOp):
            self.collect_variables(node.left)
            self.collect_variables(node.right)
        elif isinstance(node, IfStmt):
            self.collect_variables(node.condition)
            for stmt in node.then_branch:
                self.collect_variables(stmt)
            if node.else_branch:
                for stmt in node.else_branch:
                    self.collect_variables(stmt)
        elif isinstance(node, WhileStmt):
            self.collect_variables(node.condition)
            for stmt in node.body:
                self.collect_variables(stmt)
        elif isinstance(node, PrintStmt):
            self.collect_variables(node.expression)
        elif isinstance(node, Call):
            for arg in node.arguments:
                self.collect_variables(arg)

    def generate(self, node):
        self.collect_variables(node)
        
        c_code = "#include <stdio.h>\n#include <math.h>\n#include <stdbool.h>\n\n"
        
        # Standard library aliases in C
        c_code += "#define جذر sqrt\n"
        c_code += "#define جيب sin\n"
        c_code += "#define جيب_تمام cos\n"
        c_code += "#define ط M_PI\n\n"
        
        c_code += "int main() {\n"
        self.indent_level += 1
        
        # Declare variables as doubles for simplicity in this version
        for var in self.variables:
            c_code += f"{self.indent()}double {var} = 0;\n"
        
        c_code += "\n"
        
        if isinstance(node, Program):
            for stmt in node.statements:
                c_code += self.generate_stmt(stmt) + "\n"
        
        c_code += f"{self.indent()}return 0;\n"
        self.indent_level -= 1
        c_code += "}\n"
        return c_code

    def generate_stmt(self, node):
        if isinstance(node, VarAssign):
            name = node.name.replace('$', '')
            return f"{self.indent()}{name} = {self.generate_expr(node.value)};"
        
        elif isinstance(node, PrintStmt):
            expr = self.generate_expr(node.expression)
            # Basic type detection for printf (assuming double for now)
            if isinstance(node.expression, Literal) and isinstance(node.expression.value, str):
                return f'{self.indent()}printf("%s\\n", {expr});'
            else:
                return f'{self.indent()}printf("%g\\n", (double)({expr}));'
            
        elif isinstance(node, IfStmt):
            condition = self.generate_expr(node.condition)
            code = f"{self.indent()}if ({condition}) {{\n"
            self.indent_level += 1
            for stmt in node.then_branch:
                code += self.generate_stmt(stmt) + "\n"
            self.indent_level -= 1
            code += f"{self.indent()}}}"
            
            if node.else_branch is not None:
                code += " else {\n"
                self.indent_level += 1
                for stmt in node.else_branch:
                    code += self.generate_stmt(stmt) + "\n"
                self.indent_level -= 1
                code += f"{self.indent()}}}"
            return code
            
        elif isinstance(node, WhileStmt):
            condition = self.generate_expr(node.condition)
            code = f"{self.indent()}while ({condition}) {{\n"
            self.indent_level += 1
            for stmt in node.body:
                code += self.generate_stmt(stmt) + "\n"
            self.indent_level -= 1
            code += f"{self.indent()}}}"
            return code
            
        elif isinstance(node, Call):
            return f"{self.indent()}{self.generate_expr(node)};"
            
        return f"{self.indent()}// Unknown statement: {type(node)}"

    def generate_expr(self, node):
        if isinstance(node, VarAccess):
            return node.name.replace('$', '')
        
        elif isinstance(node, Literal):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        
        elif isinstance(node, BinaryOp):
            left = self.generate_expr(node.left)
            right = self.generate_expr(node.right)
            op = node.op.value
            if op == "==": return f"({left} == {right})"
            if op == "!=": return f"({left} != {right})"
            return f"({left} {op} {right})"
        
        elif isinstance(node, Call):
            callee = self.generate_expr(node.callee)
            args = ", ".join([self.generate_expr(arg) for arg in node.arguments])
            return f"{callee}({args})"
            
        return "0"
