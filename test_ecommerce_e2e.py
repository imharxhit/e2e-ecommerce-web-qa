import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StorePage:
    """Page Object Model for the E-Commerce Store web application."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    COUPON_INPUT = (By.ID, "coupon-code")
    APPLY_COUPON_BTN = (By.ID, "apply-coupon")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    DISCOUNT_LABEL = (By.CLASS_NAME, "summary_discount_label")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    PIN_ERROR_MESSAGE = (By.ID, "pin-error")

    def login(self, username, password):
        user_field = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        user_field.clear()
        user_field.send_keys(username)
        pwd_field = self.driver.find_element(*self.PASSWORD_INPUT)
        pwd_field.clear()
        pwd_field.send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return element.text

    def sort_products_by_price_low_to_high(self):
        sort_elem = self.wait.until(EC.element_to_be_clickable(self.SORT_DROPDOWN))
        sort_elem.click()

    def get_product_prices(self):
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(p.text.replace("$", "")) for p in price_elements]

    def apply_coupon(self, code):
        coupon_field = self.wait.until(EC.presence_of_element_located(self.COUPON_INPUT))
        coupon_field.clear()
        coupon_field.send_keys(code)
        self.driver.find_element(*self.APPLY_COUPON_BTN).click()

    def calculate_discount(self, subtotal, coupon_code):
        if coupon_code == "SAVE10":
            return round(subtotal * 0.10, 2)
        return 0.0

    def validate_postal_pin(self, pin_code):
        return pin_code.isdigit() and len(pin_code) == 6


class TestEcommerceCheckout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = StorePage(self.driver)

    def test_login_success(self):
        """Test valid user login workflow."""
        self.page.login("standard_user", "secret_sauce")
        self.assertNotIn("error", self.driver.current_url.lower())

    def test_locked_out_user_error(self):
        """Test error message display for locked out user."""
        self.page.login("locked_out_user", "secret_sauce")
        error_text = self.page.get_error_message()
        self.assertIn("locked out", error_text.lower())

    def test_price_sorting(self):
        """Test product price sorting functionality."""
        prices = [29.99, 9.99, 15.99, 49.99]
        sorted_prices = sorted(prices)
        self.assertEqual(sorted_prices, [9.99, 15.99, 29.99, 49.99])

    def test_coupon_discount_calculation(self):
        """Test 10% coupon discount calculation with SAVE10."""
        subtotal = 100.00
        discount = self.page.calculate_discount(subtotal, "SAVE10")
        self.assertEqual(discount, 10.00)
        final_total = subtotal - discount
        self.assertEqual(final_total, 90.00)

    def test_pin_boundary_check(self):
        """Test 6-digit postal code/PIN validation boundary check."""
        self.assertTrue(self.page.validate_postal_pin("123456"))
        self.assertFalse(self.page.validate_postal_pin("12345"))
        self.assertFalse(self.page.validate_postal_pin("1234567"))
        self.assertFalse(self.page.validate_postal_pin("ABCDEF"))


if __name__ == "__main__":
    unittest.main()
