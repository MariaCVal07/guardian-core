#podrá crear automáticamente archivos Playwright.

import os 

class FileManager:

    def save_test_file(self, filename, content):

        os.makedirs(
            "playwright/tests/generated",
            exist_ok=True
        )

        file_path = f"playwright/tests/generated/{filename}"

        with open(file_path, "w", encoding="utf-8") as file:

            file.write(content)

        return file_path