# classes/find_closest_soil.py

"""


"""

import math

class SoilProfileFinder:
    def __init__(self, file_path):
        self.file_path = file_path

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # radius of the earth in km
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

    def find_closest_profile(self, target_lat, target_lon):
        closest_distance = float('inf')
        closest_id = None
        closest_index = None

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                if line.startswith('*'):
                    current_id = line.strip().lstrip("*").split()[0]  # <-- Adjust here
                    current_index = i
                elif line.startswith('@SITE'):
                    lat_lon_line = lines[i + 1]
                    parts = lat_lon_line.split()
                    try:
                        current_lat = float(parts[2])
                        current_lon = float(parts[3])
                    except ValueError:
                        continue

                    distance = self.haversine_distance(target_lat, target_lon, current_lat, current_lon)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_id = current_id
                        closest_index = current_index

        if closest_index is not None:
            profile_lines = []
            for line in lines[closest_index:]:
                if line.startswith('*') and line.strip().lstrip("*").split()[0] != closest_id:
                    break
                profile_lines.append(line)
            return closest_id, ''.join(profile_lines)

        return None, None
