section .data
    L1 db 'أنا لغة القلب، أتحدث لغة الآلة مباشرة!', 10
    L1_len equ $ - L1
    L2 db 'لا أحتاج لمفسر، ولا للغة وسيطة.', 10
    L2_len equ $ - L2
    L5 db 'الحساب صحيح في سجلات المعالج!', 10
    L5_len equ $ - L5

section .text
global _start
_start:
    push rbp
    mov rbp, rsp
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rsi, L1
    mov rdx, L1_len
    syscall
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rsi, L2
    mov rdx, L2_len
    syscall
    sub rsp, 8 ; Allocate for س
    mov rax, 5
    mov [rbp-8], rax
    sub rsp, 8 ; Allocate for ص
    mov rax, 10
    mov [rbp-16], rax
    sub rsp, 8 ; Allocate for ج
    mov rax, [rbp-16]
    push rax
    mov rax, [rbp-8]
    pop rbx
    add rax, rbx
    mov [rbp-24], rax
    mov rax, 15
    push rax
    mov rax, [rbp-24]
    pop rbx
    cmp rax, rbx
    sete al
    movzx rax, al
    cmp rax, 0
    je L3
    mov rax, 1 ; write
    mov rdi, 1 ; stdout
    mov rsi, L5
    mov rdx, L5_len
    syscall
    jmp L4
L3:
L4:
    mov rsp, rbp
    pop rbp
    mov rax, 60
    xor rdi, rdi
    syscall
