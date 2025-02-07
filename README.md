# 🚀 Fund Transfer API & UI Test Suite

This project contains automated tests for:
- ✅ **Fund Transfer API** (Backend API Testing)
- ✅ **GomSpace Web UI** (UI Testing with Selenium WebDriver)

Both tests run inside a **Docker container**, so no manual setup is required!

---

## **📌 How to Run Tests**
### **Prerequisites**
1. Install **Docker** and **Docker Compose** on your system.  
   - [Download Docker](https://www.docker.com/get-started)

### **✅ Running Tests (One Command)**
1. Open a terminal and navigate to the project folder.
2. Run the following command:
   ```sh
   docker-compose up

Note - 
How to run a single feature or Scnerio.
    Run All Tests and View the Report - python run_tests.py
    Run a Specific Test Scenario and View the Report - python run_tests.py "Attempt to transfer a negative amount"
If you want to open the report manually.
    allure open allure-report
