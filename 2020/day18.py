def lex(line):
    def number():
        nonlocal line
        s = ""
        try:
            while line[0].isdigit():
                s += line[0]
                line = line[1:]
        except IndexError:
            pass
        return int(s)

    while line:
        c = line[0]
        if c == "(":
            yield ("opar",)
            line = line[1:]
        elif c == ")":
            yield ("cpar",)
            line = line[1:]
        elif c == "*":
            yield ("mul",)
            line = line[1:]
        elif c == "+":
            yield ("add",)
            line = line[1:]
        elif c.isdigit():
            yield ("num", number())
        else:
            line = line[1:]


def parse1(tokens):
    def peek():
        nonlocal tokens
        try:
            return tokens[0][0]
        except IndexError:
            return None

    def consume():
        nonlocal tokens
        tok = tokens[0]
        tokens = tokens[1:]
        return tok

    def atom():
        if peek() == "num":
            return ("atom", consume()[1])
        else:
            assert consume() == ("opar",)
            e = expr()
            assert consume() == ("cpar",)
            return e

    def expr():
        a = atom()
        while peek() in ("add","mul"):
            op, = consume()
            b = atom()
            if op == "add":
                a = ("add", a, b)
            else:
                a = ("mul", a, b)

        return a

    return expr()


def parse2(tokens):
    def peek():
        nonlocal tokens
        try:
            return tokens[0][0]
        except IndexError:
            return None

    def consume():
        nonlocal tokens
        tok = tokens[0]
        tokens = tokens[1:]
        return tok

    def atom():
        if peek() == "num":
            return ("atom", consume()[1])
        else:
            assert consume() == ("opar",)
            e = expr()
            assert consume() == ("cpar",)
            return e

    def mul():
        a = add()
        while peek() == "mul":
            consume()
            b = add()
            a = ("mul", a, b)
        return a

    def add():
        a = atom()
        while peek() == "add":
            consume()
            b = atom()
            a = ("add", a, b)
        return a

    def expr():
        return mul()

    return expr()


def evaluate(ast):
    if ast[0] == "add":
        return evaluate(ast[1]) + evaluate(ast[2])
    if ast[0] == "mul":
        return evaluate(ast[1]) * evaluate(ast[2])
    if ast[0] == "atom":
        return ast[1]


with open("day18.txt") as f:
    lines = [list(lex(line.strip())) for line in f]

print(sum(evaluate(parse1(tokens)) for tokens in lines))
print(sum(evaluate(parse2(tokens)) for tokens in lines))
