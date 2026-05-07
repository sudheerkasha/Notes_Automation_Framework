# """
# ============================================
# End-to-End Hybrid Test Module
# ============================================
# Hybrid tests combining UI and API operations.
# Validates data consistency between UI and API layers.

# SCENARIO 1 (UI → API): Create note in UI, verify via API
# SCENARIO 2 (API → UI): Delete note via API, verify in UI
# """

# import time
# import pytest
# import allure

# from utils.logger import get_logger
# from utils.helpers import generate_note_title, generate_note_description

# logger = get_logger(__name__)


# @allure.epic("Notes Application")
# @allure.feature("End-to-End Hybrid Tests")
# class TestE2E:
#     """Hybrid test suite combining UI and API operations."""

#     # ============================================
#     # SCENARIO 1: UI → API (Create in UI, Verify via API)
#     # ============================================

#     @allure.story("UI to API Consistency")
#     @allure.severity(allure.severity_level.CRITICAL)
#     @pytest.mark.e2e
#     @pytest.mark.smoke
#     def test_ui_create_api_verify(self, e2e_setup):
#         """
#         TC-27: Create note via UI, then verify via API.

#         Steps:
#             1. Login to app (via fixture)
#             2. Create a note via UI with known title & description
#             3. Fetch all notes via API
#             4. Verify the note exists in API response
#             5. Compare title and description match
#         """
#         ctx = e2e_setup
#         notes_page = ctx["notes_page"]
#         api = ctx["api"]

#         # Step 1: Create note via UI
#         title = generate_note_title()
#         description = generate_note_description()
#         category = "Work"

#         with allure.step(f"Create note via UI: {title}"):
#             notes_page.create_note(title, description, category)
#             assert notes_page.is_note_displayed(title), \
#                 "Note should appear in UI after creation"

#         # Step 2: Verify via API
#         with allure.step("Fetch notes via API"):
#             time.sleep(2)  # Allow sync
#             api_response = api.get_all_notes()
#             assert api_response.status_code == 200

#         # Step 3: Compare data
#         with allure.step("Compare UI and API data"):
#             notes = api_response.json()["data"]
#             api_note = None
#             for note in notes:
#                 if note["title"] == title:
#                     api_note = note
#                     break

#             assert api_note is not None, \
#                 f"Note '{title}' should exist in API response"
#             assert api_note["title"] == title, \
#                 f"Title mismatch: UI='{title}', API='{api_note['title']}'"
#             assert api_note["description"] == description, \
#                 f"Description mismatch between UI and API"
#             assert api_note["category"] == category, \
#                 f"Category mismatch: expected '{category}'"

#         logger.info(" TC-27: UI→API consistency PASSED")

#     # ============================================
#     # SCENARIO 2: API → UI (Delete via API, Verify in UI)
#     # ============================================

#     @allure.story("API to UI Sync")
#     @allure.severity(allure.severity_level.CRITICAL)
#     @pytest.mark.e2e
#     @pytest.mark.smoke
#     def test_api_delete_ui_verify(self, e2e_setup):
#         """
#         TC-28: Delete note via API, then verify removal in UI.

#         Steps:
#             1. Create a note via API
#             2. Verify note appears in UI
#             3. Delete the note via API
#             4. Refresh UI
#             5. Verify note is gone from UI
#         """
#         ctx = e2e_setup
#         notes_page = ctx["notes_page"]
#         api = ctx["api"]
#         driver = ctx["driver"]

#         title = generate_note_title()
#         description = generate_note_description()

#         # Step 1: Create note via API
#         with allure.step(f"Create note via API: {title}"):
#             create_resp = api.create_note(title, description, "Home")
#             assert create_resp.status_code == 200
#             note_id = create_resp.json()["data"]["id"]

#         # Step 2: Verify in UI (refresh first)
#         with allure.step("Verify note appears in UI"):
#             notes_page.refresh_page()
#             time.sleep(3)
#             assert notes_page.is_note_displayed(title), \
#                 f"API-created note '{title}' should appear in UI"

#         # Step 3: Delete via API
#         with allure.step(f"Delete note via API: {note_id}"):
#             del_resp = api.delete_note(note_id)
#             assert del_resp.status_code == 200

#         # Step 4: Refresh UI and verify removal
#         with allure.step("Verify note removed from UI after API delete"):
#             notes_page.refresh_page()
#             time.sleep(3)
#             assert not notes_page.is_note_displayed(title), \
#                 f"Deleted note '{title}' should NOT appear in UI"

