import unittest
import datetime

import outdate


ISO_FORMAT = '%Y-%m-%d'
US_FORMAT = '%m/%d/%Y'
UK_FORMAT = '%d/%m/%Y'
ORACLE_FORMAT = '%d-%b-%Y'
ALL_FORMATS = {ISO_FORMAT, US_FORMAT, UK_FORMAT, ORACLE_FORMAT}


class TestPatterns(unittest.TestCase):
    def test_iso_date(self):
        pat = outdate.to_re('%Y-%m-%d')
        self.assertIsNotNone(pat.fullmatch('2018-12-31'))
        self.assertIsNone(pat.fullmatch('2018-13-31'))
        self.assertIsNone(pat.fullmatch('2018-00-31'))


class TestDateFinder(unittest.TestCase):
    def test_single_iso(self):
        dt, match = outdate.find_date('2000-01-31', position=0, formats=[ISO_FORMAT])
        self.assertIsNotNone(match)
        self.assertEqual(dt, datetime.datetime(2000, 1, 31))


class TestReformat(unittest.TestCase):
    def test_reformat_iso_us(self):
        final_lines = outdate.reformat_date(['Dated 2000-01-31.'], 0, [ISO_FORMAT], US_FORMAT)
        self.assertEqual(final_lines, ['Dated 01/31/2000.'])

    def test_reformat_iso_uk(self):
        final_lines = outdate.reformat_date(['Dated 2000-01-31.'], 0, [ISO_FORMAT], UK_FORMAT)
        self.assertEqual(final_lines, ['Dated 31/01/2000.'])

    def test_reformat_iso_oracle(self):
        final_lines = outdate.reformat_date(['Dated 2000-01-31.'], 0, [ISO_FORMAT], ORACLE_FORMAT)
        self.assertEqual(final_lines, ['Dated 31-Jan-2000.'])

    def test_reformat_uk_us(self):
        final_lines = outdate.reformat_date(['Dated 31/01/2000.'], 0, [UK_FORMAT], US_FORMAT)
        self.assertEqual(final_lines, ['Dated 01/31/2000.'])


if __name__ == '__main__':
    unittest.main()
