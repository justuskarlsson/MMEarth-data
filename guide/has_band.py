import ee


ee.Authenticate()
ee.Initialize(project="ee-karlssonjustus")

aoi = ee.FeatureCollection(f"projects/ee-karlssonjustus/assets/aus_simple")
MOD14A1 = (
    ee.ImageCollection("MODIS/061/MOD14A1")
    .filterDate("2020-12-01", "2020-12-03")
    .filterBounds(aoi)
)
img = MOD14A1.first()
band_names = img.bandNames().getInfo()
print(band_names)