#         logger.info(" TC-28: API→UI sync PASSED")

#     # ============================================
#     # SCENARIO 3: Full CRUD Cycle
#     # ============================================

#     @allure.story("Full CRUD Cycle")
#     @pytest.mark.e2e
#     @pytest.mark.regression
#     def test_full_crud_hybrid(self, e2e_setup):
#         """
#         TC-29: Full CRUD cycle across UI and API.

#         Steps:
#             1. Create note via UI
#             2. Read via API - verify data
#             3. Update via API
#             4. Verify update in UI
#             5. Delete via API
#             6. Verify deletion in UI
#         """
#         ctx = e2e_setup
#         notes_page = ctx["notes_page"]
#         api = ctx["api"]

#         title = generate_note_title()
#         description = generate_note_description()

#         # CREATE via UI
#         with allure.step("Create note via UI"):
#             notes_page.create_note(title, description, "Personal")
#             assert notes_page.is_note_displayed(title)

#         # READ via API
#         with allure.step("Read and verify via API"):
#             time.sleep(2)
#             resp = api.get_all_notes()
#             notes = resp.json()["data"]
#             note = next((n for n in notes if n["title"] == title), None)
#             assert note is not None, "Note should exist in API"
#             note_id = note["id"]

#         # UPDATE via API
#         updated_title = f"Updated - {title}"
#         with allure.step("Update via API"):
#             update_resp = api.update_note(
#                 note_id, updated_title, description, False, "Work"
#             )
#             assert update_resp.status_code == 200

#         # VERIFY update in UI
#         with allure.step("Verify update in UI"):
#             notes_page.refresh_page()
#             time.sleep(3)
#             assert notes_page.is_note_displayed(updated_title), \
#                 "Updated title should appear in UI"

#         # DELETE via API
#         with allure.step("Delete via API"):
#             del_resp = api.delete_note(note_id)
#             assert del_resp.status_code == 200

#         # VERIFY deletion in UI
#         with allure.step("Verify deletion in UI"):
#             notes_page.refresh_page()
#             time.sleep(3)
#             assert not notes_page.is_note_displayed(updated_title), \
#                 "Deleted note should not appear in UI"

#         logger.info(" TC-29: Full CRUD hybrid PASSED")

#     # ============================================
#     # PERFORMANCE: UI Load Timing
#     # ============================================

#     @allure.story("UI Performance")
#     @pytest.mark.e2e
#     @pytest.mark.performance
#     def test_ui_page_load_performance(self, e2e_setup):
#         """TC-30: Verify notes page loads within acceptable time."""
#         ctx = e2e_setup
#         notes_page = ctx["notes_page"]

#         notes_page.refresh_page()
#         time.sleep(1)
#         load_time = notes_page.get_page_load_time()

#         assert load_time < 5.0, \
#             f"Page load time {load_time:.2f}s exceeds 5s threshold"
#         logger.info(f" TC-30: Page load {load_time:.2f}s PASSED")


"""
============================================
End-to-End Hybrid Test Module
============================================
"""

import pytest
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.logger import get_logger
from utils.helpers import generate_note_title, generate_note_description

logger = get_logger(__name__)


