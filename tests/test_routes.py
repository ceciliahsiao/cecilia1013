import unittest

from app import app


class BmiRouteTests(unittest.TestCase):
    """Test the Flask web route, form validation and rendered responses."""

    def setUp(self):
        self.client = app.test_client()

    def test_initial_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("了解自己的<br><em>健康狀況。</em>", page)
        self.assertIn("計算你的 BMI", page)
        self.assertIn('name="name"', page)

    def test_calculation_and_advice(self):
        response = self.client.post("/", data={"height": "170", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertIn("22.5", page)
        self.assertIn("健康體位", page)
        self.assertIn("維持均衡飲食", page)

    def test_name_is_shown_with_result(self):
        response = self.client.post("/", data={"name": "王小明", "height": "170", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertIn("王小明 的 BMI 計算結果", page)
        self.assertIn("22.5", page)

    def test_name_is_preserved_on_validation_error(self):
        response = self.client.post("/", data={"name": "陳小華", "height": "0", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertIn('value="陳小華"', page)
        self.assertNotIn("YOUR RESULT", page)

    def test_name_is_escaped(self):
        response = self.client.post("/", data={"name": "<script>alert(1)</script>", "height": "170", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_invalid_fields_do_not_produce_result(self):
        for height, weight in [("", "65"), ("0", "65"), ("abc", "65"), ("170", "-2"), ("inf", "65"), ("170", "nan"), ("1e-300", "65"), ("1e308", "65"), ("1", "1e308")]:
            with self.subTest(height=height, weight=weight):
                response = self.client.post("/", data={"height": height, "weight": weight})
                page = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('aria-invalid="true"', page)
                self.assertNotIn("YOUR RESULT", page)

    def test_input_is_escaped(self):
        response = self.client.post("/", data={"height": '<script>alert(1)</script>', "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertNotIn("<script>", page)
        self.assertIn("請輸入大於 0", page)

    def test_obese_bmi_is_highlighted(self):
        for weight, highlighted in [(107.6, False), (108, True), (120, True)]:
            with self.subTest(weight=weight):
                response = self.client.post("/", data={"height": "200", "weight": str(weight)})
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                self.assertEqual('class="result-number obese"' in page, highlighted)



if __name__ == "__main__":
    unittest.main()
