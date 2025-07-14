import os
import time
import json

from classes.template_modifier import TemplateModifier
from classes.run_command import RunCommand
from classes.prepare_simulation import PrepareSimulation
from classes.soil_profile_finder import SoilProfileFinder
from classes.weather_downloader import WeatherDownloader
from classes.soil_profile_appender import SoilProfileAppender
from classes.ic_soil_extractor import IcSoilExtractor
from classes.post_processing import PostProcessing

if __name__ == '__main__':
    print('[INFO] :..Starting PyCornSim without')

    # Static configuration variables
    WEATHER_START_DATE = "20090101"     #format yyyymmdd
    WEATHER_END_DATE = "20241231"       #format yyyymmdd
    FILENAME_SNX = "UFGA0002.SNX"       
    WEATHER_STATION_NAME = "WSTATION"
    DURATION_IN_YEARS = 1
    RUN_ID = "INGENO_"

    # JSON configuration file path
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')

    # Load configuration
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)

    user_name = config_data.get("name")
    lat = config_data.get("latitude")
    lon = config_data.get("longitude")
    simulation_start = config_data.get("sim_year")     #format yyddd
    year_planting = config_data.get("planting_year")   #format yy
    irrigated = config_data.get("irrigated")
    ingeno = config_data.get("ingeno")
    cname = config_data.get("cname")


    # Start timer
    start_time = time.time()

    #Download and prepare wether file from NASA POWER API
    print(f"[INFO] Downloading weather data for location {lat, lon} ...")
    downloader = WeatherDownloader(lat, lon, WEATHER_START_DATE, WEATHER_END_DATE)
    if not downloader.download():
        print("[ERROR] Weather data download failed. Exiting.")
        exit()

    #Find the soil profile in US.SOIL corresponding to correct lat and lon
    print(f"[INFO] Finding soil profile for location {lat, lon} ...")
    soil_finder = SoilProfileFinder("soil/US.SOL")
    soil_id, soil_profile = soil_finder.find_closest_profile(lat, lon)

    #Find the initial conditions of the soil corresponding to correct lat and lon
    print("[INFO] Extracting IC from location...")
    extractor = IcSoilExtractor('soil', lat, lon)
    extractor.extract()
    ICREN, ICRES, ICTR = extractor.ICREN, extractor.ICRES, extractor.ICRT

    #
    print(f"[INFO] Simulation for {cname}")
    sim_path = PrepareSimulation().execute_create_dir(RUN_ID + ingeno, lat, lon, soil_id, soil_profile)
    soil_file_path = os.path.join(sim_path, "SOIL.SOL")
    SoilProfileAppender().append_profile_to_file(soil_file_path, soil_profile)

    #make the modifies in the SNX simulation file using {expression language}
    TemplateModifier().modify_snx_expression(
        sim_path, FILENAME_SNX, WEATHER_STATION_NAME, soil_id,
        DURATION_IN_YEARS, year_planting,simulation_start, ingeno, cname,
        ICTR, ICRES, ICREN
    )

    #get the dssat executable path
    dssat_app = os.path.join(os.path.dirname(__file__), 'dssat/dscsm048')
    #running the simulation
    RunCommand.run_command(dssat_app, 'A', FILENAME_SNX)

    #filtering the results
    processor = PostProcessing(sim_path=sim_path, filename='summary.csv')
    processor.process()
    processor.save_processed()

    print("[INFO] All simulations completed. Genereting filtered file processed_output.csv")
    end_time = time.time()
    print(f"\n[INFO] Execution completed in: {end_time - start_time:.2f} seconds\n")