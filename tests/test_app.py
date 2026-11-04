import unittest

from app import bmi_guidance, parse_positive_number


class BmiUnitTests(unittest.TestCase):
    """Test pure BMI calculation helpers without HTTP or Flask test client."""

    def test_taiwan_adult_thresholds(self):
        for bmi, category in [
            (18.4, "體重過輕"),
            (18.5, "健康體位"),
            (23.9, "健康體位"),
            (24.0, "體重過重"),
            (26.9, "體重過重"),
            (27.0, "肥胖"),
        ]:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_guidance(bmi)["label"], category)

    def test_guidance_contains_tone_and_advice(self):
        for bmi in (17.0, 22.0, 25.0, 30.0):
            with self.subTest(bmi=bmi):
                result = bmi_guidance(bmi)
                self.assertIn(result["tone"], ("low", "healthy", "high"))
                self.assertTrue(result["advice"])

    def test_parse_positive_number(self):
        for value, expected in [("170", 170.0), ("65.5", 65.5), (" 2 ", 2.0)]:
            with self.subTest(value=value):
                self.assertEqual(parse_positive_number(value), expected)

    def test_parse_positive_number_rejects_invalid(self):
        for value in (None, "", "abc", "0", "-2", "inf", "-inf", "nan", "1e309"):
            with self.subTest(value=value):
                self.assertIsNone(parse_positive_number(value))


if __name__ == "__main__":
    unittest.main()
