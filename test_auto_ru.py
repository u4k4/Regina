import re
from playwright.sync_api import sync_playwright, expect
import time


def test_auto_ru_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # ==========================================================
            # ВАРИАНТ 1: Поиск через URL-параметры
            # ==========================================================
            search_query = "BMW X5"
            page.goto(
                f"https://auto.ru/moskva/cars/all/?text={search_query.replace(' ', '%20')}",
                wait_until="domcontentloaded",
                timeout=30000
            )

            expect(page).to_have_url(re.compile(r".*text=BMW.*"), timeout=10000)
            expect(page.get_by_role("button", name="Марка")).to_be_visible(timeout=10000)
            print("Вариант 1 (Поиск через URL) успешно пройден!")

            # ==========================================================
            # ВАРИАНТ 2: UI-тест через клик по стабильной навигации
            # ==========================================================
            page.goto("https://auto.ru/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)  # Небольшая пауза для стабилизации рендера

            all_offers_link = page.get_by_role("link", name="Все предложения")
            if not all_offers_link.is_visible():
                all_offers_link = page.locator("a").filter(has_text=re.compile("Все предложения", re.IGNORECASE)).first

            expect(all_offers_link).to_be_visible(timeout=10000)
            all_offers_link.click(force=True)

            expect(page).to_have_url(re.compile(r".*/moskva/cars/all/.*"), timeout=10000)
            expect(page.get_by_role("button", name="Марка")).to_be_visible(timeout=10000)
            print("Вариант 2 (UI-клик по навигации) успешно пройден!")

        except Exception as e:
            print(f"Тест завершился с ошибкой: {e}")
            raise
        finally:
            print("Браузер останется открытым еще на 10 секунд для визуальной проверки...")
            time.sleep(10)
            browser.close()
            print("Браузер закрыт, тест завершен.")


if __name__ == "__main__":
    test_auto_ru_search()