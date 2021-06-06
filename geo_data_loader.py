import time
import datetime
import logging
import pandas as pd
from netCDF4 import Dataset
import geopandas
import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)

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
        self.cdf_data = Dataset(self.netCDF4)
        self.lons = self.cdf_data.variables['lon'][:]
        self.lats = self.cdf_data.variables['lat'][:]
        self.tm = self.cdf_data.variables['time'][:]
        self.date_time = []
        self.cos_weights = None

    def __repr__(self):
        print(self.cdf_data)
        return ""

    def get_cdf_data(self):
        return self.cdf_data


class MonthlyMean(GeoField):
    def __init__(self, netcd4_loc, start_year=1948, end_year=1949):
        GeoField.__init__(self, netcd4_loc)
        total_months = (end_year - start_year) * 12
        dti = pd.date_range(f"{start_year}-01-01", periods=total_months, freq="M")
        print(dti)

    def __repr__(self):
        print(self.cdf_data)
        return ""

    def get_data(self, variable):
        return self.cdf_data[variable]


class Daily4x(GeoField):
    def __init__(self, netcd4_loc, year, variable):
        GeoField.__init__(self, netcd4_loc)
        self.date_time = []
        date_time = datetime.datetime(year, 1, 1, 0, 0, 0)
        for _ in enumerate(self.tm):
            self.date_time.append(date_time)
            date_time += datetime.timedelta(hours=6)
        logging.info(f"Loaded {variable} of shape {self.cdf_data.variables[variable].shape}")

    def render(self, variable, time_slice=0):
        """
        Render a geographic plot
        """
        t = time.process_time()
        render_data = dict()
        render_data['Data'] = []
        render_data['Latitude'] = []
        render_data['Longitude'] = []
        _data = self.cdf_data.variables
        for i, latitude in enumerate(_data['lat'][:]):
            for j, longitude in enumerate(_data['lon'][:]):
                render_data['Longitude'].append(longitude)
                render_data['Latitude'].append(latitude)
                render_data['Data'].append(_data[variable][time_slice][i][j])
        df = pd.DataFrame(render_data)
        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        ax = world.plot()
        gdf.plot(column='Data', ax=ax, legend=True)
        logging.info(f'Elapsed time {time.process_time() - t}')
        plt.show()


def main():
    logging.info("Testing GeoField")
    gf = Daily4x(netcd4_loc='/Volumes/ext_data/ncep/air.sig995.1948.nc', year=1948, variable='air')


if __name__ == "__main__":
    main()



