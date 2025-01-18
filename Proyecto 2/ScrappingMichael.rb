require 'nokogiri'
require 'open-uri'
require 'json'
require 'csv'

class Scrapper
  def extraction(url, output_file)
    puts "Scrapeando datos desde #{url}..."

    
    html_content = URI.open(url).read
    parsed_content = Nokogiri::HTML(html_content)


    script_content = parsed_content.css('script').find do |script|
      script.content.include?('var charts')
    end


    json_match = script_content.content.match(/var charts = ({.*});/)

    charts_data = JSON.parse(json_match[1])

    
    series_data = charts_data['general']['series']

    CSV.open(output_file, 'w') do |csv|
      csv << %w[Year Date Flights] 
      series_data.each do |series|
        year = series['name'] 
        data_points = series['data']

        data_points.each do |timestamp, flights|
          date = Time.at(timestamp / 1000).strftime('%Y-%m-%d')
          csv << [year, date, flights]
        end
      end
    end

    puts "Datos guardados exitosamente en '#{output_file}'."
    puts "Hecho Por Michael Poveda"
  end
end


scraper = Scrapper.new
scraper.extraction('https://www.flightradar24.com/data/statistics', 'flights_all_years.csv')
