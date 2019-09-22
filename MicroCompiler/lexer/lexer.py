import MicroRegEx


def match_token(target_char, token_name_nfa_mapping, token_name_action_mapping):
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
                    return matched_str, token_object

    # lexer parse failed
    return "", None


def lex_analysis(input_string, user_defined_lexer_rule):
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
