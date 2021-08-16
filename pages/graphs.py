from imports import *

@st.cache
def global_line_plot(df):
    fig = make_subplots(rows=2, cols=3, shared_xaxes=True, row_heights=[0.7, 0.3],
                        subplot_titles=('Land Avg. Temperature: 1750-2015', 'Land & Ocean Avg. Temperature: 1850-2015', 'Max-Min Land Temperature: 1850-2015',
                                        'Uncertainty', 'Uncertainty', 'Deviation'))

    # LAND
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAverageTemperature'])], 
                y=df['LandAverageTemperature'].dropna(), 
                name='Land Avg. Temp.',
                mode='lines',
                showlegend=True),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAverageTemperatureUncertainty'])], 
                y=df['LandAverageTemperatureUncertainty'].dropna(), 
                name='Land Avg. Temp. Error',
                mode='lines',
                showlegend=True),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAverageTemperature'])], 
                y=(df['LandAverageTemperature']+df['LandAverageTemperatureUncertainty']/2).dropna(), 
                name='upper bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAverageTemperature'])], 
                y=(df['LandAverageTemperature']-df['LandAverageTemperatureUncertainty']/2).dropna(), 
                name='lower bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                fillcolor='rgba(0,0,68, 0.2)',
                fill='tonexty',
                showlegend=False),
        row=1, col=1
    )
    # LAND AND OCEAN
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAndOceanAverageTemperature'])], 
                y=df['LandAndOceanAverageTemperature'].dropna(), 
                name='Land and Ocean Avg. Temp.',
                mode='lines',
                showlegend=True),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAndOceanAverageTemperatureUncertainty'])], 
                y=df['LandAndOceanAverageTemperatureUncertainty'].dropna(), 
                name='Land and Ocean Avg. Temp. Error',
                mode='lines',
                showlegend=True),
        row=2, col=2
    )

    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAndOceanAverageTemperature'])], 
                y=(df['LandAndOceanAverageTemperature']+df['LandAndOceanAverageTemperatureUncertainty']/2).dropna(), 
                name='upper bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandAndOceanAverageTemperature'])], 
                y=(df['LandAndOceanAverageTemperature']-df['LandAndOceanAverageTemperatureUncertainty']/2).dropna(), 
                name='lower bound',
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                fillcolor='rgba(0,0,68, 0.2)',
                fill='tonexty',
                showlegend=False),
        row=1, col=2
    )
    # MAX-MIN LAND
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandMaxTemperature'])], 
                y=df['LandMaxTemperature'].dropna(), 
                name='Land Max. Temp.',
                mode='lines',
                marker=dict(color="red"),
                line=dict(width=1.5),
                showlegend=True),
        row=1, col=3
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandMinTemperature'])], 
                y=df['LandMinTemperature'].dropna(),
                name='Land Min. Temp.',
                mode='lines',
                marker=dict(color="cyan"),
                line=dict(width=1.5),
                fillcolor='rgba(255,0,0, 0.2)',
                fill='tonexty',
                showlegend=True),
        row=1, col=3
    )
    fig.add_trace(
        go.Scatter(x=df['year'][pd.notnull(df['LandMaxTemperature'])], 
                y=(df['LandMaxTemperature']-df['LandMinTemperature']).dropna(), 
                name='Max-Min Land Temp. Deviation',
                mode='lines',
                showlegend=True),
        row=2, col=3
    )



    fig['layout']['yaxis1']['title']= 'Temperature (°C)'
    fig['layout']['yaxis4']['title']= 'Temperature (°C)'
    fig['layout']['xaxis1']['title']= 'Years'
    fig['layout']['xaxis2']['title']= 'Years'
    fig['layout']['xaxis3']['title']= 'Years'
    fig['layout']['xaxis4']['title']= 'Years'
    fig['layout']['xaxis5']['title']= 'Years'
    fig['layout']['xaxis6']['title']= 'Years'

    fig.update_layout(hovermode="x", height=500, width=1100, title='Change in global temperature across the years')
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=13,color='#000000')

    return fig

@st.cache
def countries_geo_plot(df, projection, scope):
    df = df.dropna(axis=0, how='any').reset_index()
    df = df.filter(['year','Country','AverageTemperature','Continent','alpha-3'])
    fig = px.choropleth(df, 
                    locations='alpha-3', 
                    color='AverageTemperature',
                    color_continuous_scale='rainbow',
                    scope=scope,
                    projection=projection,
                    labels={'AverageTemperature':'Average Temperature (°C)'},
                    title='Evolution of average temperature per country: 1743-2013',
                    width=700, height=500,
                    animation_frame='year',)
    return fig

