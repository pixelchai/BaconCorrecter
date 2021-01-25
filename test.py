import unittest
from main import correct

class TestCorrection(unittest.TestCase):
    def assertNeedsCorrecting(self, msg):
        self.assertNotEqual(msg, correct(msg))

    def assertNotNeedsCorrecting(self, msg):
        self.assertEqual(msg, correct(msg))

    def assertCorrection(self, msg, correction):
        self.assertEqual(correct(msg), correction)

    def test_normal(self):
        self.assertNotNeedsCorrecting("hello there ! ")
        self.assertNotNeedsCorrecting("hello  there")
        self.assertNotNeedsCorrecting("hello     there")

        self.assertNotNeedsCorrecting("Hi There This Is A Test")
        self.assertNotNeedsCorrecting("ALL CAPS IS\nALL OKAY")
        self.assertNotNeedsCorrecting("I like doing OOP, man")  # ALL CAPS WORDS mixed with all lowercase words is ok

        self.assertNotNeedsCorrecting("I like doing OOP\nman I like OOP")  # split on \n too
        self.assertNotNeedsCorrecting("I like doing OOP,man I like OOP")   # and split on , too
        self.assertNotNeedsCorrecting("I like doing OOP!man I like OOP")   # etc..

        self.assertNotNeedsCorrecting("Send those URLs for the LOLz")  # slightly strange but I'll allow it
        self.assertNotNeedsCorrecting("https://www.google.com/")


    def test_correction(self):
        self.assertCorrection("HeLlO thEre", "Hello there")
        self.assertCorrection("HeLlO  thEre ! ", "Hello  there ! ")

        self.assertCorrection("Don't correct URLs like git.io/JtZ5T", "Don't correct URLs like git.io/JtZ5T")

if __name__ == "__main__":
    unittest.main(verbosity=2)