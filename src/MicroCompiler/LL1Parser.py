class LL1Parser:
    def __init__(self, translation_table, production, lexer_list):
        self.translation_table = translation_table
        self.lexer_list = lexer_list

    def match(self):
        for lexer in self.lexer_list:
            pass