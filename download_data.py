import requests
from multiprocessing.pool import ThreadPool

location = '/Volumes/ext_data/ncep'


def download_data(url):
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(f'{location}/{file_name}', 'wb') as f:
            for data in r:
                f.write(data)
    return url


def download_sea_level_pressure_data(start_year=1948,
                                     end_year=1960):
    sea_level_pressure_url = 'https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/surface'
    print(f'Downloading sea level pressure data from {sea_level_pressure_url}')
    sea_level_pressure_urls = [f'{sea_level_pressure_url}/slp.{year}.nc' for year in range(start_year, end_year)]
    # Run 5 multiple threads. Each call will take the next element in urls list
    results = ThreadPool(10).imap_unordered(download_data, sea_level_pressure_urls)
    for r in results:
        print(r)
    print(f'Data is stored in {location}')


def download_air_temperature_data(start_year=1948, end_year=1960):
    air_temperature_url = 'https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/surface'
    print(f'Downloading air temperature data from {air_temperature_url}')
    air_temperature_urls = [f'{air_temperature_url}/air.sig995.{year}.nc' for year in range(start_year, end_year)]
    # Run 5 multiple threads. Each call will take the next element in urls list
    results = ThreadPool(10).imap_unordered(download_data, air_temperature_urls)
    for r in results:
        print(r)
    print(f'Data is stored in {location}')


download_sea_level_pressure_data()
download_air_temperature_data()
