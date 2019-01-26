import regex

from kismet.parser import KismetParser
from kismet.personality.core import analyze

# Create parser object.
parser = KismetParser()


def process(string: str):
    parsed = parser.parse(string)
    emoted = analyze(string)
    if parsed and emoted:
        return parsed + "\n" + emoted
    elif parsed:
        return parsed
    elif emoted:
        return emoted
    else:
        return ""


def code_blocks(string: str, syntax_type: str = "kismet"):
    blocks = []
    fence = None
    ignore = False
    for line in string.splitlines(keepends=True):
        while line:
            if fence:
                # Look for fence end
                match = regex.search(fence, line)
                if match:
                    if not ignore:
                        blocks[-1] += line[: match.start()]
                    fence = None
                    line = line[match.end() :]
                elif not ignore:
                    blocks[-1] += line
                    line = None
                else:
                    line = None
            else:
                # Look for fence start
                match = regex.search(r"^`{3,}", line)
                if match:
                    fence = "^" + match.group()
                    syntax = line[match.end() :]
                    if syntax != "\n" and syntax != syntax_type + "\n":
                        ignore = True
                    else:
                        blocks.append("")
                    line = None
                else:
                    match = regex.search(r"`+", line)
                    if match:
                        fence = match.group()
                        line = line[match.end() :]
                        blocks.append("")
                    else:
                        line = None
    if fence:
        del blocks[-1]
    return blocks
