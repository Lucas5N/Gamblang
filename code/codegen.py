from lark.visitors import Interpreter


class GAMBLANGCompiler(Interpreter):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.c_lines = []

    def start(self, node):
        self.c_lines.append("#include <stdio.h>")
        self.c_lines.append("#include <stdlib.h>")
        self.c_lines.append("#include <time.h>")
        self.c_lines.append(
            "#define CLAMP_PROB(p) ((p) > 1.0 ? 1.0 : ((p) < 0.00 ? 0.0 : (p)))"
        )
        self.c_lines.append("typedef struct {")
        self.c_lines.append("    double history[100];")
        self.c_lines.append("    int count;")
        self.c_lines.append("} gamble_t;")
        self.c_lines.append("")
        self.c_lines.append("int main() {")
        self.c_lines.append("    srand(time(NULL));")
        self.c_lines.append("")

        self.visit_children(node)

        self.c_lines.append("")
        self.c_lines.append("    return 0;")
        self.c_lines.append("}")

        return "\n".join(self.c_lines)

    def steady_decl(self, node):
        var_name = node.children[0].value
        expr_code = self.visit(node.children[1])
        self.c_lines.append(f"    double {var_name} = {expr_code};")

    def gamble_decl(self, node):
        var_name = node.children[0].value
        expr_code = self.visit(node.children[1])
        self.c_lines.append(f"    gamble_t {var_name};")
        self.c_lines.append(f"    {var_name}.count = 0;")
        self.c_lines.append(
            f"    {var_name}.history[{var_name}.count++] = {expr_code};"
        )

    def coin_decl(self, node):
        var_name = node.children[0].value
        expr_code = self.visit(node.children[1])
        self.c_lines.append(
            f"    double {var_name} = ((double)rand() / RAND_MAX) < CLAMP_PROB({expr_code}) ? 1 : 0;"
        )

    def steady_assign(self, node):
        var_name = node.children[0].value
        expr_code = self.visit(node.children[1])
        self.c_lines.append(f"    {var_name} = {expr_code};")

    def gamble_assign(self, node):
        var_name = node.children[0].value
        expr_code = self.visit(node.children[1])
        self.c_lines.append(
            f"    {var_name}.history[{var_name}.count++] = {expr_code};"
        )

    def cond_atom(self, node):
        left = self.visit(node.children[0])
        op = node.children[1].value
        right = self.visit(node.children[2])
        return f"{left} {op} {right}"

    def ask_stmt(self, node):
        var_name = node.children[0].value
        if self.symbol_table.get(var_name) == "GAMBLE":
            self.c_lines.append("    {")
            self.c_lines.append("        double _tmp;")
            self.c_lines.append('        while (scanf("%lf", &_tmp) != 1) {')
            self.c_lines.append("            int c_scarto;")
            self.c_lines.append(
                "            while ((c_scarto = getchar()) != '\\n' && c_scarto != EOF);"
            )
            self.c_lines.append(
                '            printf("Input non valido inserisci un numero: ");'
            )
            self.c_lines.append("        }")
            self.c_lines.append(
                f"        {var_name}.history[{var_name}.count++] = _tmp;"
            )
            self.c_lines.append("    }")
        else:
            self.c_lines.append(f'    while (scanf("%lf", &{var_name}) != 1) {{')
            self.c_lines.append("        int c_scarto;")
            self.c_lines.append(
                "        while ((c_scarto = getchar()) != '\\n' && c_scarto != EOF);"
            )
            self.c_lines.append(
                '        printf("Input non valido inserisci un numero: ");'
            )
            self.c_lines.append("    }")

    def loop_stmt(self, node):
        cond = self.visit(node.children[0])
        self.c_lines.append(f"    while ({cond}) {{")
        self.visit(node.children[1])
        self.c_lines.append("    }")

    def var(self, node):
        var_name = node.children[0].value
        if self.symbol_table.get(var_name) == "GAMBLE":
            return f"{var_name}.history[rand() % {var_name}.count]"
        else:
            return var_name

    def number(self, node):
        return node.children[0].value

    def print_stmt(self, node):
        expr_code = self.visit(node.children[0])
        self.c_lines.append(f'    printf("%g\\n", {expr_code});')

    def if_stmt(self, node):
        cond = self.visit(node.children[0])
        self.c_lines.append(f"    if ({cond}) {{")
        self.visit(node.children[1])
        if len(node.children) > 2:
            self.c_lines.append("    } else {")
            self.visit(node.children[2])
        self.c_lines.append("    }")

    def and_cond(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} && {right})"

    def or_cond(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} || {right})"

    def not_cond(self, node):
        cond = self.visit(node.children[0])
        return f"(!{cond})"

    def risky_stmt(self, node):
        prob = self.visit(node.children[0])
        self.c_lines.append(
            f"    if (((double)rand() / RAND_MAX) < CLAMP_PROB({prob})) {{"
        )
        self.visit(node.children[1])
        if len(node.children) > 2:
            self.c_lines.append("    } else {")
            self.visit(node.children[2])
        self.c_lines.append("    }")

    def print_str_stmt(self, node):
        raw = node.children[0].value
        inner = raw[1:-1]
        self.c_lines.append(f'    printf("{inner}\\n");')

    def add(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} + {right})"

    def sub(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} - {right})"

    def mul(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} * {right})"

    def div(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"({left} / {right})"

    def neg(self, node):
        operand = self.visit(node.children[0])
        return f"(-{operand})"
