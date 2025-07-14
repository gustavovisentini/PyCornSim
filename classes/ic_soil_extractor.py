import subprocess
import os

class IcSoilExtractor:
    def __init__(self, soils_dir, latitude, longitude):
        self.soils_dir = soils_dir
        self.latitude = latitude
        self.longitude = longitude
        self.gdal_bin = "gdallocationinfo"
        self.files = {
            'soil': "soil_profile_number.asc",
            'ICRES': "ICRES.asc",
            'ICRT': "ICRT.asc",
            'ICREN': "ICREN.asc"
        }
        self.soil = None
        self.ICRES = None
        self.ICRT = None
        self.ICREN = None

    def _run_gdal(self, filename):
        filepath = os.path.join(self.soils_dir, filename)
        try:
            cmd = [
                self.gdal_bin, "-geoloc", filepath,
                str(self.longitude), str(self.latitude)
            ]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()

            for line in output.splitlines():
                if "Value:" in line:
                    value = line.split("Value:")[1].strip()
                    if value.isnumeric() or value.replace(".", "", 1).isdigit():
                        return value.zfill(2) if len(value) == 1 else value
            return "N/A"
        except Exception:
            return "N/A"

    def extract(self):
        values = {key: self._run_gdal(fname) for key, fname in self.files.items()}
        self.soil = values['soil'].rjust(4)
        self.ICRES = values['ICRES'].rjust(4)
        self.ICRT = values['ICRT'].rjust(4)
        self.ICREN = values['ICREN'].rjust(4)
