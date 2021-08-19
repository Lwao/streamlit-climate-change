from imports import *


@st.cache(allow_output_mutation=True)
def load_dataframes():
    #"""
    #download dataset
    url = 'https://drive.google.com/uc?id=1ssdRWFu3A6z1jFlByX4hP6qtzWH8U9ez'
    out = './dataset.zip'
    gdown.download(url, out, quiet=False)

    # unzip dataset
    zip_ref = zf.ZipFile('./dataset.zip', 'r')
    zip_ref.extractall('dataset')
    zip_ref.close()
    #"""
    # load dataframes
    df = {}
    df['city']       = pd.read_csv('dataset/GlobalLandTemperaturesByCity.csv')
    df['country']    = pd.read_csv('dataset/GlobalLandTemperaturesByCountry.csv')
    df['state']      = pd.read_csv('dataset/GlobalLandTemperaturesByState.csv')
    df['glt']        = pd.read_csv('dataset/GlobalTemperatures.csv')
    df['continents'] = pd.read_csv('dataset/continents.csv')

    # clean dataframes
    for actual_df in ['glt','city','state','country']:
        df[actual_df]['dt'] = pd.to_datetime(df[actual_df]['dt']) # convert dates to datetime format
        df[actual_df]['year'] = df[actual_df]['dt'].dt.year # extract year of each row

    # group numeric data by year
    df['glt'] = df['glt'].groupby(['year']).mean().reset_index()
    df['country'] = df['country'].groupby(['year','Country']).mean().reset_index()
    df['state'] = df['state'].groupby(['year', 'State', 'Country']).mean().reset_index()
    df['city'] = df['city'].groupby(['year', 'City', 'Country', 'Latitude', 'Longitude']).mean().reset_index()

    # extract geographic information from countries
    df['continents'] = df['continents'].filter(['name', 'region', 'alpha-2', 'alpha-3']).rename({'name':'Country', 'region':'Continent'}, axis=1)

    # append geography information to each dataframe
    for actual_df in ['city','state','country']: df[actual_df] = pd.merge(left=df[actual_df], right=df['continents'], on='Country', how='left')

    return df

