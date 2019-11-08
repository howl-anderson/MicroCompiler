from typing import List, Tuple, Union

import MicroRegEx
from MicroCompiler.Lookahead import Terminal
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.SkeletonParser import WhiteSpaceToken
from MicroCompiler.lexer.exceptions import UserLevelLexerDefineError
from MicroCompiler.lexer.tokens import Token


def match_token(
    target_char, token_name_nfa_mapping, token_name_action_mapping
) -> Tuple[str, Token]:
    history = []
    for index in range(1, len(target_char) + 1):
        current_char_list = target_char[:index]

        is_accepted_mapping = {}
        still_alive_mapping = {}
        for token_object, nfa_object in token_name_nfa_mapping.items():
            nfa_object.reset()
            nfa_object.match(current_char_list)
            is_accepted_mapping[token_object] = nfa_object.is_accepted()
            still_alive_mapping[token_object] = bool(nfa_object.current_status)

        history.append(is_accepted_mapping)

        if not any(still_alive_mapping.values()) or (index == len(target_char)):
            # all regex expression engine stop, find last accepted status as result
            for reversed_history_index, monment in enumerate(history[::-1]):
                if any(monment.values()):
                    accepted_nfa_num = sum(bool(i) for i in monment.values())
                    if accepted_nfa_num > 1:
                        # TODO: two token pattern matched, maybe show warning
                        #       then select first rule
                        raise ValueError("at least two token partten match same string")

                    first_true_parser = list(filter(lambda x: x[1], monment.items()))
                    matched_token_type = first_true_parser[0][0]
                    matched_str = target_char[0 : index - reversed_history_index]

                    action = token_name_action_mapping[matched_token_type]

                    token_object = action(matched_str)

                    if not isinstance(token_object, Token):
                        raise UserLevelLexerDefineError(
                            "Expected return type of {!r} but get {!r}.".format(
                                Token, token_object.__class__
                            )
                        )

                    return matched_str, token_object

    # lexer parse failed
    # TODO
    return "", None


def lex_analysis(input_string, user_defined_lexer_rule) -> List[Tuple[str, Token]]:
    token_name_nfa_mapping = {}
    token_name_action_mapping = {}
    for token_object, token_regex, token_action in user_defined_lexer_rule:
        nfa_object = MicroRegEx.compile(token_regex)
        token_name_nfa_mapping[token_object] = nfa_object
        token_name_action_mapping[token_object] = token_action

    result = []

    current_target_char = input_string
    while True:
        if not current_target_char:
            # job done
            break

        matched_str, token_object = match_token(
            current_target_char, token_name_nfa_mapping, token_name_action_mapping
        )
        if matched_str:
            current_target_char = current_target_char[len(matched_str) :]
        else:
            raise ValueError("lexer parse failed")

        result.append((matched_str, token_object))

    return result


class Lexer(object):
    def __init__(self, user_defined_lexer_rule):
        self.program_string = None
        self.user_defined_lexer_rule = user_defined_lexer_rule
        self.raw_token_list = None
        self.token_list = None

        self.current_offset = 0

    def read_from_file(self, program_file):
        with open(program_file, "rt") as fd:
            self.program_string = fd.read()

    def read_from_string(self, program_string):
        self.program_string = program_string

    def reset(self):
        self.current_offset = 0

    def parse(self):
        self.raw_token_list = [
            i[1]
            for i in lex_analysis(self.program_string, self.user_defined_lexer_rule)
        ]
        # remote whitespace token
        self.token_list = list(
            filter(lambda x: not isinstance(x, WhiteSpaceToken), self.raw_token_list)
        )
        # append EOF token
        self.token_list.append(EOF())

    def get_next(self) -> Union[Token, EOF]:
        if self.current_offset >= len(self.token_list):
            raise ValueError()

        token = self.token_list[self.current_offset]
        self.current_offset += 1

        return token
