"""Sprint 1 acceptance: four UI smoke tests using page objects."""
import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.smoke, pytest.mark.ui]


def test_search_pliers_shows_only_matching_products(page):
    """Goal: keyword search filters products.
    Precondition: the product catalogue is available.
    Expected: results are nonempty and every product name contains pliers."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in name.lower() for name in names), names


def test_add_three_claw_hammers_updates_cart_badge(page):
    """Goal: add the requested quantity to the cart.
    Precondition: a fresh cart and Claw Hammer in the catalogue.
    Expected: adding three hammers shows a success toast and cart badge 3."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    product.add_to_cart(quantity=3)
    expect(product.toast).to_contain_text("Product added to shopping cart")
    expect(product.cart_quantity).to_have_text("3")


def test_login_with_nonexistent_email_shows_error(page):
    """Goal: invalid credentials are rejected.
    Precondition: use a nonexistent email rather than a shared account.
    Expected: Invalid email or password appears and the login URL is retained."""
    login = LoginPage(page).open().login("nobody-here@example.com", "Wrong-Password-123")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


def test_empty_contact_form_requires_subject_and_message(page):
    """Goal: the contact form validates required fields.
    Precondition: open the contact page without filling any fields.
    Expected: sending shows Subject is required and Message is required."""
    contact = ContactPage(page).open().submit()
    expect(contact.subject_error).to_contain_text("Subject is required")
    expect(contact.message_error).to_contain_text("Message is required")
