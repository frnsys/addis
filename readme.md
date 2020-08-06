## Data

In `data/`:

- `PopulationDensity2015EJRC`
    - As far as I can tell, this is where the data is from:
        - <https://ghsl.jrc.ec.europa.eu/ghs_pop2019.php>
        - <https://ghsl.jrc.ec.europa.eu/ghs_pop.php>
        - So the cell value is the number of people in that cell.
    - Based on the included readme, each cell is 5000m2, so dividing each cell's value by 5000 should get us the population density per square meter, which then makes resampling doable.
- `special_economic_zones`
    - Source: <https://www.ethiogis-mapserver.org/dataDownload.php>
    - Source: <https://datacatalog.worldbank.org/dataset/special-economic-zones-sez>
    - Only has 584 SEZs out of 3500-4000
    - Has 6 SEZs around Addis Ababa
    - Only provided as points, not shapes