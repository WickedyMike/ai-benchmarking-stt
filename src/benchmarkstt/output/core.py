from benchmarkstt import output
from benchmarkstt.schema import Schema
from csv import writer
import sys


class ReStructuredText(output.Base):
    def result(self, title, result):
        print(title)
        print('=' * len(title))
        print()

        if type(result) is float:
            print("%.6f" % (result,))
        else:
            print(result)
        print()


class MarkDown(output.Base):
    def result(self, title, result):
        print('# %s' % (title,))
        print()

        if type(result) is float:
            print("%.6f" % (result,))
        else:
            print(result)
        print()


class Json(output.Base):
    def __init__(self):
        self._line = None

    def __enter__(self):
        if self._line is not None:
            raise ValueError("Already open")
        print('{')
        self._line = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._line = None
        print('\n}')

    def result(self, title, result):
        if self._line != 0:
            print(',')
        self._line += 1
        en = Schema.dumps
        print('\t%s: %s' % (en(title), en(result)), end='')


class Csv(output.Base):
    def __init__(self, dialect=None):
        self._writer = None
        self._dialect = dialect

    def __enter__(self):
        if self._writer is not None:
            raise ValueError('Already open')
        self._writer = writer(sys.stdout, self._dialect)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._writer = None

    def result(self, title, result):
        self._writer.writerow([title, result])