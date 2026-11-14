"""Sprint 2 UI regression scenarios, alongside the four Sprint 1 smoke cases."""
import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


def test_search_without_matches_shows_empty_state(page):
    """Goal: explain an unsuccessful product search.
    Precondition: the site has loaded its catalogue.
    Expected: a no-results message and an empty product list."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_contain_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.parametrize("order", ["price,asc", "price,desc"])
def test_catalogue_sorts_prices_in_both_directions(page, order):
    """Goal: sorting rearranges the displayed catalogue.
    Precondition: the catalogue is available.
    Expected: prices follow the selected direction."""
    home = HomePage(page).open().sort_by(order)
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert len(prices) > 1, prices
    assert prices == sorted(prices, reverse=order == "price,desc"), prices


def test_product_details_show_the_selected_item(page):
    """Goal: opening a card displays its product details.
    Precondition: the catalogue contains Combination Pliers.
    Expected: matching name, a positive price, and default quantity one."""
    product = HomePage(page).open().open_product("Combination Pliers")
    expect(product.name).to_contain_text("Combination Pliers")
    expect(product.quantity).to_have_value("1")
    assert product.price() > 0


def test_cart_total_matches_the_selected_product_and_quantity(page):
    """Goal: cart displays the correct totals.
    Precondition: a fresh cart and Combination Pliers in the catalogue.
    Expected: the correct product and quantity, with total equal to unit price times two."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit_price = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_text(["Combination Pliers"])
    expect(cart.quantities).to_have_value("2")
    expect(cart.line_prices).to_have_count(1)
    expect(cart.total).not_to_be_empty()
    assert cart.line_totals() == pytest.approx([unit_price * 2])
    assert cart.total_value() == pytest.approx(unit_price * 2)


def test_empty_login_form_shows_both_required_field_errors(page):
    """Goal: validate the required login fields.
    Precondition: the login form is blank.
    Expected: email and password both show a required field error."""
    login = LoginPage(page).open().login("", "")
    expect(login.email_error).to_have_text("Email is required")
    expect(login.password_error).to_have_text("Password is required")


def test_saved_session_opens_the_users_account(logged_in_page):
    """Goal: a saved session grants access to the account.
    Precondition: the user fixture is authenticated.
    Expected: the account title and the registered user's name appear."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
    expect(account.nav_profile).to_be_visible()


def test_contact_form_rejects_invalid_email(page):
    """Goal: reject an invalid contact email address.
    Precondition: the contact form is available.
    Expected: the email field shows an invalid format error on submit."""
    contact = ContactPage(page).open()
    contact.email.fill("invalid-email")
    contact.submit()
    expect(contact.email_error).to_have_text("Email format is invalid")
