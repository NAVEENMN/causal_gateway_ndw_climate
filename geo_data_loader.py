import datetime
import logging
import pandas as pd
from netCDF4 import Dataset
import geopandas

logging.basicConfig(format='%(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

class GeoField:
    """
    GeoField represents the time series of a geographic field.
    All represented fields have two spatial dimensions (longitude,
    latitude) and one temporal dimension.  Optionally the fields may
    have a height dimension.
    """
    def __init__(self, netcd4_loc, year, variable):
        """
        Initialize to empty data.
        """
        self.netCDF4 = netcd4_loc
        self.start_date_time = datetime.datetime(year, 1, 1, 0, 0, 0)
        self.cdf_data = Dataset(self.netCDF4)
        self.variable = variable
        self.lons = None
        self.lats = None
        self.tm = None
        self.date_time = []
        self.cos_weights = None

    def get_cdf_data(self):
        return self.cdf_data

    def data(self):
        """
        Return a copy of the stored data as a multi-array. If access
        without copying is required for performance reasons, use
        self.d at your own risk.
        """
        return self.cdf_data.copy()

    def print_data_description(self):
        d = self.cdf_data
        print(d.title)
        print('Description')
        print(d.description)
        print(f"\nDimension :")
        print(f"    time: {d.dimensions['time']}")
        print(f"    longitude: {d.dimensions['lon']}")
        print(d.variables[self.variable])
        print(f"    latitude: {d.dimensions['lat']}")

    def load(self):
        """
        Load GeoData structure from netCDF file.
        """
        # extract spatial & temporal info
        self.lons = self.cdf_data.variables['lon'][:]
        self.lats = self.cdf_data.variables['lat'][:]
        self.tm = self.cdf_data.variables['time'][:]
        date_time = self.start_date_time
        for _ in enumerate(self.tm):
            self.date_time.append(date_time)
            date_time += datetime.timedelta(hours=6)
        logging.info(f"Loaded {self.variable} of shape {self.cdf_data.variables[self.variable].shape}")


def main():
    logging.info("Testing GeoField")
    gf = GeoField(netcd4_loc='/Volumes/ext_data/ncep/air.sig995.1948.nc', year=1948, variable='air')
    gf.load()


if __name__ == "__main__":
    main()



