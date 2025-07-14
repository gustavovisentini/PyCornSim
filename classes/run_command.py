# classes/run_command.py

"""
run_command Module

"""
import subprocess

class RunCommand:
    
    #:.. SNX file update values
    #:..
    @staticmethod
    def run_command(exec_path, *args):
        """
        Functions for execute terminal commands and return the results
        """
        command = [exec_path] + list(args)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
