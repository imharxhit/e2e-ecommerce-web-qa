# e2e-ecommerce-web-qa

Selenium WebDriver + Python E2E automation tests for an e-commerce store using Page Object Model.

## Overview

This repository contains an end-to-end automated test suite built with Python's unittest framework and Selenium WebDriver, following the Page Object Model (POM) design pattern.

The test suite covers key e-commerce user workflows:
- User authentication and login functionality
- Error handling for locked/invalid user accounts
- Product catalog price sorting
- Cart total calculation and discount logic with coupon code SAVE10
- Checkout validation including 6-digit postal PIN boundary checks

## Setup and Execution

1. Install dependencies:
pip install -r requirements.txt

2. Run the test suite:
python -m unittest test_ecommerce_e2e.py -v
