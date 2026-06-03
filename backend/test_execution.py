from agents.execution_agent.agent import ExecutionAgent
from run_manager import RunManager

agent = ExecutionAgent()
run_manager = RunManager()

result = agent.execute_test()

run_id = run_manager.create_run(result)

print("\n=====================================")
print("GUARDIÁN QA EXECUTION REPORT")
print("=====================================\n")

print(f"RUN ID: {run_id}\n")

if result["success"]:

    print("STATUS:")
    print("PASSED\n")

    stdout = result["stdout"]

    if "chromium" in stdout.lower():
        print("BROWSER:")
        print("- Chromium")

    if "firefox" in stdout.lower():
        print("- Firefox")

    if "webkit" in stdout.lower():
        print("- Webkit")

    print("\nTEST RESULT:")

    lines = stdout.splitlines()

    for line in lines:
        if "passed" in line:
            print(line)

else:

    print("STATUS:")
    print("FAILED\n")

    print("ERROR:")
    print(result.get("error") or result.get("stderr"))

print("\nExecution saved successfully.")
print("\n=====================================")
