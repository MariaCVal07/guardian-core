import json
import os
from datetime import datetime


class RunManager:

    def create_run(self, data):

        os.makedirs("runs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        run_id = f"RUN_{timestamp}"

        file_path = f"runs/{run_id}.json"

        run_data = {
            "run_id": run_id,
            "created_at": timestamp,
            "data": data
        }

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(
                run_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return run_id