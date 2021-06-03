import datetime
import pandas as pd
from netCDF4 import Dataset



class GeoField:
    """
    GeoField represents the time series of a geographic field.
    All represented fields have two spatial dimensions (longitude,
    latitude) and one temporal dimension.  Optionally the fields may
    have a height dimension.
    """
    def __init__(self, netcd4_loc):
        """
        Initialize to empty data.
        """
        self.netCDF4 = netcd4_loc
        self.start_date_time = datetime.datetime(1948, 1, 1, 0, 0, 0)
        self.d = Dataset(self.netCDF4)
        self.lons = None
        self.lats = None
        self.tm = None
        self.cos_weights = None

    def data(self):
        """
        Return a copy of the stored data as a multi-array. If access
        without copying is required for performance reasons, use
        self.d at your own risk.
        """
        return self.d.copy()

    def print_data_description(self):
        d = self.d
        print(d.title)
        print('Description')
        print(d.description)
        print(f"\nDimension :")
        print(f"    time: {d.dimensions['time']}")
        print(f"    longitude: {d.dimensions['lon']}")
        print(d.variables['slp'])
        print(f"    latitude: {d.dimensions['lat']}")

    def load(self):
        """
        Load GeoData structure from netCDF file.
        """

        v = self.d.variables

        # extract the data

        # extract spatial & temporal info
        self.lons = self.d.variables['lon'][:]
        self.lats = self.d.variables['lat'][:]
        # 24 hours
        self.tm = self.d.variables['time'][:]
        date_time = self.start_date_time
        data = {}
        print(len(self.tm))
        print(len(self.lats))
        print(self.d.variables['slp'][0])
        print(self.d.variables['slp'][0].shape)
        for i, tm in enumerate(self.slp):
            data['time'] = date_time
            data['latitude'] = self.lats[i]
            data['longitude'] = self.lons[i]
            date_time += datetime.timedelta(hours=6)
            print(date_time, self.lats[i], self.lons[i])
        df = pd.DataFrame(data)
        print(df.head())


gf = GeoField(netcd4_loc='/Volumes/ext_data/ncep/slp.1948.nc')
gf.load()



class Dataset(object):
    def __init__(self, data_location):
        self.data_location = data_location

    def load_monthly_data_general(self):
        pass
