import os
import subprocess

class WeatherDownloader:
    def __init__(self, lat, lon, start_date, end_date):
        self.lat = lat
        self.lon = lon
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = "weather"
        self.output_file = os.path.join(self.output_dir, "WSTATION.WTH")

    def download(self):
        os.makedirs(self.output_dir, exist_ok=True)

        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point"
            f"?parameters=T2M,PRECTOT,ALLSKY_SFC_SW_DWN"
            f"&community=AG"
            f"&longitude={self.lon}"
            f"&latitude={self.lat}"
            f"&start={self.start_date}"
            f"&end={self.end_date}"
            f"&format=ICASA"
        )

        command = ["curl", "-s", "-o", self.output_file, url]
        try:
            subprocess.run(command, check=True)
            print(f"[INFO] Download completed on: {self.output_file}")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Error during download.")
            return False