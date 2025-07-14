import os

class TemplateModifier:
    """
    Modify DSSAT SNX template files by replacing placeholders with actual values.
    """

    @staticmethod
    def modify_snx_expression(directory, filename, weather_station, id_soil, fh_dur, year_planting,sdate, ingeno, cname, icrt, icres, icren):
        file_path = os.path.join(directory, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"[ERROR] File not found: {file_path}")

        substitutions = {
            "{{WEATHER_STATION}}": weather_station,
            "{{ID_SOIL}}": id_soil,
            "{{FHDUR}}": str(fh_dur),
            "{{SDATE}}": str(sdate),
            "{{Y_PLANT}}": str(year_planting),
            "{{INGENO}}" : ingeno,
            "{{CNAME}}" : cname,
            "{{ICRT}}" : str(icrt),
            "{{ICRES}}": str(icres),
            "{{ICREN}}": str(icren)
        }

        with open(file_path, 'r') as f:
            content = f.read()

        for key, value in substitutions.items():
            if key not in content:
                print(f"[WARNING] Placeholder {key} not found in {filename}")
            content = content.replace(key, value)

        with open(file_path, 'w') as f:
            f.write(content)

        #print(f"[INFO] Updated SNX file: {file_path}")
        #print(f"[INFO] SNX file Updated")

