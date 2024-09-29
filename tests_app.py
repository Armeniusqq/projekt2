import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """
    Spouští prohlížeč před testy a zavírá ho po testech.

    Používáme Playwright pro spuštění Chromium prohlížeče.
    Testy budou běžet s viditelným oknem prohlížeče (headless=False).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


def test_homepage_title(browser):
    """
    Kontroluje, zda domovská stránka Engeto.cz má správný název (title).

    Postup:
    1. Otevře stránku https://engeto.cz/.
    2. Ověří, že název stránky obsahuje slova 'ENGETO' a 'kurzy'.

    Ověření probíhá tak, že hledáme obě slova v názvu stránky, přičemž 'kurzy' může být v jakémkoliv formátu (malými/velkými písmeny).
    """
    page = browser.new_page()
    page.goto("https://engeto.cz/")
    assert "ENGETO" in page.title() and "kurzy" in page.title().lower()
    page.close()


def test_contact_page_navigation(browser):
    """
    Testuje, zda lze přejít na kontaktní stránku na Engeto.cz.

    Postup:
    1. Otevře stránku https://engeto.cz/.
    2. Pokud se zobrazí cookie lišta, klikne na tlačítko 'Chápu a přijímám!' pro přijetí cookies.
    3. Klikne na odkaz 'Kontakt a fakturační údaje'.
    4. Ověří, že jsme na stránce s kontaktními údaji.

    Tento test kontroluje, zda se po kliknutí na správný odkaz zobrazí kontaktní informace.
    """
    page = browser.new_page()
    page.goto("https://engeto.cz/")

    # Přijímáme cookies, pokud je zobrazen banner
    page.wait_for_selector("#cookiescript_accept")
    page.locator("#cookiescript_accept").click()

    # Kliknutí na odkaz 'Kontakt a fakturační údaje'
    page.locator("text=Kontakt a fakturační údaje").wait_for()
    page.locator("text=Kontakt a fakturační údaje").click()

    # Ověření, že jsme na správné URL
    assert page.url == "https://engeto.cz/kontakt/"
    page.close()


def test_dates_section(browser):
    """
    Testuje, zda lze přejít na stránku s termíny kurzů na Engeto.cz.

    Postup:
    1. Otevře stránku https://engeto.cz/.
    2. Přijme cookies kliknutím na tlačítko 'Chápu a přijímám!'.
    3. Klikne na odkaz 'Termíny'.
    4. Ověří, že aktuální URL je stránka s termíny kurzů.

    Tento test se zaměřuje na navigaci na stránku s termíny kurzů pomocí odkazu s určitou třídou (CSS class).
    """
    page = browser.new_page()
    page.goto("https://engeto.cz/")

    # Přijímáme cookies, pokud je zobrazen banner
    page.wait_for_selector("#cookiescript_accept")
    page.locator("#cookiescript_accept").click()

    # Kliknutí na odkaz 'Termíny' pomocí tříd pro přesné určení odkazu
    page.locator("a.block-button.type-premium.size-l.orange-link.hide-mobile").click()

    # Ověření, že jsme na stránce s termíny kurzů
    assert page.url == "https://engeto.cz/terminy/"
    page.close()
