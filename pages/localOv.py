from imports import *

def latlon2gedree(str_):
    # example: str_ = '20.21N'
    numb = float(str_[:-1])
    dir = str_[-1]
    if dir in ('S','W'): numb *=-1
    return numb

@st.cache
def map_plot(df):
    if(df.dtypes['Latitude']=='O'): df['Latitude'] = df['Latitude'].apply(latlon2gedree)
    if(df.dtypes['Longitude']=='O'): df['Longitude'] = df['Longitude'].apply(latlon2gedree)
    map = st.map(df.rename(columns={'Latitude':'lat','Longitude':'lon'}))
    return map
@st.cache
def line_plot_state(df, states):
    fig = go.Figure()
    for choice in states:
        fig.add_trace(
            go.Scatter(x=df.year[df['State']==choice], y=df.AverageTemperature[df['State']==choice], name=choice,
            mode='lines', showlegend=True)
        )
    fig.update_xaxes(title='Years')
    fig.update_yaxes(title='Average Temperature (°C)')
    fig.update_layout(width=700, height=600, title='Average temperature in each state')
    fig.update_layout(
                        xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(step="all"),
                                    dict(count=113,
                                        label="1900",
                                        step="year",
                                        stepmode="backward")                                        
                                ])
                            ),
                            rangeslider=dict(
                                visible=True
                            ),
                            type="date"
                        )
                    )
    return fig

@st.cache
def mapbox_plot(df, stt='open-street-map'):
    if(df.dtypes['Latitude']=='O'): df['Latitude'] = df['Latitude'].apply(latlon2gedree)
    if(df.dtypes['Longitude']=='O'): df['Longitude'] = df['Longitude'].apply(latlon2gedree)

    fig = px.density_mapbox(df.rename(columns={'AverageTemperature':'Average temperature (°C)'})[np.mod(df['year'],10)==0], 
                        lat='Latitude', lon='Longitude', z='Average temperature (°C)', 
                        center=dict(lat=0, lon=180), zoom=0,
                        radius=10, animation_frame='year',
                        mapbox_style=stt, 
                        width=1100, height=600, title='Average temperature distributed according to latitude and longitude')      

    return fig

def city_line_plot(df, city):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3],
                            subplot_titles=('Avg. temperature', 'Uncertainty'))

    fig.add_trace(
        go.Scatter(x=df['year'], 
                y=df['AverageTemperature'], 
                name='Avg. Temp.',
                mode='lines',
                showlegend=False), row=1,col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'], 
                y=df['AverageTemperatureUncertainty'], 
                name='Error in Avg. Temp.',
                mode='lines',
                showlegend=False), row=2,col=1
    )

    fig.add_trace(
        go.Scatter(x=df['year'], 
                y=df['AverageTemperature']+df['AverageTemperatureUncertainty']/2, 
                name='upper bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False), row=1,col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'], 
                y=df['AverageTemperature']-df['AverageTemperatureUncertainty']/2,
                name='lower bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                fillcolor='rgba(0,0,68, 0.2)',
                fill='tonexty',
                showlegend=False), row=1,col=1
    )

    fig.update_layout(hovermode="x", height=400, width=400, title='Average temperature in ' + city)
    fig.update_xaxes(title='Years')
    fig.update_yaxes(title='Temperature (°C)')

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=13,color='#000000')

    return fig

