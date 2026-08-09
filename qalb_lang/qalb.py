import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from codegen import PythonGenerator
from c_codegen import CGenerator
from asm_codegen import AsmGenerator
import subprocess

def run(code, interpreter=None):
    if interpreter is None:
        interpreter = Interpreter()
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        return interpreter.interpret(ast)
    except Exception as e:
        print(f"خطأ: {e}")

def repl():
    print("لغة القلب 0.1 - مفسر تفاعلي")
    print("اكتب 'خروج' للمغادرة")
    interpreter = Interpreter()
    while True:
        try:
            text = input("القلب > ")
            if text.strip() == "خروج":
                break
            if not text.strip():
                continue
            run(text, interpreter)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n")
            continue

def compile_to_python(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = PythonGenerator()
        return generator.generate(ast)
    except Exception as e:
        print(f"خطأ في الترجمة: {e}")
        return None

def compile_to_c(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CGenerator()
        return generator.generate(ast)
    except Exception as e:
        print(f"خطأ في توليد كود C: {e}")
        return None

def compile_to_asm(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = AsmGenerator()
        return generator.generate(ast)
    except Exception as e:
        print(f"خطأ في توليد كود التجميع: {e}")
        return None

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "سيادي":
            if len(sys.argv) < 3:
                print("الرجاء تحديد ملف للبناء السيادي")
                return
            filename = sys.argv[2]
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            asm_code = compile_to_asm(code)
            if asm_code:
                asm_filename = filename.replace('.qalb', '.asm')
                obj_filename = filename.replace('.qalb', '.o')
                exe_filename = filename.replace('.qalb', '_سيادي')
                
                with open(asm_filename, 'w', encoding='utf-8') as f:
                    f.write(asm_code)
                
                # Assemble using NASM and link using LD
                try:
                    subprocess.run(["nasm", "-f", "elf64", asm_filename, "-o", obj_filename], check=True)
                    subprocess.run(["ld", obj_filename, "-o", exe_filename], check=True)
                    print(f"تم بناء الملف التنفيذي السيادي (لغة آلة مباشرة) بنجاح: {exe_filename}")
                except subprocess.CalledProcessError:
                    print("خطأ أثناء البناء السيادي (تأكد من تثبيت nasm)")
                except FileNotFoundError:
                    print("خطأ: لم يتم العثور على nasm. يرجى تثبيته باستخدام sudo apt install nasm")

        elif command == "بناء":
            if len(sys.argv) < 3:
                print("الرجاء تحديد ملف للبناء")
                return
            filename = sys.argv[2]
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            c_code = compile_to_c(code)
            if c_code:
                c_filename = filename.replace('.qalb', '.c')
                exe_filename = filename.replace('.qalb', '')
                
                with open(c_filename, 'w', encoding='utf-8') as f:
                    f.write(c_code)
                
                # Compile C to Binary using GCC
                try:
                    subprocess.run(["gcc", c_filename, "-o", exe_filename, "-lm"], check=True)
                    print(f"تم بناء الملف التنفيذي المستقل بنجاح: {exe_filename}")
                except subprocess.CalledProcessError:
                    print("خطأ أثناء التصريف باستخدام GCC")

        elif command == "ترجم":
            if len(sys.argv) < 3:
                print("الرجاء تحديد ملف للترجمة")
                return
            filename = sys.argv[2]
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            py_code = compile_to_python(code)
            if py_code:
                output_file = filename.replace('.qalb', '.py')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(py_code)
                print(f"تمت الترجمة بنجاح إلى: {output_file}")
        else:
            filename = sys.argv[1]
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                run(code)
            else:
                print(f"الملف {filename} غير موجود")
    else:
        repl()

if __name__ == "__main__":
    main()
