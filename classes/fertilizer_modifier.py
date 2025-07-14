import os
import json

class FertilizerModifier:
    def __init__(self, directory_path, filename, json_filename):
        self.directory_path = directory_path
        self.filename = filename
        self.json_filename = json_filename
        self.snx_path = os.path.join(self.directory_path, self.filename)

        with open(self.json_filename, 'r') as f:
            data = json.load(f)
        self.fertilizers = data.get("fertilizers", [])

    def render_fertilizer_section(self):
        lines = []
        lines.append("*FERTILIZERS (INORGANIC)")
        lines.append("@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME")

        for fert in self.fertilizers:
            # Alignment the FAMN value with 5 left spaces
            line = "{:>2} {:>5} {:<5} {:<5} {:>5} {:>5.1f} {:>5} {:>5} {:>5} {:>5} {:>5} {}".format(
                fert["fert_level"],
                fert["fdate"],
                fert["fmcd"],
                fert["facd"],
                fert["fdep"],
                fert["famn"],  # Alignment FAMN 
                0,
                -99,
                -99,
                -99,
                -99,
                fert["fert_name"]
            )
            lines.append(line)

        # add one blank line after the last fertilizer line
        lines.append("")  # Linha em branco

        return "\n".join(lines) + "\n"

    def write_to_file(self):
        if not os.path.isfile(self.snx_path):
            raise FileNotFoundError(f"SNX not found: {self.snx_path}")

        with open(self.snx_path, 'r') as f:
            lines = f.readlines()

        start_idx = None
        for i, line in enumerate(lines):
            if "*FERTILIZERS (INORGANIC)" in line:
                start_idx = i
                break

        if start_idx is None:
            raise ValueError("Seção '*FERTILIZERS (INORGANIC)' não encontrada no arquivo .SNX")

        end_idx = start_idx + 1
        while end_idx < len(lines) and not lines[end_idx].startswith("*"):
            end_idx += 1

        new_section = self.render_fertilizer_section().splitlines(keepends=True)
        updated_lines = lines[:start_idx] + new_section + lines[end_idx:]

        with open(self.snx_path, 'w') as f:
            f.writelines(updated_lines)

        #print(f"[INFO] Fertilizers successfully inserted in: {self.snx_path}")
        #print("[INFO] Fertilizers successfully inserted")