def local_overview(state):
    GLT = state.__getitem__('df')

    st.title(':house_with_garden: Local overview')

    justBegin = "<p style='text-align: justify;'> "
    justEnd = " </p>"

    mdown = 'Looks likes things are getting warmer. Despite the global overview shows the data of every country and continent in the globe, it laks a more deep analysis into each one of them.'
    mdown += ' So the local overview analysis has the intention to give a deep meaning about the climate change in a state/city level, allowing the viewer to focus in specific places such as his/her hometown. Fun is it not? Keep up with the analysis below and check for yourself.'
    st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

    st.markdown('Allow yourself to select a specific location that you bear in mind. Perhaps the place you were born? Or were you lives now? Let us filter your choice.')
        
    """
    with st.form(key="Select a location"):
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            continents = GLT['country']['Continent'].dropna().sort_values().unique()
            continent = st.selectbox('Select a continent:', continents)
        with col2:
            countries = GLT['city']['Country'][GLT['city']['Continent']==continent].dropna().sort_values().unique()
            country = st.selectbox('Select a country:', countries)
        with col3:
            states = GLT['state']['State'][GLT['state']['Country']==country].dropna().sort_values().unique()
            state = st.selectbox('Select a state:', states)
        with col4:
            cities = GLT['city']['City'][GLT['city']['Country']==country].dropna().sort_values().unique()
            city = st.selectbox('Select a city:', cities)
        submitted = st.form_submit_button("Confirm")
    """

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        continents = list(GLT['country']['Continent'].dropna().sort_values().unique())
        continents.remove('Americas')
        continents.insert(0, 'Americas')
        continent = st.selectbox('Select a continent:', continents)
        countries = list(GLT['city']['Country'][GLT['city']['Continent']==continent].dropna().sort_values().unique())
        if(continent=='Americas'): 
            countries.remove('Brazil')
            countries.insert(0, 'Brazil')
        country = st.selectbox('Select a country:', countries)
    with col2:
        with st.form(key="Select a state"):
            states = GLT['state']['State'][GLT['state']['Country']==country].dropna().sort_values().unique()
            state = st.selectbox('Select a state:', states)
            st.form_submit_button("Confirm")
    with col3:
        with st.form(key="Select a city"):
            cities = GLT['city']['City'][GLT['city']['Country']==country].dropna().sort_values().unique()
            city = st.selectbox('Select a city:', cities)
            st.form_submit_button("Confirm")

    st.markdown('<p style="color:Red; font-size: 10px;">Obs.: in the actual version of this dashboard, it does not allow to fetch a city filter by its state, so it has to be fetched by the country.</p>', unsafe_allow_html=True)

    #st.header(':bus: Country analysis')

    st.header(':bus: State analysis')

    st.markdown('In the state analysis we are using the follow graphs:')
    st.markdown('- **Scatter plot** with lines to show the evolution of temperature in each state;')
    st.markdown('- **Sunburst chart** with the country as a parent and the states as its children to show a geometrical comparison between the temperatures of each state in a given year.')

    col1, col2 = st.columns([2,1])

    with col1:
        st.write(line_plot_state(GLT['state'].copy(), states))

    with col2: 
        df = GLT['state'].copy()
        ano = st.select_slider('Choose the year:', df['year'], 2000)
        title = 'States average temperature in year ' + str(ano)
        df = df[(df['Country']==country) & (df['year']==ano)]

        fig = px.sunburst(df, names='State', parents='Country', 
                        values='AverageTemperature', 
                        width=400, height=400, 
                        title=title)
        st.write(fig)

    st.header(':car: City analysis')

    st.markdown('Considering the latitude and longitude of each city, we can plot a **density mapbox** along the geographical position of each city on earth acros time, resulting in the plot below.')

    graph = st.container()
    with graph: 
        with st.expander(label='Select mapbox style', expanded=False):
            stss = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen- terrain', 'stamen-toner', 'stamen-watercolor'] 
            stt = st.selectbox(" ", options=stss)
        st.write(mapbox_plot(GLT['city'], stt))

    st.markdown('But what you are looking for is your city. To the data related to the city of choice it will be used couple graphics:')
    st.markdown('- **Line plot** to show a curve of the temperature of the city and its uncertainty;')
    st.markdown('- **Box plot** to clarify about the statistics in that city;')
    st.markdown('- **Dist plot** been a histogram with a rug and the probability density function of the data.')

    col1, col2, col3 = st.columns([1,1,1])

    df = GLT['city'][GLT['city']['City']==city].dropna().copy()
    with col1: st.write(city_line_plot(df, city))
    with col2: 
        st.write(
            px.box(
                df.rename(columns={'AverageTemperature':'Average temperature (°C)'}), 
                x='City', y='Average temperature (°C)', 
                points='all', title='Statistics of temperature in ' + city,
                width=350, height=400
                )
        )
    with col3:
        fig = ff.create_distplot([df['AverageTemperature']], [city], bin_size=.2, show_rug=True)
        fig.update_layout(width=400, 
                        height=400,
                        bargap=0.01)
        fig.update_xaxes(title='Temperature (°C)')
        fig.update_layout(title='Distribution of temperature in ' + city, showlegend=False)
        st.write(fig)

