#Imports
import obspy as op
from obspy.clients.fdsn import Client
import time
import os
import shutil
import configparser
import ast
from SeismoGrabberClasses import *

#Main Function
def main():
    """Reads config.ini then downloads IRIS waveforms to build a .kml inventory
        and .mseed file from them. Finally saves images of each waveform plot"""
  
# Set up initial variables  
    dm = directory_manager()
    cm = config_manager()
    IRIS_client = Client("IRIS")
    cm.startup_updater()
    request_info = cm.obspy_request_info()
    dm.update_time(cm.time)
    dm.update_directory()
    dm.make_directory()
    cd = dm.current_directory
    base_fn = cm.time.isoformat().replace(":", "").replace(".", "")
    inv_fn = base_fn + ".kml"
    stream_fn = base_fn + ".mseed"
    dm_inv_fn = cd+"/"+inv_fn
    dm_stream_fn = cd+"/"+stream_fn

# Send server requests for inventory and instrument traces
    print("Building Inventory...")
    inventory = IRIS_client.get_stations_bulk(request_info, level='response')
    print("Gathering Waveforms from IRIS server. This may take a while...")
    stream = IRIS_client.get_waveforms_bulk(request_info)
    print("Completed.")
    
# Write data to file, create instrument waveform plots,
# and save them in the appropriate directory
    print("Writing Files...")
    inventory.write(base_fn, format="KML")
    shutil.move(inv_fn, cd)
    stream.write(stream_fn, format="MSEED")
    shutil.move(stream_fn, cd)
    for x in range(len(stream)):
        trace = stream[x]
        fn = str(trace.id)+".PNG"
        plot_fn = cd+"/"+fn
        trace.plot(outfile=fn, size=(1600, 500), format="PNG")
        shutil.move(fn, cd)
    cm.write_network_config()
    print("Completed. Seismology Time!")
#Main
if __name__ == "__main__":
    main()
