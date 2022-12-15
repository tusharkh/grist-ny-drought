import geopandas as gpd
import rioxarray as rxr

# plotting packages
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import rcParams

# get new york counties shapfiles and reproject
zipfile_counties = "/Users/tushar/Downloads/cb_2021_us_county_5m.zip"
counties = gpd.read_file(zipfile_counties)
counties = counties[counties['STATEFP'] == '36']
# reproject to us national atles equal area projections
counties = counties.to_crs(epsg=2163)

# upload raster data from PRSIM
july_30yr_file = "/Users/tushar/Downloads/PRISM_ppt_30yr_normal_4kmM3_07_bil/PRISM_ppt_30yr_normal_4kmM3_07_bil.bil"
june_30yr_file = "/Users/tushar/Downloads/PRISM_ppt_30yr_normal_4kmM3_06_bil/PRISM_ppt_30yr_normal_4kmM3_06_bil.bil"
july_2022_file = "/Users/tushar/Downloads/PRISM_ppt_provisional_4kmM3_202207_bil/PRISM_ppt_provisional_4kmM3_202207_bil.bil"
june_2022_file = "/Users/tushar/Downloads/PRISM_ppt_provisional_4kmM3_202206_bil/PRISM_ppt_provisional_4kmM3_202206_bil.bil"
july_30yr = rxr.open_rasterio(july_30yr_file, masked=True)
june_30yr = rxr.open_rasterio(june_30yr_file, masked=True)
july_2022 = rxr.open_rasterio(july_2022_file, masked=True)
june_2022 = rxr.open_rasterio(june_2022_file, masked=True)

# compute percent values
da = (june_2022 + july_2022) * 100 / (july_30yr + june_30yr)
da = da.rio.reproject(counties.crs)
#da = june_july_2022_percent.rio.reproject(da = june_july_2022_percent.rio.reproject(counties.crs))
da = da.rio.clip(counties.geometry, drop=True)
# clip nadata values
da = da.where(da < 500)

# plot
# Add every font at the specified location
font_dir = ['/Users/tushar/Library/Fonts']
for font in font_manager.findSystemFonts(font_dir):
    # use font_manager.FontProperties(fname=font).get_name() to get the name
    font_manager.fontManager.addfont(font)
    
# Set font family globally
rcParams['font.family'] = 'Open Sans'

# set global style parameters
rcParams['xtick.labelcolor'] = '#666666'
rcParams['ytick.labelcolor'] = '#666666'
rcParams['grid.color'] = '#ffffff'
rcParams['axes.facecolor'] = '#eeeeee'
rcParams['figure.facecolor'] = '#eeeeee'
rcParams['axes.labelcolor'] = '#666666'

fig, ax = plt.subplots(figsize=(15, 8))
da.plot(ax=ax, cmap='BrBG', add_colorbar=False)
ax.imshow(da[0,:, :], cmap='BrBG')
counties.plot(ax=ax, facecolor='none', linewidth=0.5)

ax.set_title('')
# clear spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticklabels('')
ax.set_yticklabels('')
ax.set_ylabel('')
ax.set_xlabel('')
ax.tick_params(left=False)
ax.tick_params(bottom=False)

ax.text(s='How Dry?', fontsize=30, y=1.11, x=-0.15, transform=ax.transAxes, fontweight=650)
ax.text(s='Percent of normal monthly precipitation,', fontsize=27, y=1.03, x=-0.15, transform=ax.transAxes, fontweight=350)
ax.text(s='New York, June-July 2022', fontsize=27, y=0.95, x=-0.15, transform=ax.transAxes, fontweight=350)

# caption
ax.text(s='Data Source: PRISM Climate Data /', fontsize=13, y=-0, x=-0.15, transform=ax.transAxes, fontweight=300)
ax.text(s='Northwest Alliance for Computational Science and Engineering / Oregon State University', fontsize=13, y=-0.04, x=-0.15, transform=ax.transAxes, fontweight=300)
ax.text(s='"Normal" refers to 1991-2020 average cumulative precipitation for June and July', style='italic', fontsize=13, y=-0.08, x=-0.15, transform=ax.transAxes, fontweight=300)

fig.savefig('ny-drought.jpg', bbox_inches='tight', pad_inches=0.3)