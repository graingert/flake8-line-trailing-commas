
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
