import io
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import csv_peek as c

DATA = "name,age,city\nAda,30,Paris\nBo,40,Paris\nCy,,Rome\n"


class Tests(unittest.TestCase):
    def setUp(self):
        self.header, self.rows = c.read_csv(io.StringIO(DATA))
        self.p = {i["name"]: i for i in c.profile(self.rows, self.header)}

    def test_counts(self):
        self.assertEqual(len(self.rows), 3)
        self.assertEqual(self.p["age"]["empty"], 1)

    def test_numeric(self):
        a = self.p["age"]
        self.assertEqual(a["type"], "number")
        self.assertEqual((a["min"], a["max"], a["mean"]), (30.0, 40.0, 35.0))

    def test_text_top(self):
        self.assertEqual(self.p["city"]["top"][0], ("Paris", 2))
        self.assertEqual(self.p["city"]["unique"], 2)

    def test_thousands_separator(self):
        self.assertEqual(c.to_number("1,200"), 1200.0)
        self.assertIsNone(c.to_number("abc"))

    def test_short_rows(self):
        h, r = c.read_csv(io.StringIO("a,b\n1\n2,3\n"))
        p = c.profile(r, h)
        self.assertEqual(p[1]["empty"], 1)

    def test_delimiter(self):
        h, r = c.read_csv(io.StringIO("a;b\n1;2\n"), ";")
        self.assertEqual(h, ["a", "b"])

    def test_empty(self):
        self.assertEqual(c.read_csv(io.StringIO("")), ([], []))

    def test_render(self):
        self.assertIn("min 30", c.render(self.p["age"]))
        self.assertIn("Paris (2)", c.render(self.p["city"]))


if __name__ == "__main__":
    unittest.main()
