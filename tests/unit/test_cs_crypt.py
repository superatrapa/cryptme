import pytest
from cs_crypt import *


class TestCrypt:

    def test_allowed_characters(self):
        Crypt.encode('ABC', 'fsfs')

    def test_not_allowed_characters(self):
        with pytest.raises(CEInputError):
            Crypt.encode('AAav¢')

    def test_table(self):
        obj = Crypt.new(raw_string='ABC', key_string='dda')
        obj._raw_column_names = '12'
        obj._raw_row_names = 'AB'
        obj._column_names = None
        obj._row_names = None
        obj.charset = None
        with pytest.raises(CECharsetError):
            obj.generate_charset()

    def test_encode_decode(self):
        txt = 'ABCD'
        assert Crypt.decode(Crypt.encode(txt)) == txt

    def test_encode_decode_with_key(self):
        txt = 'ABCD'
        key = 'vvkk'
        assert Crypt.decode(Crypt.encode(txt, key), key) == txt
        assert Crypt.decode(Crypt.encode(txt, key)) != txt
        assert Crypt.decode(Crypt.encode(txt), key) != txt
        assert Crypt.decode(Crypt.encode(txt, 'diff'), key) != txt
        assert Crypt.decode(Crypt.encode(txt, key), 'diff') != txt


class TestNlist:

    def test_shift(self):
        obj = Nlist('ABCD')
        assert obj[0] == obj[4]
        assert obj[1] == obj[5]
        assert obj[2] == obj[6]
        assert obj[-1] == obj[3]
        obj[6] = 'X'
        assert obj[2] == 'X'

    def test_iter(self):
        obj = Nlist('ABCD')
        for x in obj:
            assert x == obj[obj.cursor]
