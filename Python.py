# ========================= IMPORTY =========================
import pytest
from playwright.sync_api import sync_playwright, expect



#========================= NASTAVENÍ TESTŮ PRO CHROME, FIREFOX A SAFARI =========================
@pytest.fixture(params=["chromium", "firefox", "webkit"])
#@pytest.fixture(params=["firefox"])
def prohlizec(request):
    p = sync_playwright().start()
    #========== Testování každého z prohlížečů =============
    browser = getattr(p, request.param).launch()
    yield browser
    browser.close()
    p.stop()



#========================= POMOCNÉ FUNKCE =========================
#cookies accept funkce
def cookies_accept(page):
    #odkliknutí cookies popup pokud je viditelný
    page.wait_for_timeout(2000)  # počkej 2 sekundy
    # najdi tlačítko "Povolit vše" podle ID
    try:
        cookies_btn = page.locator("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        # ověř, že je viditelné, a klikni na něj
        if cookies_btn.is_visible():
            cookies_btn.click()
            page.wait_for_timeout(1500)
    except:
        print("Cookies banner nebyl nalezen.")

# odhlasení funkce
def odhlaseni(page):
    # odhlášení
    page.click(".mpHeader__iconLink--login") # =======================> kliknuti na ikonu uzivatele pro zobrazení menu
    page.wait_for_timeout(2000)  # počkej 2 sekundy
    odhlaseni_btn = page.locator(".popup__logged__menuItem >> text=Odhlášení") 
    odhlaseni_btn.wait_for(state="visible") 
    odhlaseni_btn.scroll_into_view_if_needed()
    #page.screenshot(path="pred_odhlasenim.png")
    odhlaseni_btn.click(force=True) # ======> kliknuti na odhlášení v menu
    # Ověření odhlášení
    expect(page.locator(".mpHeader__iconLink--login .desc")).to_have_text("Přihlásit")  # ==> Ověření, že je uživatel odhlášen



#=====================================> TESTY <=====================================
#==============================> https://www.mp.cz/ <=====================================

# =========== TEST 1: PŘIHLÁŠENÍ SE ŠPATNÝM HESLEM ===============                   ======> KROKY TESTU <======
def test_spatne_heslo(prohlizec):
    page = prohlizec.new_page()     # ===========================================> 1) Otevření nové stránky
    page.set_default_timeout(10000)
    page.goto("https://www.mp.cz/")     # =======================================> 2) Navigace na URL
    # odkliknutí cookies popup pokud je viditelný
    cookies_accept(page)
    page.click(".mpHeader__iconLink--login")    # ===============================> 3) Kliknutí na tlačítko přihlášení
    #počkat až vyskočí okno s přihlášením
    page.wait_for_selector('.popup-auth input[name="username"]', state="visible")
    page.wait_for_selector('.popup-auth input[name="password"]', state="visible")
    page.fill('input[name="username"]', "test_user")    # =======================> 4) Vyplnění uživatelského jména
    page.fill('input[name="password"]', "test_password")     # ==================> 5) Vyplnění špatného hesla
    page.click('.popup-auth button:has-text("Přihlásit")')   # ==================> 6) Kliknutí na tlačítko přihlášení
    #uložit lokátor chybové hlášky
    chybova_hlaska = page.locator('.popup-auth .v-alert.v-alert--variant-flat')
    chybova_hlaska.wait_for(state="visible", timeout=10000)
    expect(chybova_hlaska).to_have_text("Pomocí zadaných údajů se nelze přihlásit.") # 7) Ověření, že se zobrazila chybová hláška Pomocí zadaných údajů se nelze přihlásit.


# =========== TEST 2: PŘIHLÁŠENÍ S PRAZDNÝM HESLEM ===============                   ======> KROKY TESTU <======
def test_prazdne_heslo(prohlizec):
    page = prohlizec.new_page()     # ===========================================> 1) Otevření nové stránky
    page.set_default_timeout(10000)
    page.goto("https://www.mp.cz/")     # =======================================> 2) Navigace na URL
    # odkliknutí cookies popup pokud je viditelný
    cookies_accept(page)
    page.click(".mpHeader__iconLink--login")    # ===============================> 3) Kliknutí na tlačítko přihlášení
    #počkat až vyskočí okno s přihlášením
    page.wait_for_selector('.popup-auth input[name="username"]', state="visible")
    page.wait_for_selector('.popup-auth input[name="password"]', state="visible")
    page.fill('input[name="username"]', "test_user")    # =======================> 4) Vyplnění uživatelského jména
    page.fill('input[name="password"]', "")     # ===============================> 5) Vyplnění prázdného hesla
    page.click('.popup-auth button:has-text("Přihlásit")')   # ==================> 6) Kliknutí na tlačítko přihlášení
    #uložit lokátor chybové hlášky
    chybova_hlaska = page.locator('.popup-auth .v-input:has(input[name="password"]) .v-input__details .v-messages__message')
    chybova_hlaska.wait_for(state="visible", timeout=10000)
    expect(chybova_hlaska).to_have_text("Povinné")      # ========================> 7) Ověření, že se zobrazila chybová hláška, Povinné.


# =========== TEST 3: ÚSPĚŠNÉ PŘIHLÁŠENÍ ===============                   ======> KROKY TESTU <======
def test_uspesne_prihlaseni(prohlizec):
    page = prohlizec.new_page()     # ===========================================> 1) Otevření nové stránky
    page.set_default_timeout(10000)
    page.goto("https://www.mp.cz/")     # =======================================> 2) Navigace na URL
    # odkliknutí cookies popup pokud je viditelný
    cookies_accept(page)
    # zjišteni jestli není přihlášen uživatel a případné odhlášení
    login_text = page.locator(".mpHeader__iconLink--login .desc").inner_text()
    if login_text != "Přihlásit":
        odhlaseni(page)
    page.click(".mpHeader__iconLink--login")  # ===============================> 3) Kliknutí na tlačítko přihlášení
    #počkat až vyskočí okno s přihlášením
    page.wait_for_selector('.popup-auth input[name="username"]', state="visible")
    page.wait_for_selector('.popup-auth input[name="password"]', state="visible")
    page.fill('input[name="username"]', "lenule14@gmail.com")    # =======================> 4) Vyplnění uživatelského jména
    page.fill('input[name="password"]', "Engeto+123")     # ==================> 5) Vyplnění správného hesla
    page.click('.popup-auth button:has-text("Přihlásit")')   # ==================> 6) Kliknutí na tlačítko přihlášení
    #ověření úspěšného přihlášení
    page.wait_for_selector(".mpHeader__iconLink--login .desc", state="visible")
    email_element = page.locator(".mpHeader__iconLink--login .desc")
    expect(email_element).to_have_text("lenule14@gmail.com") # ===>  7) Ověření, že je zobrazen email přihlášeného uživatele


# =========== TEST 4: ÚSPĚŠNÉ PŘIHLÁŠENÍ A ODHLÁŠENÍ ===============                   ======> KROKY TESTU <======
def test_uspesne_prihlaseni_a_odhlaseni(prohlizec):
    page = prohlizec.new_page()  # ===========================================> 1) Otevření nové stránky
    page.set_default_timeout(10000)
    page.goto("https://www.mp.cz/")  # =======================================> 2) Navigace na URL
    # odkliknutí cookies popup pokud je viditelný
    cookies_accept(page)
    # zjišteni jestli není přihlášen uživatel a případné odhlášení
    login_text = page.locator(".mpHeader__iconLink--login .desc").inner_text()
    if login_text != "Přihlásit":
        odhlaseni(page)
    page.click(".mpHeader__iconLink--login")  # ===============================> 3) Kliknutí na tlačítko přihlášení
    # počkat až vyskočí okno s přihlášením
    page.wait_for_selector('.popup-auth input[name="username"]', state="visible")
    page.wait_for_selector('.popup-auth input[name="password"]', state="visible")
    page.fill('input[name="username"]',"lenule14@gmail.com")  # =======================> 4) Vyplnění uživatelského jména
    page.fill('input[name="password"]', "Engeto+123")  # ==================> 5) Vyplnění správného hesla
    page.click('.popup-auth button:has-text("Přihlásit")')  # ==================> 6) Kliknutí na tlačítko přihlášení
    # ověření úspěšného přihlášení
    page.wait_for_selector(".mpHeader__iconLink--login .desc", state="visible")
    email_element = page.locator(".mpHeader__iconLink--login .desc")
    expect(email_element).to_have_text("lenule14@gmail.com")  # ====> 7)Ověření, že je zobrazen email přihlášeného uživatele
    #odhlášení
    odhlaseni(page) # =======================> 8) provedení odhlášení pomocí pomocné funkce


if __name__ == "__main__":
    pytest.main([__file__])
