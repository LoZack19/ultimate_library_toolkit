import json

def load(filename: str, verbose=False) -> list:
    raws = []

    with open(filename, 'r') as infile:
        messages = [message["text"] for message in json.load(infile)["messages"]]
    
    for message in messages:
        raw = tuple()

        try:
            raw = message_to_raw(message)
            raws.append(raw)
        except RuntimeError as err:
            if verbose:
                print(err)
                print("[MESSAGE]", message)
    
    return raws


def message_to_raw(message) -> tuple:
    (text, link) = ("", "")

    if type(message) == str:
        
        if message == '':
            raise RuntimeError("Empty message")
        
        return (message, None)
    
    elif type(message) == list:
        
        for n in message:
            if type(n) == str:
                text += n
            elif type(n) == dict:
                if "text" in n:
                    text += n["text"]
                if "href" in n:
                    link = n["href"]
            else:
                raise RuntimeError("Invalid type for text list entry")
    
        return (text, link)
    
    raise RuntimeError("Invalid type for message")