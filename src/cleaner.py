def clean(raws: list, filename: str) -> list:
    clears = list(raws)
    substitutions = init_substitutions(filename)

    texts = [clear[0] for clear in clears]

    for sub in substitutions:
        try:
            i = texts.index(sub)
            clears[i] = (substitutions[sub], clears[i][1])
        except ValueError:
            pass
    
    return clears


def init_substitutions(filename: str) -> dict:
    substitutions = {}

    with open(filename, 'r') as infile:
        for line in infile:
            (from_, to_) = line.strip("\t \n\"").split('">"')
            substitutions[from_] = to_
    
    return substitutions