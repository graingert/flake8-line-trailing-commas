import tokenize
import collections
import token as mod_token

try:
    import pycodestyle
except ImportError:
    import pep8 as pycodestyle

try:
    from flake8.engine import pep8 as stdin_utils
except ImportError:
    from flake8 import utils as stdin_utils

import pkg_resources

try:
    dist = pkg_resources.get_distribution('flake8-commas')
    __version__ = dist.version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'

# A parenthesized expression list yields whatever that expression list
# yields: if the list contains at least one comma, it yields a tuple;
# otherwise, it yields the single expression that makes up the expression
# list.

PYTHON_2_KWDS = {
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
    'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise',
    'return', 'try', 'while', 'with', 'yield',
}

PYTHON_3_KWDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
    'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
    'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
    'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
}

KWD_LIKE_FUNCTION = {'import', 'assert'}

ALL_KWDS = (PYTHON_2_KWDS & PYTHON_3_KWDS) - KWD_LIKE_FUNCTION
NOT_PYTHON_2_KWDS = (PYTHON_3_KWDS - PYTHON_2_KWDS) - KWD_LIKE_FUNCTION
NOT_PYTHON_3_KWDS = (PYTHON_2_KWDS - PYTHON_3_KWDS) - KWD_LIKE_FUNCTION


class TupleOrParenthForm(object):
    def __bool__(self):
        return False

    __nonzero__ = __bool__


TUPLE_OR_PARENTH_FORM = TupleOrParenthForm()


class SimpleToken(object):
    def __init__(self, token, type):
        self.token = token
        self.type = type


Context = collections.namedtuple('Context', ['comma', 'unpack'])


NEW_LINE = 'new-line'
COMMA = ','
OPENING_BRACKET = '('
SOME_CLOSING = 'some-closing'
SOME_OPENING = 'some-opening'
OPENING = {SOME_OPENING,  OPENING_BRACKET}
CLOSING = {SOME_CLOSING}
BACK_TICK = '`'
CLOSE_ATOM = CLOSING | {BACK_TICK}
FOR = 'for'
NAMED = 'named'
PY2_ONLY_ERROR = 'py2-only-error'
PY3K_ONLY_ERROR = 'py3-only-error'
DEF = 'def'
FUNCTION_DEF = 'function-def'
FUNCTION = {NAMED, PY2_ONLY_ERROR, PY3K_ONLY_ERROR, FUNCTION_DEF}
UNPACK = '* or **'
NONE = SimpleToken(token=None, type=None)


def simple_tokens(tokens):
    tokens = (t for t in tokens)
    for token in tokens:
        yield token


ERRORS = {
    True: ('C812', 'missing trailing comma'),
    FUNCTION_DEF: ('C812', 'missing trailing comma'),
    PY3K_ONLY_ERROR: ('C813', 'missing trailing comma in Python 3'),
    PY2_ONLY_ERROR: ('C814', 'missing trailing comma in Python 2'),
    'py35': ('C815', 'missing trailing comma in Python 3.5+'),
    'py36': ('C816', 'missing trailing comma in Python 3.6+'),
}


def process_parentheses(token, prev_1, prev_2):
    previous_token = prev_1

    if token.type == OPENING_BRACKET:
        is_function = (
            previous_token and
            (
                (previous_token.type in CLOSE_ATOM) or
                (
                    previous_token.type in FUNCTION
                )
            )
        )
        if is_function:
            if prev_2.type == DEF:
                return [Context(FUNCTION_DEF, False)]
            tk_string = previous_token.type
            if tk_string == PY2_ONLY_ERROR:
                return [Context(PY2_ONLY_ERROR, False)]
            if tk_string == PY3K_ONLY_ERROR:
                return [Context(PY3K_ONLY_ERROR, False)]
        else:
            return [Context(TUPLE_OR_PARENTH_FORM, False)]

    return [Context(True, False)]


def get_tokens(filename):
    if filename == 'stdin':
        file_contents = stdin_utils.stdin_get_value().splitlines(True)
    else:
        file_contents = pycodestyle.readlines(filename)
    file_contents_iter = iter(file_contents)

    def file_contents_next():
        return next(file_contents_iter)

    for t in tokenize.generate_tokens(file_contents_next):
        yield t


def no_qa_comment(token):
    return token.type == tokenize.COMMENT and token.string.endswith('noqa')


def get_noqa_lines(tokens):
    return [token.start_row for token in tokens if no_qa_comment(token)]


def get_comma_errors(tokens):

    yield {
        'message': 'HOLLA',
        'line': 1,
        'col': 50,
    }


class CommaChecker(object):
    name = __name__
    version = __version__

    def __init__(self, tree, filename='(none)', file_tokens=None):
        fn = 'stdin' if filename in ('stdin', '-', None) else filename
        self.filename = fn
        self.tokens = file_tokens

    def run(self):
        filename = self.filename

        if filename == 'stdin':
            lines = stdin_utils.stdin_get_value().splitlines(True)
        else:
            lines = pycodestyle.readlines(filename)

        for idx, line in enumerate(lines):
            line = line.strip()
            if line and line in ['},', '),', '],']:
                yield (
                    idx,
                    len(line),
                    "My Word!",
                    "C811",
                )
