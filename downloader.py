from downloaders import (ghg_mlo,
                         nasa_ssta,
                         pulse,
                         sunspots,
                         mediteranean_ssta,
                         ocean_heat,
                         elnino
                         )

modules = [
        ocean_heat,
        elnino,
        mediteranean_ssta,
        nasa_ssta,
        ghg_mlo,
        pulse,
        sunspots
    ]


for module in modules:
    module.download()
    break