#Imports
import obspy as op
import time
import os
import shutil
import configparser
import ast

#Class Definitions
class directory_manager:
    """Used to manage directory space for SeismoGrabber"""
    def __init__(self):
        self.time = None
        self.start_time = None
        self.current_directory = None
        
    def update_time(self, UTC_time):
        """Sets time attribute from user input"""
        self.time = UTC_time
    
    def make_directory(self):
        """Makes directory path if it does not already exist"""
        year = str(self.time.year)
        month = str(self.time.month)
        day = str(self.time.day)
        ym = year+"/"+month
        ymd = ym+"/"+day
        try:
            if not os.path.exists(year):
                os.mkdir(year)
            if not os.path.exists(ym):
                os.mkdir(ym)
            if not os.path.exists(ymd):
                os.mkdir(ymd)
        except Exception as e:
            print("Could not make directory.")
            print(e)
            
    def update_directory(self):
        """Finds out what the day's directory should be"""
        should_be = str(self.time.year)+"/"+str(self.time.month)+"/"+str(self.time.day)
        self.current_directory = should_be

class config_manager:
    """Used to streamline ObsPy database requests for SeismoGrabber"""
    def __init__(self):
        self.netwrk_stn_list = None
        self.channels = None
        self.locations = None
        self.last_fetch = None
        self.time = None
        self.start_time = None

    def update_time(self):
        """Updates attribute to an obspy UTCDateTime object"""
        self.time = op.core.UTCDateTime()
        
    def update_start_time(self):
        """Updates attribute to reflect a UTCDateTime object for the last fetch date"""
        self.start_time = op.core.UTCDateTime(self.last_fetch)

    def return_real_time():
        """Returns the current time in UTCDateTime fomat"""
        return op.core.UTCDateTime.now()
    
    def obspy_request_info(self):
        """Returns request info needed for ObsPy to query IRIS servers
            [('Network', 'Station', 'Location', 'Channel', 'Start Time',
              'End Time'),...]"""
        requests = []
        for request in range(len(self.netwrk_stn_list)):
            temp = (
            self.netwrk_stn_list[request][0],
            self.netwrk_stn_list[request][1],
            self.locations,
            self.channels,
            self.start_time,
            self.time
            )
            requests.append(temp)
        return requests

    def get_network_config(self, filepath='config.ini'):
        """Reads configuration file for query information"""
        config = configparser.ConfigParser()
        try:
            if os.path.exists(filepath):
                config.read(filepath)
                netwrk_getter = config.get('NETWORK', 'netwrk_stn_list')
                netwrk_stn_prelist = ast.literal_eval(netwrk_getter)
                netwrk_stn_list = []
                for x in netwrk_stn_prelist: netwrk_stn_list.append(x)
                self.netwrk_stn_list = netwrk_stn_list
                self.channels = config.get('NETWORK', 'channels').strip()
                self.locations = config.get('NETWORK', 'locations').strip()
                self.last_fetch = config.get('NETWORK', 'last_fetch_time').strip()
            else:
                print('Path does not exist')
                pass
        except IOError as e:
            print("Couldn't read the configuration file.")
            print(e)

    def write_network_config(self, filepath="config.ini"):
        """Writes current attribute settings to a configuration file"""
        config = configparser.ConfigParser()
        
        config['NETWORK'] = {
            'netwrk_stn_list' : str(self.netwrk_stn_list).strip('[]'),
            'channels' : str(self.channels),
            'locations' : str(self.locations),
            'last_fetch_time' : str(self.time)
        }
        if os.path.exists(filepath):
            print(filepath + " already exists. Do you wish to rewrite it?")
            choice = "Y"
            if choice.upper() == "Y" or "YES":
                try:
                    with open(filepath, "w+") as configfile:
                        config.write(configfile)
                except Exception as e:
                    print("Failed to write config file!")
                    print(e)
            elif choice.upper() == "N" or "NO":
                print("Config file not written")
            else:
                print("Not a valid choice, please enter Y/Yes or N/No")
        try:
            with open(filepath, "w+") as configfile:
                config.write(configfile)
        except Exception as e:
            print("Failed to write config file!")
            print(e)
            
    def startup_updater(self):
        """Startup method for a Configuration Manager object"""
        self.update_time()
        self.get_network_config()
        self.update_start_time()
