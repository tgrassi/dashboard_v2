from preprocessors import global_temperature, era5_daily


preproc = [global_temperature,
           era5_daily
        ]



for p in preproc:
    p.preprocess()