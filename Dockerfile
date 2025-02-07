# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies, including Edge WebDriver and Microsoft Edge Browser
# Install dependencies, including Edge WebDriver and Microsoft Edge Browser
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    openjdk-11-jre \
    software-properties-common \
    gnupg2 \
    lsb-release \
    ca-certificates \
    && echo "Adding Microsoft GPG key..." \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && DISTRO=$(lsb_release -c | awk '{print $2}') \
    && echo "Adding Edge repository..." \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge $DISTRO main" | tee /etc/apt/sources.list.d/microsoft-edge-stable.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable \
    && echo "Downloading Edge WebDriver..." \
    && wget -O msedgedriver.zip https://msedgedriver.azureedge.net/114.0.1823.43/edgedriver_linux64.zip \
    && unzip msedgedriver.zip \
    && mv msedgedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/msedgedriver \
    && echo "Microsoft Edge and WebDriver installed successfully"
# Set Edge WebDriver path
ENV PATH="/usr/local/bin:$PATH"

# Install Allure for report generation
RUN wget -O allure.tar.gz https://github.com/allure-framework/allure2/releases/latest/download/allure-2.21.0.tgz \
    && tar -zxvf allure.tar.gz \
    && mv allure-2.21.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure

# Default command: Run API and UI tests
CMD python run_tests.py && python run_ui_tests.py