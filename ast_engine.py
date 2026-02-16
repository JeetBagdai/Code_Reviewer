import ast
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
api_key: Optional[str] = os.getenv("GROQ_API_KEY")
llm: ChatGroq = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)
print("Groq model initialized.")
def parse_code(code: str) -> Optional[ast.AST]:
    try:
        tree: ast.AST = ast.parse(code)
        print("Code parsed successfully.")
        return tree
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return None
def unparse_code(tree: ast.AST) -> Optional[str]:
    try:
        source_code: str = ast.unparse(tree)
        return source_code
    except Exception as e:
        print(f"Error unparsing code: {e}")
        return None
def main() -> None:
    filename: str = "test_input.py"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Usage: python ast_engine.py <filename>")
        print("Defaulting to 'test_input.py' for demonstration.")
    try:
        with open(filename, "r") as f:
            code: str = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    print(f"--- Parsing Code from {filename} ---")
    tree: Optional[ast.AST] = parse_code(code)
    if tree:
        print("\n--- AST Dump (Partial) ---")
        dump: str = ast.dump(tree, indent=4)
        print(dump[:500] + "..." if len(dump) > 500 else dump)
        print("\n--- Unparsing Code ---")
        unparsed: Optional[str] = unparse_code(tree)
        if unparsed:
            print("Unparsing successful.")
if __name__ == "__main__":
    main()
