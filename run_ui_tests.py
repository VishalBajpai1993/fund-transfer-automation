import os
import sys
import webbrowser

# Ensure results directory exists
os.makedirs("allure-results", exist_ok=True)

# Get scenario name from command-line arguments (optional)
scenario_name = " ".join(sys.argv[1:])

# Behave command with Allure formatter
behave_command = 'python -m behave ui_tests -f allure_behave.formatter:AllureFormatter -o allure-results'
if scenario_name:
    behave_command = f'python -m behave ui_tests -n "{scenario_name}" -f allure_behave.formatter:AllureFormatter -o allure-results'

# Run Behave UI tests
print(f"\n Running UI tests with command: {behave_command}\n")
exit_code = os.system(behave_command)

# Serve Allure report (automatically launches in the browser)
print("\n Serving Allure Report...\n")
os.system("allure serve allure-results")

print("\n UI Test execution completed. Allure report opened in the browser.\n")

# Exit with the same status as Behave execution (useful for CI/CD pipelines)
sys.exit(exit_code)
