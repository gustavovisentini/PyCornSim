# classes/soil_profile_appender.py

class SoilProfileAppender:
    """
    Appends a soil profile to a SOIL.SOL file.
    """

    @staticmethod
    def append_profile_to_file(output_file_path, soil_profile):
        """
        Appends a soil profile string to the specified SOIL.SOL file.
        
        Parameters:
            output_file_path (str): Path to the SOIL.SOL file.
            soil_profile (str): Soil profile content to be appended.
        """
        try:
            with open(output_file_path, 'a') as file:
                file.write('\n')  # Ensure there's a blank line before appending
                file.write(soil_profile)
        except Exception as e:
            print(f"Error writing to file {output_file_path}: {e}")