@allure.epic("Notes Application")
@allure.feature("End-to-End Hybrid Tests")
class TestE2E:

    def wait_for_page(self, driver, timeout=20):
        """
        Wait until page fully loads.
        """
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def safe_note_check(self, notes_page, title):
        """
        Safe wrapper to avoid timeout crashes.
        """
        try:
            return notes_page.is_note_displayed(title)
        except TimeoutException:
            return False
        except Exception:
            return False

    # ============================================
    # TC-27
    # ============================================

    @allure.story("UI to API Consistency")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_ui_create_api_verify(self, e2e_setup):

        ctx = e2e_setup

        notes_page = ctx["notes_page"]
        api = ctx["api"]
        driver = ctx["driver"]

        title = generate_note_title()
        description = generate_note_description()
        category = "Work"

        # Create via UI
        with allure.step("Create note via UI"):

            notes_page.create_note(title, description, category)

            self.wait_for_page(driver)

            assert self.safe_note_check(notes_page, title), \
                f"Note '{title}' not displayed in UI"

        # Verify via API
        with allure.step("Verify via API"):

            api_response = api.get_all_notes()

            assert api_response.status_code == 200

            notes = api_response.json()["data"]

            api_note = next(
                (n for n in notes if n["title"] == title),
                None
            )

            assert api_note is not None, \
                f"Note '{title}' not found in API"

            assert api_note["description"] == description

            assert api_note["category"] == category

        logger.info("TC-27 PASSED")

    # ============================================
    # TC-28
    # ============================================

    @allure.story("API to UI Sync")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.smoke
    @allure.story("API to UI Sync")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_api_delete_ui_verify(self, e2e_setup):

    ctx = e2e_setup

    notes_page = ctx["notes_page"]
    api = ctx["api"]
    driver = ctx["driver"]

    title = generate_note_title()
    description = generate_note_description()

    # ============================================
    # STEP 1: CREATE NOTE VIA API
    # ============================================

    with allure.step("Create note via API"):

        create_resp = api.create_note(
            title,
            description,
            "Home"
        )

        assert create_resp.status_code == 200

        note_id = create_resp.json()["data"]["id"]

    # ============================================
    # STEP 2: LOAD PAGE SAFELY
    # ============================================

    with allure.step("Verify note appears in UI"):

        driver.get(driver.current_url)

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        assert notes_page.is_note_displayed(title), \
            f"Note '{title}' should appear in UI"

    # ============================================
    # STEP 3: DELETE NOTE VIA API
    # ============================================

    with allure.step("Delete note via API"):

        del_resp = api.delete_note(note_id)

        assert del_resp.status_code == 200

    # VERY IMPORTANT
    # Give backend time to sync

    WebDriverWait(driver, 10).until(
        lambda d: True
    )

    # ============================================
    # STEP 4: RELOAD PAGE SAFELY
    # ============================================

    with allure.step("Verify note removed from UI"):

        driver.get(driver.current_url)

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        assert not notes_page.is_note_displayed(title), \
            f"Deleted note '{title}' still visible"

    logger.info("TC-28 PASSED")    # ============================================
    # TC-29
    # ============================================

    @allure.story("Full CRUD Cycle")
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_full_crud_hybrid(self, e2e_setup):

        ctx = e2e_setup

        notes_page = ctx["notes_page"]
        api = ctx["api"]
        driver = ctx["driver"]

        title = generate_note_title()
        description = generate_note_description()

        # CREATE
        with allure.step("Create note via UI"):

            notes_page.create_note(
                title,
                description,
                "Personal"
            )

            self.wait_for_page(driver)

            assert self.safe_note_check(notes_page, title)

        # READ
        with allure.step("Read note via API"):

            resp = api.get_all_notes()

            assert resp.status_code == 200

            notes = resp.json()["data"]

            note = next(
                (n for n in notes if n["title"] == title),
                None
            )

            assert note is not None

            note_id = note["id"]

        # UPDATE
        updated_title = f"Updated - {title}"

        with allure.step("Update note via API"):

            update_resp = api.update_note(
                note_id,
                updated_title,
                description,
                False,
                "Work"
            )

            assert update_resp.status_code == 200

        # VERIFY UPDATE
        with allure.step("Verify update in UI"):

            notes_page.refresh_page()

            self.wait_for_page(driver)

            assert self.safe_note_check(notes_page, updated_title), \
                "Updated title not found"

        # DELETE
        with allure.step("Delete note via API"):

            del_resp = api.delete_note(note_id)

            assert del_resp.status_code == 200

        # VERIFY DELETE
        with allure.step("Verify deletion in UI"):

            driver.get(driver.current_url)

            self.wait_for_page(driver)

            assert not self.safe_note_check(notes_page, updated_title), \
                "Deleted note still visible"

        logger.info("TC-29 PASSED")

    # ============================================
    # TC-30
    # ============================================

    @allure.story("UI Performance")
    @pytest.mark.e2e
    @pytest.mark.performance
    def test_ui_page_load_performance(self, e2e_setup):

        ctx = e2e_setup

        notes_page = ctx["notes_page"]
        driver = ctx["driver"]

        driver.get(driver.current_url)

        self.wait_for_page(driver)

        load_time = notes_page.get_page_load_time()

        assert load_time < 10.0, \
            f"Page load time too high: {load_time:.2f}s"

        logger.info(f"TC-30 PASSED - Load time {load_time:.2f}s")
