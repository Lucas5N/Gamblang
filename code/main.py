import os
import subprocess
import sys

from lark import Lark

from codegen import GAMBLANGCompiler
from semantics import controllo_semantico


def main():
    if len(sys.argv) < 2:
        print("Errore: Nessun file di input specificato.")
        print("Uso corretto: ./gamblang <nome_file.gamblang>")
        sys.exit(1)

    source_file = sys.argv[1]

    if not os.path.exists(source_file):
        print(f"Il file '{source_file}' non esiste")
        sys.exit(1)

    with open(source_file, "r") as f:
        source = f.read()

    with open("gamblang.lark", "r") as ff:
        grammar = ff.read()

    parser = Lark(grammar, parser="lalr")

    print("<--PARSING-->")
    try:
        ast = parser.parse(source)
        print("--<PARSING FINITO--<")

        print("<--ANALISI SEMANTICA-->")
        symbol_table = controllo_semantico(ast)

        print("--<ANALISI SEMANTICA FINITA--<")
        print(symbol_table)

        print("<--CODE-GEN-->")
        compiler = GAMBLANGCompiler(symbol_table)
        c_code = compiler.visit(ast)

        with open("output.c", "w") as f:
            if isinstance(c_code, list):
                f.write("\n".join(c_code))
            else:
                f.write(c_code)

        print("--<COMPILAZIONE COMPLETATA--<")

        if sys.platform == "win32":
            executable = "output.exe"
            compile_cmd = ["gcc", "output.c", "-o", executable]
            run_cmd = [executable]
        else:
            executable = "output"
            compile_cmd = ["gcc", "output.c", "-o", executable]
            run_cmd = ["./" + executable]

        subprocess.run(compile_cmd, check=True)
        subprocess.run(run_cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"\nERRORE DI COMPILAZIONE/ESECUZIONE C (vedi output sopra)")
    except Exception as e:
        print(f"\nERRORE DI COMPILAZIONE : {e}")


if __name__ == "__main__":
    main()
