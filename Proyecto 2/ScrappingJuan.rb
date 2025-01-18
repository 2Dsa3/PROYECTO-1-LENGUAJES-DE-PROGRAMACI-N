require 'nokogiri'
require 'open-uri'
require 'json'
require 'csv'




class Crash
  attr_accessor :date, :location, :aboard, :fatalities, :summary

  def initialize(date, location, aboard, fatalities, summary)

    @date = date
    @location = location
    @aboard = aboard
    @fatalities = fatalities
    @summary = summary
    
    if date == "?"
      @date = "unknown"
    end
    if location == "?"
      @location = "unknown"
    end
    if aboard == "?"
      @aboard = "unknown"
    end
    if fatalities == "?" 
      @fatalities = "unknown"
    end
    if summary == "?"
      @summary = "unknown"
    end

  end

  def save(file)
    CSV.open(file, 'a') do |csv|
      csv << [@date, @location, @aboard, @fatalities, @summary]
    end
  end

end


class PlaneCrashScraper



  def scrape_accident_data(url, output_file)
    puts "Scrapeando datos desde #{url}..."

    options = { "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" }

    html_content = URI.open(url + "database.htm", options).read
    parsed_content = Nokogiri::HTML(html_content)

    parsed_content.css("a").each do |link|

      year = link.text.strip

      puts "Scrapeando datos del año #{year}..."

      year_html = URI.open(url+ year + "/" + year + ".htm").read
      parsed_year = Nokogiri::HTML(year_html)

      sleep(rand(1..5))

      crash_counter = 1
      parsed_year.css("tr").drop(1).each do |row|

        crash_html = URI.open(url+ year + "/" + year + "-" + crash_counter.to_s + ".htm").read
        parsed_crash = Nokogiri::HTML(crash_html)

        crash = Crash.new("","","","","")
        
        parsed_crash.css("tr").drop(1).each do |field|

          if(field.css("b").text.strip == "Date:")
            crash.date = field.css("font").inner_text
          end
          if(field.css("b").text.strip == "Location:")
            crash.location = field.css("font").inner_text
          end
          if(field.css("b").text.strip == "Aboard:")
            crash.aboard = field.css("font").inner_text
          end
          if(field.css("b").text.strip == "Fatalities:")
            crash.fatalities = field.css("font").inner_text
          end
          if(field.css("b").text.strip == "Summary:")
            crash.summary = field.css("font").inner_text
          end

        end

        sleep(rand(1..5))

        crash.save(output_file)
        puts "#{year}: año #{crash_counter}"
        crash_counter += 1
      end


    end

    puts "Datos guardados exitosamente en '#{output_file}'."
    puts "Hecho por Juan Severino"
  end
end

# Ejemplo de uso
scraper = PlaneCrashScraper.new
scraper.scrape_accident_data('https://www.planecrashinfo.com/', 'plane_crashes.csv')