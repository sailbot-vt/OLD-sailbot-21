import json
import pdb
from pprint import pprint as pp

class logReader():
    """
    Class that allows for log readback
    """
    def __init__(self, infile):
        """
        Initialization of reader
        Reads header and config files

        Keyword arguments:
        infile -- File path to log file to be read
        """ 
        self.infile = infile
        self.logfile = open(self.infile, 'r');
        self.lineno = 0
        self.read_header()
        self.read_configs()

    def read_header(self):
        """
        Reads header and stores as dictionary
        """
        self.header = json.loads(self.logfile.readline())
        self.lineno += 1

    def read_configs(self):
        """
        Reads config files and stores as dictionary
        """
        num_config_files = self.header['num_config_files'] 
        self.config_dict = {}
        for n in range(num_config_files):
            temp_config_dict = json.loads(self.logfile.readline())
            self.lineno += 1
            self.config_dict.update(temp_config_dict)

    def read_log(self):
        """
        Reads log line by line as a generator
        Create generator by calling:
            example_generator = exampleLogReader.read_log()
        Obtain logs one by one by calling:
            exampleLog = example_generator.__next__()
        
        Returns:
        A log with datetime, pin number, and a message
        """
        for line in self.logfile.readlines():
            yield json.loads(line)
            self.lineno += 1
