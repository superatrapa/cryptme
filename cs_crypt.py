import math
import random


class CryptException(Exception):
    pass


class CECharsetError(CryptException):
    pass


class CEInputError(CryptException):
    pass


class Nlist(list):
    """
    Improved list class, to get and set values outside of index using cycled values.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.cursor = None

    def __iter__(self):
        for i in range(len(self)):
            self.cursor = i
            yield self[i]
        self.cursor = None

    def __getitem__(self, item):
        return super().__getitem__(int(int(item) % len(self)))

    def __setitem__(self, item, value):
        super().__setitem__(int(item % len(self)), value)

    def copy(self):
        return self.__class__(super().copy())

    def pack_iter(self, step):
        """

        Args:
            step: length of yield touple

        Returns: yields tuples of values

        """
        assert len(self) % step == 0, f'Wrong length of the list step:{step} list:{len(self)} {self}'
        for x in range(len(self)):
            if x % step == 0:
                out = list()
                self.cursor = int(x / 2)
                for i in range(step):
                    out.append(self[x + i])
                yield tuple(out)


class Crypt:
    """Class to encode and decde text with optional key
       Crypt class is using table of characters. Each character have row and column.
       to Encode: Crypt.encode(text, otional key)
       to Decode: Crypt.decode(text, otional key)
       """

    charset = None  # character set avaiable to use in input text

    def __init__(self):
        self._key_string = ''
        self._crtpt_string = None
        self._raw_string = None
        self._total_length = None
        self._raw_column_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Labels for columns
        self._raw_row_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Labels for rows
        self._column_names = None
        self._row_names = None
        self.generate_charset()

    @property
    def column_names(self):
        if self._column_names is None:
            self._column_names = Nlist(self._raw_column_names)
            random.seed(self.key_string_seed)
            random.shuffle(self._column_names)
        return self._column_names

    @property
    def row_names(self):
        if self._row_names is None:
            self._row_names = Nlist(self._raw_row_names)
            random.seed(self.key_string_seed + 10)
            random.shuffle(self._row_names)
        return self._row_names

    @property
    def key_string_seed(self):
        seed = 0
        for letter in self.key_string:
            seed += ord(letter)
        return seed

    def validate_charset(self):
        """validate size of charset"""
        if len(self._raw_column_names) * len(self._raw_row_names) < len(self.charset):
            raise CECharsetError("Table too small to handle charset length")

    def generate_charset(self):
        if self.charset is not None:
            return
        self.charset = Nlist()
        for i in range(0, 126):
            self.charset.append(chr(i))
        self.validate_charset()

    @property
    def table_length(self):
        if self._total_length is None:
            self._total_length = math.ceil(len(self.charset) ** 0.5)
        return self._total_length

    def get_character_column(self, char, delta=0):
        i = self.charset.index(char)
        return self.column_names[i % self.table_length + delta]

    def get_character_row(self, char, delta=0):
        i = self.charset.index(char)
        return self.row_names[math.floor(i / self.table_length) + delta]

    @property
    def get_encoded(self):
        """

        Returns: Encoded Value

        """
        out = ''
        for i, letter in enumerate(self.raw_string):
            if letter not in self.charset:
                raise CEInputError(f'Not allowed character "{letter}" in input_string')
            out += str(self.get_character_row(letter, i))
            out += str(self.get_character_column(letter, i))
        self.crtpt_string = out
        return out

    @property
    def get_decoded(self):
        """

        Returns: Decoded Value

        """
        out = ''
        crypt_list = Nlist(self.crtpt_string)
        for row, col in crypt_list.pack_iter(2):
            icol = self.column_names.index(col) - crypt_list.cursor
            irow = self.row_names.index(row) - crypt_list.cursor
            out += self.charset[irow * self.table_length + icol]

        return out

    @property
    def key_string(self):
        return self._key_string

    @key_string.setter
    def key_string(self, value):
        self._key_string = value

    @property
    def crtpt_string(self):
        return self._crtpt_string

    @crtpt_string.setter
    def crtpt_string(self, value):
        self._crtpt_string = value

    @property
    def raw_string(self):
        return self._raw_string

    @raw_string.setter
    def raw_string(self, value):
        self._raw_string = value

    @classmethod
    def encode(cls, raw_string, key_string=''):
        """
        Main encode method
        Args:
            raw_string (str): input string
            key_string (str): key string - optional

        Returns: Encoded Value

        """
        obj = cls()
        obj.raw_string = raw_string
        obj.key_string = key_string
        return obj.get_encoded

    @classmethod
    def decode(cls, crypt_string, key_string=''):
        """
        Main decode method
        Args:
            crypt_string (str): input_string
            key_string (str): key string - optional

        Returns: Decoded Value

        """
        obj = cls()
        obj.crtpt_string = crypt_string
        obj.key_string = key_string
        return obj.get_decoded

    @classmethod
    def new(cls, raw_string='', crypt_string='', key_string=''):
        """
        Method for testing
        Args:
            raw_string (str): input_string
            crypt_string (str): input_string
            key_string (str): key string - optional

        Returns: Crypt Object

        """
        obj = cls()
        obj.raw_string = raw_string
        obj.crtpt_string = crypt_string
        obj.key_string = key_string
        return obj