@st.cache
def continents_mult_plot(df):
    df = df.groupby(['year','Continent']).mean().reset_index()
    df = df[df['year']>1890]
    continentsToSelect = df['Continent'].sort_values().unique()

    #fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
    fig = make_subplots(rows=6, cols=3, subplot_titles=('Avg. temperature with error', 'Increment in avg. temperature', 'Violin plot of avg. temperature'))

    for itr in range(len(continentsToSelect)):
        continent=continentsToSelect[itr]
        half_error = df['AverageTemperatureUncertainty'][df['Continent']==continent]/2
        avg_temp = df['AverageTemperature'][df['Continent']==continent]
        time_year = df['year'].unique()
        fig.add_trace(
            go.Scatter(x=time_year, 
                        y=avg_temp, 
                        name=continent + ' avg. temp.',
                        mode='lines',
                        legendgroup='group'+str(itr+1),
                        ),
            row=itr+1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=time_year,
                        y=avg_temp+half_error, 
                        name='upper bound',
                        mode='lines',
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        showlegend=False,
                        ),
            row=itr+1, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_year, 
                        y=avg_temp-half_error,
                        name='lower bound',
                        mode='lines',
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        fillcolor='rgba(0,0,68, 0.2)',
                        fill='tonexty',
                        showlegend=False),
            row=itr+1, col=1
        )
        fig.add_trace(
            go.Waterfall(x = time_year[1:],
                        y = np.diff(avg_temp),
                        name=continent + ' temperature increment',
                        legendgroup='group'+str(itr+1),
                        ),
            row=itr+1, col=2
        )
        fig.add_trace(
            go.Violin(y=avg_temp, 
                        name=continent + ' violin',
                        box_visible=True, 
                        meanline_visible=True, opacity=0.6,
                        x0=continent,
                        legendgroup='group'+str(itr+1)),
            row=itr+1, col=3
        )


    fig['layout']['yaxis1']['title']= 'Temperature (°C)'
    fig['layout']['yaxis4']['title']= 'Temperature (°C)'
    fig['layout']['yaxis7']['title']= 'Temperature (°C)'
    fig['layout']['yaxis10']['title']= 'Temperature (°C)'
    fig['layout']['yaxis13']['title']= 'Temperature (°C)'
    fig['layout']['xaxis1']['title']= 'Years'
    fig['layout']['xaxis2']['title']= 'Years'
    fig['layout']['xaxis4']['title']= 'Years'
    fig['layout']['xaxis5']['title']= 'Years'
    fig['layout']['xaxis7']['title']= 'Years'
    fig['layout']['xaxis8']['title']= 'Years'
    fig['layout']['xaxis10']['title']= 'Years'
    fig['layout']['xaxis11']['title']= 'Years'
    fig['layout']['xaxis13']['title']= 'Years'
    fig['layout']['xaxis14']['title']= 'Years'


    fig.update_layout(height=1400, width=1000, title='Change in continents average temperature across the years: 1900-2010',
                    legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=0,
                                xanchor="center",
                                x=0.5)
    )
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=14,color='#000000')
    #fig.show()
    return fig

