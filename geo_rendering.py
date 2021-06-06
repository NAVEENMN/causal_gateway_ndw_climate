import logging
import time
import pandas as pd
import geopandas
from geo_data_loader import GeoField
import matplotlib.pyplot as plt
import geopandas

logging.basicConfig(format='%(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)

class Render(object):
    """
    Renders a geo field.
    """
    def __init__(self, data, variable, time_slice=0):
        self.cdf_data = data
        self.time_slice = time_slice
        self.variable = variable

    def transform(self,):
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
                render_data['Data'].append(_data[self.variable][self.time_slice][i][j])
        df = pd.DataFrame(render_data)
        gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
        print(gdf.head())
        logging.info(f'Elapsed time {time.process_time() - t}')
        return gdf

    def render(self, gdf):
        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        print(world.head())
        ax = world.plot()
        gdf.plot(column='Data', ax=ax, legend=True)
        plt.show()


def main():
    print("Testing geo rendering")
    gf = GeoField(netcd4_loc='/Volumes/ext_data/ncep/air.sig995.1948.nc', year=1948, variable='air')
    gf.load()
    rd = Render(gf.get_cdf_data(), variable='air')
    gdf = rd.transform()
    rd.render(gdf)


if __name__ == "__main__":
    main()

