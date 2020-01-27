import os
import json
import datetime
import yaml
import glob
from pubsub import pub

class Logger():
    """
    Class that allows processes to log messages in log files in JSON format
    """
    def __init__(self):
        self.outfile_name = self._get_file_name()       #Gets default log file name (SHOULD CHANGE DIRECTORY THAT LOGS GO IN
        yml_file_list = self._find_config_files()       #Finds all config files in subdirectories
        header_dict = {'file_name' : self.outfile_name, 'num_config_files': len(yml_file_list)}
        with open(self.outfile_name, 'w') as outfile:
            json.dump(header_dict, outfile)             #Write header to log file
            outfile.write('\n')
        self._record_config_files(yml_file_list)        #Write config files to log to track config values for each process

        self.log_dict = dict()
        pub.subscribe(self.write_msg, 'write msg')

    def _find_config_files(self):
        """
        Finds all config.yml files in subdirectories

        Returns:
        A list of config.yml file paths
        """
        config_file_list = []
        for directory in os.listdir('src'):
            for config_file in glob.iglob('src/' + directory + '**/*.yml', recursive=True):
                config_file_list.append(config_file)
          
        return config_file_list
  
    def _record_config_files(self,yml_file_list):
        """
        Loads config files from yml format and dumps them as JSON in the log file

        Keyword arguments:
        yml_file_list --  List of config.yml file paths
        """
        for config_file in yml_file_list:
            with open(config_file, 'r') as infile:
                config_dict = yaml.safe_load(infile)
            out_dict = {config_file: config_dict}
            with open(self.outfile_name, 'a') as outfile:
                json.dump(out_dict, outfile)
                outfile.write('\n')
                pub.sendMessage("config dict", config_dict=out_dict)


    def write_msg(self, author, msg):
        """
        Writes a log given data from process

        Keyword arguments:
        author -- author of message being written
        msg -- Message to be recorded (data on pin)
        """

        datetime_str = self._get_datetime_str()
        
        self.log_dict = {'datetime': datetime_str, 'author': author, 'msg': msg} 

        with open(self.outfile_name, 'a') as outfile:
            json.dump(self.log_dict, outfile)
            outfile.write('\n')


    def _get_datetime_str(self):
        """
        Finds formatted current date and time

        Returns:
        A string formatted date and time
        """
        return datetime.datetime.now().strftime('%Y-%m-%d // %H:%M:%S')

    def _get_file_name(self):
        """
        Finds a filename for the output log file

        Returns:
        Filename for the log file
        """
        current_date = datetime.datetime.now().strftime('%Y_%m_%d')
        n = 1
        temp_name = 'logs/' + current_date + '_%d.log' % n
        while os.path.isfile(temp_name):                                    #Loops until open file name is found
            n += 1
            temp_name = 'logs/' + current_date + '_%d.log' % n
        return temp_name
