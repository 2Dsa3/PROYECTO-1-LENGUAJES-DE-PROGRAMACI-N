require 'nokogiri'

# Set up Selenium WebDriver
driver = Selenium::WebDriver.for :chrome
url = 'https://www.airfleets.net/flightlog/index.php?file=reportview&start=0&tot=3231'

# Navigate to the URL
driver.get(url)

# Wait for the page to fully load (adjust as needed)
sleep(3)  # Or use explicit waits to wait for specific elements to load

# Retrieve the page source after JavaScript has rendered content
html_content = driver.page_source

parsed_content = Nokogiri::HTML(html_content)

puts parsed_content