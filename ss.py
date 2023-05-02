
def get_cleaned_regex(regex):
    terminals = ['a', 'b', 'c', 'd']
    starters = [')'] + terminals
    enders = ['('] + terminals
    new_regex = ""
    for ch in regex:
        if ch != " ":
            new_regex += ch

    i=0
    while i < len(new_regex)-1:
        ch = new_regex[i]
        next_symbol = new_regex[i+1]
        if ch in starters and next_symbol in enders:
            new_regex = new_regex[:i+1] + "~" + new_regex[i+1:]
        i += 1
    return new_regex


print(get_cleaned_regex("ab(cd)"))