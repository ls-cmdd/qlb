from lexer import TokenType
from parser import *

class PythonGenerator:
    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def generate(self, node):
        if isinstance(node, Program):
            lines = []
            for stmt in node.statements:
                lines.append(self.generate(stmt))
            return "\n".join(lines)
        
        elif isinstance(node, VarAssign):
            # Clean variable name for Python (remove $)
            py_name = node.name.replace('$', '')
            return f"{self.indent()}{py_name} = {self.generate(node.value)}"
        
        elif isinstance(node, VarAccess):
            return node.name.replace('$', '')
        
        elif isinstance(node, Literal):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        
        elif isinstance(node, BinaryOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            op = node.op.value
            return f"({left} {op} {right})"
        
        elif isinstance(node, PrintStmt):
            return f"{self.indent()}print({self.generate(node.expression)})"
            
        elif isinstance(node, IfStmt):
            condition = self.generate(node.condition)
            code = f"{self.indent()}if {condition}:\n"
            self.indent_level += 1
            for stmt in node.then_branch:
                code += self.generate(stmt) + "\n"
            self.indent_level -= 1
            
            if node.else_branch is not None:
                code += f"\n{self.indent()}else:\n"
                self.indent_level += 1
                if len(node.else_branch) == 0:
                    code += f"{self.indent()}pass\n"
                else:
                    for stmt in node.else_branch:
                        code += self.generate(stmt) + "\n"
                self.indent_level -= 1
            return code.strip()
            
        elif isinstance(node, WhileStmt):
            condition = self.generate(node.condition)
            code = f"{self.indent()}while {condition}:\n"
            self.indent_level += 1
            if len(node.body) == 0:
                code += f"{self.indent()}pass\n"
            else:
                for stmt in node.body:
                    code += self.generate(stmt) + "\n"
            self.indent_level -= 1
            return code.strip()
            
        return f"# Unknown node: {type(node)}"
