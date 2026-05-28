import subprocess


class ExecutionAgent:

    def execute_test(self):

        try:

            result = subprocess.run(

                "run_tests.bat",

                capture_output=True,
                text=True,
                shell=True,
                cwd="playwright",
                timeout=60
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "error": "Execution timeout exceeded"
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }