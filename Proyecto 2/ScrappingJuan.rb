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

class DetailedCrash < Crash
  attr_accessor :operator, :Flight

  def initialize(date, location, aboard, fatalities, summary, operator)
    super(date, location, aboard, fatalities, summary)
    @operator = operator
    if operator == "?"
      @operator = "unknown"
    end
  end
  def save(file)
    CSV.open(file, 'a') do |csv|
      csv << [@date, @location, @operator, @aboard, @fatalities, @summary]
    end
  end
end

class PlaneCrashScraper

  def scrape_accident_data(url, yearStart, output_file, user)
    puts "Scrapeando datos desde #{url}..."

    options = { "User-Agent" => user }

    year = yearStart.to_s
    while yearStart < Time.now.year
      year = year.to_s
      puts "Scrapeando datos del año #{year}..."

      year_html = URI.open(url + year + "/" + year + ".htm", options).read
      parsed_year = Nokogiri::HTML(year_html)

      crash_counter = 1
      parsed_year.css("tr").drop(1).each do |row|
        crash_html = URI.open(url + year + "/" + year + "-" + crash_counter.to_s + ".htm", options).read
        parsed_crash = Nokogiri::HTML(crash_html)

        crash = DetailedCrash.new("", "", "", "", "", "")

        parsed_crash.css("tr").drop(1).each do |field|
          if field.css("b").text.strip == "Date:"
            crash.date = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
          if field.css("b").text.strip == "Location:"
            crash.location = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
          if field.css("b").text.strip == "Aboard:"
            crash.aboard = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
          if field.css("b").text.strip == "Fatalities:"
            crash.fatalities = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
          if field.css("b").text.strip == "Summary:"
            crash.summary = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
          if field.css("b").text.strip == "Operator:"
            crash.operator = field.css("font").inner_text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '').gsub("\n", " ").strip
          end
        end

        crash.save(output_file)
        puts "#{crash_counter}: año #{year}"
        crash_counter += 1
      end
      year = year.to_i + 1
    end

    puts "Datos guardados exitosamente en '#{output_file}'."
    puts "Hecho por Juan Severino"
  end
end



# Ejemplo de uso

userDavid= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
userJuan= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
scraper = PlaneCrashScraper.new
scraper.scrape_accident_data('https://www.planecrashinfo.com/',2000, 'plane_crashes_with_operator.csv',userDavid)