def to_num(number: int) -> str:
    alphabet = "0123456789ABC"
    result = str()
    while number > 0:
        result += alphabet[number % 13]
        number = number // 13
    return result[::-1]


def encrypt(_string: str) -> str:
    _encrypted = str()
    for index, char in enumerate(_string):
        enc_char = int(str(ord(char) + 1), 13) ** 2 + index * 37 + 3
        enc_char = f"{to_num(enc_char)}"

        separator = "FEDEFFDFDEDF"
        l = len(separator)

        if index + 1 == len(_string):
            _encrypted += f"{enc_char}"
        else:
            _encrypted += f"{enc_char}{separator[index % l]}"
    return _encrypted


def decrypt(_string: str) -> str:
    _decrypted = str()
    work = list()
    work2 = str()
    sep = {"F", "E", "D"}
    for char in _string:
        if char not in sep:
            work2 += char
        elif work2 != "":
            work.append(work2)
            work2 = str()

    for index, enc_char in enumerate(work):
        w_char = int(enc_char, 13) - index * 37 - 3
        w_char = int(w_char ** 0.5)
        w_char = chr(int(to_num(w_char)) - 1)
        _decrypted += w_char
    return _decrypted
