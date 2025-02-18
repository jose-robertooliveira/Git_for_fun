from string import ascii_lowercase


VOWELS = "aeiou"

def LetterChanges(str) -> None:
    new_chars = []

    for char in str:
        if char == 'z':
            new_chars.append('a')
            continue
        try:
            index_char = ascii_lowercase.index(char)
        except ValueError:
            new_chars.append(char)
        else:
            new_index = index_char + 1
            new_char = ascii_lowercase[new_index]
            new_chars.append(new_char)
    
    def capitalize_if_needed(x_char):
        if x_char in VOWELS:
            return x_char.upper()
        return x_char
    
    new_chars = [
        capitalize_if_needed(char)
        for char in new_chars
    ]
    return ''.join(new_chars)

obj = LetterChanges("abcdefghijklmnopqrstuvwxyz")
print(obj)
