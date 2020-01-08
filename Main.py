





import geopandas as gpd
import requests








if __name__== "__main__":



    shapefile = '/Users/rubenperezibanez/PycharmProjects/GeoreferenciaMundo/test/ne_110m_admin_0_countries.shp'
    # Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    # Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']
    print(gdf.head())

    print(gdf[gdf['country'] == 'Antarctica'])
    # Drop row corresponding to 'Antarctica'
    gdf = gdf.drop(gdf.index[159])

    import pandas as pd

    datafile = 'test/ESPERANZA.csv'
    # Read csv file using pandas
    df = pd.read_csv(datafile, sep=",")

    df = df.melt(id_vars=["Country Name","Country Code","Indicator Name","Indicator Code"],
            var_name="year",
            value_name="Value")

    print(df.head())

    print(df.info())

    df = df.drop(columns=["Indicator Name","Indicator Code"])

    df[df['Country Code'].isnull()]

    # Filter data for year 2016.
    df_2016 = df[df['year'] == "2016"]
    df_2016["original"]=  df_2016["Value"]


    df_2016["Value"]= ((df_2016["Value"] - min(df_2016["Value"])) * 100) / (max(df_2016["Value"]) - min(df_2016["Value"]))



    # Merge dataframes gdf and df_2016.
    merged = gdf.merge(df_2016, left_on='country_code', right_on='Country Code')

    import json

    # Read data to json.
    merged_json = json.loads(merged.to_json())
    # Convert to String like object.
    json_data = json.dumps(merged_json)


    from bokeh.io import output_notebook, show, output_file
    from bokeh.plotting import figure
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, \
    LogTicker, FixedTicker, FuncTickFormatter
    from bokeh.palettes import brewer
    from bokeh.models import PrintfTickFormatter

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 100)

    #Define custom tick labels for color bar.

    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
    tick_labels = {}
    cont=0;

    for i in list(range(int(min(df_2016["original"])), int(max(df_2016["original"])),int((max(df_2016["original"])-min(df_2016["original"]))//8))):
        tick_labels[cont]=str(i)
        cont = cont + 12.5
    print(tick_labels)


    # Create color bar.


    ticker = FixedTicker(ticks=[0,12.5, 25, 37.5, 50, 62.5, 75,87.5,100])
    data= {0: '51', 12.5: '55', 25: '59', 37.5: '63', 50: '67', 62.5: '71', 75: '75', 87.5: '79', 100: '83'}




    color_bar = ColorBar(color_mapper=color_mapper,

                         border_line_color=None, location=(0, 0),
                         orientation='horizontal', ticker= ticker,major_label_overrides = data,


                    major_label_text_font_size='10pt', label_standoff=7)

    
    
    

    p = figure(title = 'Esperanza da vida, 2016', plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure.
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'Value', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify figure layout.
    p.add_layout(color_bar, 'below')

    #Display figure.
    show(p)


