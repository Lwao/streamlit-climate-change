from imports import *

def latlon2gedree(str_):
    # example: str_ = '20.21N'
    numb = float(str_[:-1])
    dir = str_[-1]
    if dir in ('S','W'): numb *=-1
    return numb

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
    fig = px.density_mapbox(df.rename(columns={'AverageTemperature':'Average temperature (°C)'}), 
                        lat='Latitude', lon='Longitude', z='Average temperature (°C)', 
                        center=dict(lat=0, lon=180), zoom=0,
                        radius=10, animation_frame='year',
                        mapbox_style=stt, 
                        width=1100, height=600, title='Average temperature distributed according to latitude and longitude')      

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
        continents = GLT['country']['Continent'].dropna().sort_values().unique()
        continent = st.selectbox('Select a continent:', continents)
        countries = GLT['city']['Country'][GLT['city']['Continent']==continent].dropna().sort_values().unique()
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

    col1, col2 = st.columns([2,1])

    with col1:
        st.write(line_plot_state(GLT['state'].copy(), states))

    with col2: 
        df = GLT['state'].copy()
        ano = st.select_slider('Escolha o ano:', df['year'], 2000)
        title = 'States average temperature in year ' + str(ano)
        df = df[(df['Country']==country) & (df['year']==ano)]

        fig = px.sunburst(df, names='State', parents='Country', 
                        values='AverageTemperature', 
                        width=400, height=400, 
                        title=title)
        st.write(fig)

    st.header(':car: City analysis')

    st.markdown('Considering the latitude and longitude of each city, we can plot a density mapbox along the geographical position of each city on earth acros time, resulting in the plot below.')

    graph = st.container()
    with graph: 
        with st.expander(label='Select mapbox style', expanded=False):
            stss = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen- terrain', 'stamen-toner', 'stamen-watercolor'] 
            stt = st.selectbox(" ", options=stss)
        st.write(mapbox_plot(GLT['city'], stt))