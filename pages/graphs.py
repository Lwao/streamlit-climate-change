from imports import *

def global_overview(state):
    graph1 = st.container()
    graph2 = st.container()
    graph3 = st.container()

    GLT = state.__getitem__('df')

    df = GLT['glt'].copy()

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

    fig.update_layout(hovermode="x", height=500, width=1200, title='Change in global temperature across the years')
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=14,color='#000000')
    
    #fig.show()
    graph1.write(fig)

    df = GLT['country'].copy()
    df = df.dropna(axis=0, how='any').reset_index()
    df = df.filter(['year','Country','AverageTemperature','Continent','alpha-3'])

    fig = px.choropleth(df, 
                    locations='alpha-3', 
                    color='AverageTemperature',
                    color_continuous_scale='rainbow',
                    scope='world',
                    projection='natural earth',
                    #projection='orthographic',
                    labels={'AverageTemperature':'Average Temperature (°C)'},
                    title='Evolution of countries average temperature: 1743-2013',
                    width=800, height=600,
                    animation_frame='year',)
    #fig.show()
    graph2.write(fig)

    fig = px.choropleth(df, 
                    locations='alpha-3', 
                    color='AverageTemperature',
                    color_continuous_scale='rainbow',
                    scope='world',
                    #projection='natural earth',
                    projection='orthographic',
                    labels={'AverageTemperature':'Average Temperature (°C)'},
                    title='Evolution of countries average temperature: 1743-2013',
                    width=800, height=600,
                    animation_frame='year',)
    fig.show()
    graph3.write(fig)