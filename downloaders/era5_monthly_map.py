import cdsapi
import os


def download():


    # set environment variable: export CDSAPI_KEY="eabc8e89-8554-46c4-bbac-66878901dd99"
    os.environ["CDSAPI_KEY"] = "eabc8e89-8554-46c4-bbac-66878901dd99"
    os.environ["CDSAPI_URL"] = "https://cds.climate.copernicus.eu/api"

    """
    Download ERA5 monthly data from the Copernicus Climate Data Store (CDS).
    """
    dataset = "reanalysis-era5-land-monthly-means"
    request = {
        "product_type": ["monthly_averaged_reanalysis"],
        "variable": ["2m_temperature"],
        "year": [
            "1950", "1951", "1952",
            "1953", "1954", "1955",
            "1956", "1957", "1958",
            "1959", "1960", "1961",
            "1962", "1963", "1964",
            "1965", "1966", "1967",
            "1968", "1969", "1970",
            "1971", "1972", "1973",
            "1974", "1975", "1976",
            "1977", "1978", "1979",
            "1980", "1981", "1982",
            "1983", "1984", "1985",
            "1986", "1987", "1988",
            "1989", "1990", "1991",
            "1992", "1993", "1994",
            "1995", "1996", "1997",
            "1998", "1999", "2000",
            "2001", "2002", "2003",
            "2004", "2005", "2006",
            "2007", "2008", "2009",
            "2010", "2011", "2012",
            "2013", "2014", "2015",
            "2016", "2017", "2018",
            "2019", "2020", "2021",
            "2022", "2023", "2024",
            "2025", "2026"
        ],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "time": ["00:00"],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [48.9, 4.6, 36.1, 19.3]
    }

    client = cdsapi.Client()
    target = 'data/era5_monthly_map.nc'
    client.retrieve(dataset, request, target)
