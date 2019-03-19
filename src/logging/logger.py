import os
import json
import datetime
import yaml
import glob
import pdb

class Logger():
    def __init__(self):
        self.outfile_name = self._get_file_name()
        yml_file_list = self._find_config_files()
        header_dict = {'file_name' : self.outfile_name, 'num_config_files': len(yml_file_list)}
        with open(self.outfile_name, 'w') as outfile:
            json.dump(header_dict, outfile)
            outfile.write('\n')
        self._record_config_files(yml_file_list)

    def _find_config_files(self):
        config_file_list = []
        for directory in os.listdir('./'):
            for config_file in glob.iglob('./' + directory + '**/*.yml', recursive=True):
                config_file_list.append(config_file)
          
        return config_file_list
  
    def _record_config_files(self,yml_file_list):
        for config_file in yml_file_list:
            with open(config_file, 'r') as infile:
                config_dict = yaml.safe_load(infile)
            out_dict = {config_file: config_dict}
            with open(self.outfile_name, 'a') as outfile:
                json.dump(out_dict, outfile)
                outfile.write('\n')


    def write_msg(self, pin_no, msg):

        datetime_str = self._get_datetime_str()
        
        log_dict = {'datetime': datetime_str, 'pin_no': pin_no, 'msg': msg} 

        with open(self.outfile_name, 'a') as outfile:
            json.dump(log_dict, outfile)
            outfile.write('\n')


    def _get_datetime_str(self):
        return datetime.datetime.now().strftime('%Y-%m-%d // %H:%M:%S')

    def _get_file_name(self):
        current_date = datetime.datetime.now().strftime('%Y_%m_%d')
        n = 1
        temp_name = 'logging/dir_log/' + current_date + '_%d.log' % n
        while os.path.isfile(temp_name):
            n += 1
            temp_name = 'logging/dir_log/' + current_date + '_%d.log' % n
        return temp_name
    

if __name__ == '__main__':
    
    ex_logger = Logger()

    ex_logger.write_msg(4, 'abcdefg testmsg') 
