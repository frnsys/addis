import rasterio
import matplotlib
import rasterio.warp
import rasterio.features
from matplotlib import pyplot
from rasterio.windows import Window
from rasterio.enums import Resampling
from pyproj import CRS, Transformer

# For X11 forwarding
matplotlib.use('TkAgg')

# equivalent to wgs:84
from_proj = CRS('epsg:4326')

# (very) rough bounding box for Addis Ababa
bbox = (9.089963, 38.653849, 8.822045, 38.898295)

scale_factor = 2

# Note: this is for the whole of Ethiopia
with rasterio.open('PopulationDensity2015EJRC/etnaejrcpopd2015.tif') as dataset:
    print('width', dataset.width)
    print('height', dataset.height)
    print('bounds', dataset.bounds)

    # Assume we're working with the first band
    index = dataset.indexes[0]

    # Get value that represents no data
    nodata = dataset.nodatavals[0]

    # Calculate the correct window based on the specified bounds
    # Helpful reference: <https://epsg.io/transform>
    to_proj = CRS(dataset.crs.to_string())
    transformer = Transformer.from_crs(from_proj, to_proj)
    lat0, lon0, lat1, lon1 = bbox
    x0, y0 = transformer.transform(lat0, lon0)
    x1, y1 = transformer.transform(lat1, lon1)
    py0, px0 = dataset.index(x0, y0)
    py1, px1 = dataset.index(x1, y1)
    w = px1 - px0
    h = py1 - py0
    window = Window(px0, py0, w, h)

    # Get data for the window
    data = dataset.read(index, window=window)

    # Convert to population per sqm
    data /= 5000

    # Save to a new file
    kwargs = dataset.meta.copy()
    kwargs.update({
        'height': window.height,
        'width': window.width,
        'transform': dataset.window_transform(window)
    })
    with rasterio.open(
            '/tmp/windowed.tif', 'w', **kwargs) as dst:
        dst.write(data, indexes=index)

# Load generated file
with rasterio.open('/tmp/windowed.tif') as dataset:
    index = dataset.indexes[0]

    # Re-sample if requested
    if scale_factor != 1:
        # Resampling methods: <https://rasterio.readthedocs.io/en/latest/api/rasterio.enums.html#rasterio.enums.Resampling>
        # More details: <https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/resample-function.htm>
        data = dataset.read(
            index,
            out_shape=(
                int(dataset.height * scale_factor),
                int(dataset.width * scale_factor)
            ),
            resampling=Resampling.bilinear
        )

        # scale image transform
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )
    else:
        data = dataset.read(index)
        transform = dataset.transform

    # Show data
    pyplot.imshow(data, cmap='pink')
    pyplot.show()

# This is for generating geojson features:
#     # Mask out no data areas
#     # mask = dataset.dataset_mask()

#     # Extract feature shapes and values from the array.
#     # for geom, val in rasterio.features.shapes(
#     #         mask, transform=dataset.transform):

#     # print('here')
#     # for geom, val in rasterio.features.shapes(
#     #         mask, transform=transform):
#         # import ipdb; ipdb.set_trace()
#         # print(val)

#         # Transform shapes from the dataset's own coordinate
#         # reference system to CRS84 (EPSG:4326).
#         # geom = rasterio.warp.transform_geom(
#         #     dataset.crs, 'EPSG:4326', geom, precision=6)

#         # Print GeoJSON shapes to stdout.
#         # print(geom)