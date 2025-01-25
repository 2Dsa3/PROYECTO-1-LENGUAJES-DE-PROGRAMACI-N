require 'nokogiri'
require 'open-uri'
require 'selenium-webdriver'
require 'csv'

class AirfleetsScrapper
    def headers(output_file) 
        CSV.open(output_file, 'w') do |csv|
            csv << %w[Date Airline Departure Arrival OverallRating ReportLink] 
        end
    end

    def extraction(url, output_file)
        # Set up Selenium WebDriver
        driver = Selenium::WebDriver.for :chrome
        driver.get(url)
        sleep(2.4)  # Use explicit waits to wait for specific elements to load
        html_content = driver.page_source
        sleep(2.4) # Adding a sleep to avoid scraper detection
        parsed_content = Nokogiri::HTML(html_content)

        table = parsed_content.css('table')
        tabcontent = table.css('.tab23 .tabcontent').each do |cell|
            date = cell.css('td')[0].text
            flight = cell.css('td')[1]
            #get the link of the flight
            link = flight.css('a').first.attribute('href').text
            airline = link.split('/')[2].split('.')[0].split('_')[2]
            departure = cell.css('td')[2].text
            arrival = cell.css('td')[3].text
            overall_rating = cell.css('td')[4]
            #get hte imgs
            imgs = overall_rating.css('img')
            star2Count = 0
                for img in imgs
                    star= img.attribute('src').text.split('/')[2].split('.')[0]
                    if star == 'star2' then star2Count+=1 end
                end

            report = cell.css('td')[5]
            reportview= report.css('a').first.attribute('href').text

            Flight.new(date, airline, departure, arrival, star2Count, reportview).save(output_file) 
            
        end

        driver.quit

    end



          
end

class AirfleetsScrapperPageIterator < AirfleetsScrapper 

    def extraction(url, output_file, pagIni, pagFin) 
        i = pagIni
        while i < pagFin +1
            puts "Extraction #{i}"
            super(url, output_file)
            puts "Changing url"
            url = changeUrl(url)
            i += 1
            sleep(3) # Adding a sleep to avoid scraper detection
        end

    
    end

    def changeUrl(url)
        sleep(3) # Adding a sleep to avoid scraper detection
        url = url.split('=')
        url[2] = (url[2].split('&')[0].to_i + 50).to_s
        url[2] = url[2] + '&tot'
        url = url.join('=')
        puts url
        return url
    end

end

class Flight
  attr_accessor :date, :flight, :departure, :arrival, :overall_rating, :report

  def initialize(date, flight, departure, arrival, overall_rating, report)
    @date = date
    @flight = flight
    @departure = departure
    @arrival = arrival
    @overall_rating = overall_rating
    @report = report
    
  end

    def save(file)
        CSV.open(file, 'a') do |csv|
            csv << [@date, @flight, @departure, @arrival, @overall_rating, @report]
        end
        
    end
end


#First Scrapping
# ini = AirfleetsScrapper.new
# ini.headers('rated_flights.csv')

# scrapper = AirfleetsScrapperPageIterator.new
# url = 'https://www.airfleets.net/flightlog/index.php?file=reportview&start=0&tot=3231'

# scrapper.extraction(url, 'RatedFlights.csv')

#Final Scrapping

# scrapper = AirfleetsScrapperPageIterator.new
# url = 'https://www.airfleets.net/flightlog/index.php?file=reportview&start=450&tot=3231' #Si el scrapping se detiene, cambiar el valor de start por el valor de la pagina en la que se quedo
# scrapper.extraction(url, 'rated_flights.csv',10,62)