def global_overview(state):
    

    GLT = state.__getitem__('df')

    st.title(':airplane: Global overview')

    justBegin = "<p style='text-align: justify;'> "
    justEnd = " </p>"

    mdown = 'In this page the analysis has a larger scope encompassing the whole earth, ocean and the countries temperatures. '
    mdown += 'Once the datasets have data between months, turns out to be impractical and a poor practic considering the design of the plots to show th data per month. '
    mdown += 'So the data in the used data frames was grouped by year and a mean with the monthly values of quantitatives features was applied to achieve an average value by year.'
    st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

    st.header('Global land and ocean temperatures')
    mdown = 'This section presents plots using the ```GlobalTemperatures``` dataset that gathers information about the temperatures regarding the whole planet.'
    st.markdown(mdown, unsafe_allow_html=True)



    graph1 = st.container()
    graph1.write(global_line_plot(GLT['glt'].copy())) # global line plot

    mdown1 = 'Regarding the land average temperature, due to its high uncertainty in the measures in the early years'
    mdown1 += 'the data cannot assure a potential rise in the temperature until the 20th century. '
    mdown1 += 'After that the rise in the average land temperature turns out to be clear.'
    mdown2 = 'Considering the land and ocean average temperature, even with the high uncertainty in the early years, it turns out to'
    mdown2 += ' show a more clear rising behavior with two knees, one in the beggining of the 20th and other after the WWII period.'
    mdown3 = 'Now looking for maximum and minimum land temperature measured in the globe the rising in both is pretty clear,'
    mdown3 += ' mantaining the same rising behaviour without further sudden changes in the gradient.'
    mdown3 += ' Along this the deviation between those values tends to drop and once both min. and max. temperatures are rising'
    mdown3 += ', it means that the min. temperatures is rising with higher rate.'

    colSize = 5.4
    _, col1, col2, col3, _ = st.columns([1,colSize,colSize,colSize,4])
    with col1: 
        st.subheader('About the land avg. temperature')
        st.markdown(justBegin+mdown1+justEnd, unsafe_allow_html=True)
    with col2: 
        st.subheader('About the land & ocean avg. temperature')
        st.markdown(justBegin+mdown2+justEnd, unsafe_allow_html=True)
    with col3: 
        st.subheader('About the max & min land temperature')
        st.markdown(justBegin+mdown3+justEnd, unsafe_allow_html=True)

    st.header('Continents e countries temperatures')
    mdown = 'This section presents plots using the ```GlobalLandTemperaturesByCountry``` dataset that gathers information about the temperatures in countries.'
    st.markdown(mdown, unsafe_allow_html=True)
    mdown = 'The dataframes only show data about the countries, but with the name of the country the continent of origin can be easily traced with the ```Continents2``` dataframe. So the data can be processed and visualized as below.'
    st.markdown(mdown, unsafe_allow_html=True)
    
    st.subheader('Continents')
    mdown = 'The continents data was generated grouping the countries by the respective region. Once group a mean was taken to reproduce the average temperature and with the uncertainty some plots was generated:'
    mdown += '\n\n - Scatter plot to show the avg. temperature with the error in the measures (that drops with the time and increase in recording technology);'
    mdown += '\n\n - Waterffal chart showing the increase in the average temperatura;'
    mdown += '\n\n - Violin plot to show essential statistics for all the data gathered across the years.'
    st.markdown(mdown, unsafe_allow_html=True)
    graph = st.container()
    graph.write(continents_mult_plot(GLT['country'].copy())) # continents mult plot

    st.subheader('Countries temperatures')
    mdown = 'Some data from in the plots below are missing. This is explained considering that some countries only start to record its data further in time. '
    mdown += ' In the line plots there will be discontinuities and blank spaces in between the missing data, but in the geographical plot there will be any color for these missing data. '
    mdown += ' No imputation was used in the data just to have the raw value of each year.'
    st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

    graph2, graph3 = st.columns([1.8,1])
    config1, config2 = st.columns([2,1])
    
    
    with config1:
        with st.expander(label='Choropleth geographical plot configuration', expanded=True):
            st.markdown('Those two select box allow to configure the choropleth graph below by selecting a projection type and/or setting a socpe in one of the continents.')
            projections = ['natural earth', 'orthographic', 'equirectangular', 'mercator', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'winkel tripel', 'aitoff', 'sinusoidal'] # there is no 'albers usa'
            projection = st.selectbox("Select a projection type:", options=projections)
            scopes = ['world', 'europe', 'asia', 'africa', 'north america','south america'] # there is no 'usa'
            scope = st.selectbox("Select a scope in one continent:", options=scopes)

    df = GLT['country'].copy()
    graph2.write(countries_geo_plot(df, projection, scope))

    continentsToSelect = df['Continent'].dropna().sort_values().unique()
    
    with config2:
        with st.expander(label='Line plot configuration', expanded=True):
            st.markdown('The two multiselections below allow to select continents and its countries to plot a line chart with the tendency of the countries average temepratures across the years. Only available data is shown.')
            selectedContinent = st.multiselect('Select continents:', continentsToSelect, continentsToSelect[0])
            countriesToSelect = df['Country'][df['Continent'].isin(selectedContinent)].sort_values().unique()
            with st.form("Plot line chart"):
                selectedCountries = st.multiselect('Select countries:', countriesToSelect, countriesToSelect[0:4])
                submitted = st.form_submit_button("Plot")

    #if submitted:
        fig = px.line(df[df['Country'].isin(selectedCountries)], 
                    x='year', y='AverageTemperature', color='Country', 
                    title='Tendency of average temperature per country', width=500, height=520)
                    
        fig.update_xaxes(title='Years')
        fig.update_yaxes(title='Average Temperature (°C)')
        #fig.show()
        graph3.write(fig)


    
