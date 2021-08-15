from imports import *


@st.cache
def load_dataframes():
    #download dataset
    url = 'https://drive.google.com/uc?id=1ssdRWFu3A6z1jFlByX4hP6qtzWH8U9ez'
    out = './dataset.zip'
    gdown.download(url, out, quiet=False)

    # unzip dataset
    zip_ref = zf.ZipFile('./dataset.zip', 'r')
    zip_ref.extractall('dataset')
    zip_ref.close()

    # load dataframes
    df = {}
    df['city']       = pd.read_csv('dataset/GlobalLandTemperaturesByCity.csv')
    df['country']    = pd.read_csv('dataset/GlobalLandTemperaturesByCountry.csv')
    df['state']      = pd.read_csv('dataset/GlobalLandTemperaturesByState.csv')
    df['glt']        = pd.read_csv('dataset/GlobalTemperatures.csv')
    df['continents'] = pd.read_csv('dataset/continents.csv')

    # clean dataframes
    for actual_df in ['df','city','state','country']:
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
        st.title(':earth_americas: Is climate change real?')
        st.markdown('Some people believe that climate change is not real, some believe that is. Who shall we trust? I do not know, so let the data speak for itself.')
        

    with about:
        st.header('About the data')

        df = load_dataframes()

        st.markdown('So keep up with the side bar pages and analyze the data as you wish')
    
    state.__setitem__('df',df)
    
    return state