def app(state):

    header = st.container()
    about = st.container()

    with header:
        st.image('images/cover.png')
        st.text('Source: NY times.')
        st.title(':earth_americas: Is climate change real?')
        st.markdown('Some people believe that climate change is not real, some believe that is. Who shall we trust? In case of doubt, let the data speak for itself.')
        

    with about:
        st.header(':chart_with_upwards_trend: About the data')

        df = load_dataframes()
        

        justBegin = "<p style='text-align: justify;'> "
        justEnd = " </p>"

        mdown = 'The data used in this web application comes from a Kaggle dataset of <a href="https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data">"Climate Change: Earth Surface Temperature Data"</a>. '
        mdown += 'Even thought the data comes from <a href="http://berkeleyearth.org/about/">Berkeley Earth</a>, the Kaggle dataset consists in a repackaged e newly compiled version of these data. '
        mdown += '"The Berkeley Earth Surface Temperature Study combines 1.6 billion temperature reports from 16 pre-existing archives. It is nicely packaged and allows for slicing into interesting subsets (for example by country). They publish the source data and the code for the transformations they applied. They also use methods that allow weather observations from shorter time series to be included, meaning fewer observations need to be thrown away". Source: Kaggle.'
        st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

        mdown = 'Raw data source: <a href="http://berkeleyearth.org/data/">Berkeley Earth data page</a>,'
        st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

        mdown = 'To complement the use of the previous datasets, another Kaggle dataset named <a href="https://www.kaggle.com/andradaolteanu/country-mapping-iso-continent-region">Country Mapping - ISO, Continent, Region</a> was used to address each country its geographical data such as ISO code, continent and region. ' 
        mdown += 'Further will be discussed the features of each dataset in details, but the complementary dataset will ensure a better visualization of the evolution of temperature in each country, state and city with a plot in a geographical map.'
        st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

        st.subheader('Dataset files and features:')

        mdown = '- ```GlobalTemperatures.csv``` Global Land and Ocean-and-Land Temperatures;\n'
        mdown += '  - **dt** timestamp information when the data was registered;\n'
        mdown += '  - **LandAverageTemperature** global average land temperature in celsius;\n'
        mdown += '  - **LandAverageTemperatureUncertainty** the 95% confidence interval around the average;\n'
        mdown += '  - **LandMaxTemperature** global average maximum land temperature in celsius;\n'
        mdown += '  - **LandMaxTemperatureUncertainty** the 95% confidence interval around the maximum land temperature;\n'
        mdown += '  - **LandMinTemperature** global average minimum land temperature in celsius;\n'
        mdown += '  - **LandMinTemperatureUncertainty** the 95% confidence interval around the minimum land temperature;\n'
        mdown += '  - **LandAndOceanAverageTemperature** global average land and ocean temperature in celsius;\n'
        mdown += '  - **LandAndOceanAverageTemperatureUncertainty** the 95% confidence interval around the global average land and ocean temperature;\n'
        
        mdown += '- ```GlobalLandTemperaturesByCountry.csv``` Global Average Land Temperature by Country;\n'
        mdown += '  - **dt** timestamp information when the data was registered;\n'
        mdown += '  - **AverageTemperature** global average temperature in celsius;\n'
        mdown += '  - **AverageTemperatureUncertainty** the 95% confidence interval around the average;\n'
        mdown += '  - **Country** country where the measures was taken;\n'

        mdown += '- ```GlobalLandTemperaturesByState.csv``` Global Average Land Temperature by State;\n'
        mdown += '  - **dt** timestamp information when the data was registered;\n'
        mdown += '  - **AverageTemperature** global average temperature in celsius;\n'
        mdown += '  - **AverageTemperatureUncertainty** the 95% confidence interval around the average;\n'
        mdown += '  - **State** state where the measures was taken;\n'
        mdown += '  - **Country** country where the measures was taken;\n'

        mdown += '- ```GlobalLandTemperaturesByCity.csv``` Global Land Temperatures By City;\n'
        mdown += '  - **dt** timestamp information when the data was registered;\n'
        mdown += '  - **AverageTemperature** global average temperature in celsius;\n'
        mdown += '  - **AverageTemperatureUncertainty** the 95% confidence interval around the average;\n'
        mdown += '  - **City** city where the measures was taken;\n'
        mdown += '  - **Country** country where the measures was taken;\n'
        mdown += '  - **Latitude** geographical latitude of the city in analysis;\n'
        mdown += '  - **Longitude** geographical longitude of the city in analysis;\n'

        mdown += '- ```continents2.csv``` Country Mapping - ISO, Continent, Region: complementary dataset with data regarding continents geographical position;\n'
        mdown += '  - **name** country name;\n'
        mdown += '  - **alpha-2** 2 letters ISO code;\n'
        mdown += '  - **alpha-3** 3 letters ISO code to use in Plotly;\n'
        mdown += '  - **country-code** unique country code;\n'
        mdown += '  - **iso_3166-2** ISO-3166-2 code;\n'
        mdown += '  - **region** continent;\n'
        mdown += '  - **sub-region** subcontinent;\n'
        mdown += '  - **intermediate-region** ;\n'
        mdown += '  - **region-code**, **sub-region-code**, **intermediate-region-code** regions code ;\n'
        
        st.markdown(mdown)

        st.subheader('Libraries used:')
        mdown = '- ```numpy``` for easy array manipulation;\n'
        mdown += '- ```pandas``` to deal with data frames manipulation;\n'
        mdown += '- ```plotly ``` for interactive data visualization;\n'
        mdown += '  - ```plotly.express``` module for quick graphs;\n'
        mdown += '  - ```plotly.graph_objects``` module to create complexs and custom graphs;\n'
        mdown += '  - ```plotly.subplots``` module to allow multiple plts in a single figure;\n'
        mdown += '  - ```plotly.figure_factory``` module to create figures;\n'
        mdown += '- ```datetime``` to deal with dates in a timestamp format;\n'
        mdown += '- ```streamlit``` high level API to deploy web applications with Python;\n'
        mdown += '- ```gdown``` to download data from Google Drive;\n'
        mdown += '- ```zipfile``` to extract files from compressed formats;\n'
        st.markdown(mdown)

        st.markdown('Keep up with the sidebar pages and analyze the data as you wish and formulate your own opinion.')
    
    state.__setitem__('df',df)

    return state



