from lexer import TokenType
from parser import *

class AsmGenerator:
    def __init__(self):
        self.data_section = []
        self.text_section = []
        self.variables = {} # name -> offset from RBP
        self.stack_offset = 0
        self.label_count = 0

    def next_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        self.text_section.append("section .text")
        self.text_section.append("global _start")
        self.text_section.append("_start:")
        
        # Prologue
        self.text_section.append("    push rbp")
        self.text_section.append("    mov rbp, rsp")
        
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generate_stmt(stmt)
        
        # Epilogue & Exit syscall
        self.text_section.append("    mov rsp, rbp")
        self.text_section.append("    pop rbp")
        self.text_section.append("    mov rax, 60") # exit
        self.text_section.append("    xor rdi, rdi") # status 0
        self.text_section.append("    syscall")
        
        # Data section
        asm = "section .data\n"
        for line in self.data_section:
            asm += f"    {line}\n"
        asm += "\n"
        
        # Text section
        for line in self.text_section:
            asm += f"{line}\n"
        
        return asm

    def generate_stmt(self, node):
        if isinstance(node, VarAssign):
            name = node.name.replace('$', '')
            if name not in self.variables:
                self.stack_offset += 8
                self.variables[name] = self.stack_offset
                self.text_section.append(f"    sub rsp, 8 ; Allocate for {name}")
            
            self.generate_expr(node.value)
            self.text_section.append(f"    mov [rbp-{self.variables[name]}], rax")
            
        elif isinstance(node, PrintStmt):
            if isinstance(node.expression, Literal) and isinstance(node.expression.value, str):
                label = self.next_label()
                val = node.expression.value
                # In a real compiler, we'd handle string escapes and lengths properly
                self.data_section.append(f"{label} db '{val}', 10") # 10 is newline
                self.data_section.append(f"{label}_len equ $ - {label}")
                
                self.text_section.append(f"    mov rax, 1 ; write")
                self.text_section.append(f"    mov rdi, 1 ; stdout")
                self.text_section.append(f"    mov rsi, {label}")
                self.text_section.append(f"    mov rdx, {label}_len")
                self.text_section.append(f"    syscall")
            else:
                # For numbers, we'd need a number-to-string routine in assembly
                # For this MVP, let's just print a placeholder or handle simple case
                self.generate_expr(node.expression)
                # We'll skip complex number printing in raw assembly for this demo
                # and just focus on the fact that it's generating real machine instructions
                self.text_section.append("    ; Number printing would go here (complex in raw asm)")
                
        elif isinstance(node, IfStmt):
            self.generate_expr(node.condition)
            label_else = self.next_label()
            label_end = self.next_label()
            
            self.text_section.append("    cmp rax, 0")
            self.text_section.append(f"    je {label_else}")
            
            for stmt in node.then_branch:
                self.generate_stmt(stmt)
            self.text_section.append(f"    jmp {label_end}")
            
            self.text_section.append(f"{label_else}:")
            if node.else_branch:
                for stmt in node.else_branch:
                    self.generate_stmt(stmt)
            self.text_section.append(f"{label_end}:")

    def generate_expr(self, node):
        if isinstance(node, Literal):
            if isinstance(node.value, (int, float)):
                self.text_section.append(f"    mov rax, {int(node.value)}")
            return
        
        elif isinstance(node, VarAccess):
            name = node.name.replace('$', '')
            if name in self.variables:
                self.text_section.append(f"    mov rax, [rbp-{self.variables[name]}]")
            else:
                self.text_section.append("    mov rax, 0")
            return

        elif isinstance(node, BinaryOp):
            self.generate_expr(node.right)
            self.text_section.append("    push rax")
            self.generate_expr(node.left)
            self.text_section.append("    pop rbx")
            
            op = node.op.value
            if op == "+": self.text_section.append("    add rax, rbx")
            elif op == "-": self.text_section.append("    sub rax, rbx")
            elif op == "*": self.text_section.append("    imul rax, rbx")
            elif op == "/": 
                self.text_section.append("    cqo")
                self.text_section.append("    idiv rbx")
            elif op == ">":
                self.text_section.append("    cmp rax, rbx")
                self.text_section.append("    setg al")
                self.text_section.append("    movzx rax, al")
            elif op == "<":
                self.text_section.append("    cmp rax, rbx")
                self.text_section.append("    setl al")
                self.text_section.append("    movzx rax, al")
            elif op == "==":
                self.text_section.append("    cmp rax, rbx")
                self.text_section.append("    sete al")
                self.text_section.append("    movzx rax, al")
            return
