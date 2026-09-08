import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

def preprocess():

    # open era5_monthly_map.nc
    ds = xr.open_dataset("data/era5_monthly_map.nc")

    dates = ds["valid_time"].values

    years = np.array([pd.to_datetime(d).year for d in dates])  # years
    months = np.array([pd.to_datetime(d).month for d in dates])  # months
    years_season = [y if m != 12 else y + 1 for y, m in zip(years, months)] # years assuming that December belongs to the next year for seasonal analysis

    # get season (DJF, MAM, JJA, SON) for each month
    def get_season(month):
        seasons_dict = {
            "DJF": [12, 1, 2],
            "MAM": [3, 4, 5],
            "JJA": [6, 7, 8],
            "SON": [9, 10, 11]
        }

        for season, months in seasons_dict.items():
            if month in months:
                return season
        return None

    # get seasons for each month and year
    seasons = np.array([get_season(m) for m in months])

    # get lats, lons, and temperature
    lats = ds["latitude"].values
    lons = ds["longitude"].values
    temp = ds["t2m"].values - 273.15  # convert from K to C

    # get last month, year, and season
    last_month = months[-1]
    last_year = years[-1]
    last_season = seasons[-1]

    print(f"Last month: {last_month}, Last year: {last_year}, Last season: {last_season}")


    temp_mean = []
    for y in sorted(np.unique(years_season)):
        temp_mean.append(np.mean(temp[(years_season == y) & (seasons == last_season), :, :], axis=0))

    temp_mean_last = np.mean(temp[(years_season == last_year) & (seasons == last_season), :, :], axis=0)

    temp_rank = np.sort(temp_mean, axis=0)

    rank = len(np.unique(years_season)) - np.argmin(np.abs(temp_rank - temp_mean_last), axis=0)

    print(f"Rank shape: {rank.shape}")

    world = gpd.read_file("./geo/geoBoundaries-ITA-ADM0.shp")

    #print(world.head())

    # Plot the single country boundary
    # temp_max = np.max(temp[idx, :, :], axis=0)
    fig, ax = plt.subplots(figsize=(7, 6))
    #ax.tripcolor(X.flatten(), Y.flatten(), diff.flatten(), cmap="RdYlBu_r", vmin=-val, vmax=val)
    #p = ax.pcolor(lons, lats, rank, cmap="tab10", vmin=1, vmax=10)
    p = ax.contourf(lons, lats, rank, levels=np.arange(1, 6) - 0.5, cmap="RdYlBu")
    #plt.colorbar()
    world.plot(ax=ax, facecolor="none", edgecolor="k", linewidth=1)
    cbar = plt.colorbar(p, ax=ax)
    cbar.set_ticks([1, 2, 3, 4])
    cbar.set_ticklabels(["Primo", "Secondo", "Terzo", "Quarto"])
    cbar.ax.invert_yaxis()
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    preprocess()