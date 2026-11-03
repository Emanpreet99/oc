# OpenCart system tests (Selenium + pytest)
    pip install -r requirements.txt
    pytest                                      # everything
    pytest tests/Test_product_discovery -v      # one folder
    pytest tests/Test_cart_wishlist -v 
    pytest tests/Test_checkout -v
Screenshots are saved to /screenshots after every test.

# OpenCart Store UI Automation

Automated browser tests for the OpenCart demo store using Python, pytest and Selenium WebDriver.

## Site under test

[OpenCart demo store](https://opencart.abstracta.us/)

## Tools and environment

- Operating system: Microsoft Windows NT [10.0.26100.0]
- Processor architecture: [AMD64]
- Python: [3.14.3]
- pytest: [9.1.1]
- Selenium: [4.51.0]
- Browser: [Chrome]
- Editor: Visual Studio Code

## Project structure

oc/
├── __pycache__/
├── .pytest_cache/
├── common/
├── screenshots/
├── tests/
│   ├── __pycache__/
│   ├── Test_cart_wishlist/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── test_cart.py
│   │   └── test_wishlist.py
│   ├── Test_checkout/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── test_cartcheckout.py
│   ├── Test_product_discovery/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── test_search.py
│   └── __init__.py
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt