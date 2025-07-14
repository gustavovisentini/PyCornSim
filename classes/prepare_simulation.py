# classes/prepare_simualtion.py

"""
prepare_sumulation Module

Prepare the directories and copy necessary files for simulation

"""


import os
import shutil

class PrepareSimulation:
    def __init__(self, script_dir=None):
        self.script_dir = script_dir or os.path.dirname(os.path.realpath(__file__))

    def create_simulation_directory(self, location_id):
        output_dir = os.path.join(self.script_dir, "..", "OUTPUT", str(location_id))
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        return output_dir

    # copy the files with that names
    def copy_required_files(self, sim_dir):
       
        file_map = {
            "WSTATION.WTH":    os.path.join(self.script_dir, "..", "weather", "WSTATION.WTH"),
            "UFGA0002.SNX": os.path.join(self.script_dir, "..", "template", "UFGA0002.SNX"),
            "SOIL.SOL":       os.path.join(self.script_dir, "..", "soil", "SOIL.SOL"),
            "MZCER048.CUL":   os.path.join(self.script_dir, "..", "template", "MZCER048.CUL"),
            "MZCER048.ECO":   os.path.join(self.script_dir, "..", "template", "MZCER048.ECO"),
            "MZCER048.SPE":   os.path.join(self.script_dir, "..", "template", "MZCER048.SPE"),
        }

        for target, source in file_map.items():
            if not os.path.exists(source):
                print(f"[ERROR] File not found: {source}")
                continue
            shutil.copy(source, os.path.join(sim_dir, target))

        return file_map

    def execute_create_dir(self, location_id, lat, lon, s_id, s_profile):
        #Create the folder with the location_id
        sim_dir = self.create_simulation_directory(location_id)
        #Copy the files
        self.copy_required_files(sim_dir)
        os.chdir(sim_dir)        
        #print(f"[INFO] Simulation prepared in: {sim_dir}")
        #print(f"[INFO] Simulation prepared")
        #return the folder path with the files inside
        return sim_dir
