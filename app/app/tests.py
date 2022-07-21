from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    """Test the calc module"""
    def test_add_numbers(self):
        """test adding the numbers together"""
        res=calc.add(5,6)

        self.assertEqual(res,11)

    def test_subtract_numbers(self):
        """test subtracting the numbers together"""
        res=calc.subtract(10,3)

        self.assertEqual(res,7)


