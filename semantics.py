from lark.visitors import Interpreter


class GAMBLANGSemanticAnalyzer(Interpreter):
    def __init__(self):
        self.symbol_table = {}
        self.gamble_history = {}

    def start(self, node):
        self.visit_children(node)
        return self.symbol_table

    def steady_decl(self, node):
        var_name = node.children[0].value
        if var_name in self.symbol_table:
            raise Exception(f"Errore: ridichiarazione della variabile '{var_name}'")
        self.symbol_table[var_name] = "STEADY"
        if len(node.children) > 1:
            self.visit(node.children[1])

    def gamble_decl(self, node):
        var_name = node.children[0].value
        if var_name in self.symbol_table:
            raise Exception(f"Errore: Ridichiarazione della variabile '{var_name}'")
        self.symbol_table[var_name] = "GAMBLE"
        self.gamble_history[var_name] = 0  # inizializza contatore
        if len(node.children) > 1:
            self.visit(node.children[1])
            self.gamble_history[var_name] = 1  # il <- iniziale conta

    def steady_assign(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise Exception(f"Errore: variabile '{var_name}' non dichiarata")
        if self.symbol_table[var_name] != "STEADY":
            raise Exception(
                f"Errore: '{var_name}' è di tipo gamble. Usa <- Per favore!"
            )
        self.visit(node.children[1])

    def gamble_assign(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise Exception(f"Errore : variabile '{var_name}'non dichiarata")
        if self.symbol_table[var_name] != "GAMBLE":
            raise Exception(
                f"Errore : '{var_name}' è di tipo steady. Usa = Per favore!"
            )
        self.visit(node.children[1])
        self.gamble_history[var_name] += 1  # incrementa ad ogni <-

    def var(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise Exception(
                f"Errore : variabile '{var_name}' viene usata ma non dichiarata!!!"
            )

    def coin_decl(self, node):
        var_name = node.children[0].value
        if var_name in self.symbol_table:
            raise Exception(f"Errore: Ridichiarazione della variabile {var_name}")
        self.symbol_table[var_name] = "COIN"
        if len(node.children) > 1:
            self.visit(node.children[1])

    def if_stmt(self, node):
        self.visit(node.children[0])
        if len(node.children) > 1:
            self.visit(node.children[1])
        if len(node.children) > 2:
            self.visit(node.children[2])

    def ask_stmt(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise Exception(f"Errore: variabile '{var_name}' non dichiarata")
        tipo = self.symbol_table[var_name]
        if tipo == "COIN":
            raise Exception(f"Errore: ask non è consentito su variabili COIN")
        if tipo == "GAMBLE":
            if self.gamble_history.get(var_name, 0) < 1:
                raise Exception(
                    f"Errore: ask su '{var_name}' richiede almeno un '<-' precedente"
                )

    def risky_stmt(self, node):
        self.visit_children(node)

    def print_str_stmt(self, node):
        pass

    def cond_atom(self, node):
        self.visit(node.children[0])
        self.visit(node.children[2])

    def and_cond(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def or_cond(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def not_cond(self, node):
        self.visit(node.children[0])

    def loop_stmt(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def print_stmt(self, node):
        self.visit(node.children[0])

    def add(self, node):
        self.visit_children(node)

    def sub(self, node):
        self.visit_children(node)

    def mul(self, node):
        self.visit_children(node)

    def div(self, node):
        self.visit_children(node)

    def neg(self, node):
        self.visit(node.children[0])


def controllo_semantico(ast):
    analyzer = GAMBLANGSemanticAnalyzer()
    analyzer.visit(ast)
    return analyzer.symbol_table
