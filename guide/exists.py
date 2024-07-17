import ee


ee.Authenticate()
ee.Initialize(project="ee-karlssonjustus")

aoi = ee.FeatureCollection(f"projects/ee-karlssonjustus/assets/aus_simple")
MOD14A1: ee.imagecollection.ImageCollection = (
    ee.ImageCollection("MODIS/061/MOD14A1")
    .filterDate("2024-12-01", "2024-12-03")
    .filterBounds(aoi)
)
print(MOD14A1.size().getInfo())

