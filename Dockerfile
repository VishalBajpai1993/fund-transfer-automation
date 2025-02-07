# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Edge WebDriver and required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    openjdk-11-jre \
    microsoft-edge \
    && wget -O /usr/local/bin/msedgedriver https://msedgedriver.azureedge.net/114.0.1823.43/edgedriver_linux64.zip \
    && chmod +x /usr/local/bin/msedgedriver

# Install Allure for report generation
RUN wget -O allure.tar.gz https://github.com/allure-framework/allure2/releases/latest/download/allure-2.21.0.tgz \
    && tar -zxvf allure.tar.gz \
    && mv allure-2.21.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure

# Default command: Run API and UI tests
CMD python run_tests.py && python run_ui_tests.py