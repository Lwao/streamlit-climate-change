# Objetivos


Análise por:
- Globo
- Continentes
- Países
- Estados
- Cidades
  https://gist.github.com/rxaviers/7360908
- https://docs.streamlit.io/en/stable/api.html
- https://www.kaggle.com/andradaolteanu/country-mapping-iso-continent-region
- https://www.kaggle.com/andradaolteanu/plotly-advanced-global-warming-analysis
- https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data

# Data frames

1. **city** (459.2MB)

```
dt : timestamp                    
AverageTemperature          
AverageTemperatureUncertainty 
City                        
Country                        
Latitude                      
Longitude 
```

1. **country** (17.6MB)

```
dt : timestamp                    
AverageTemperature          
AverageTemperatureUncertainty                         
Country
```

3. **major_city** (12.8MB)

```
dt : timestamp                    
AverageTemperature          
AverageTemperatureUncertainty 
State                     
Country     
```

4. **state** (24.6MB)

```
dt : timestamp                    
AverageTemperature          
AverageTemperatureUncertainty 
State                    
Country                        
```

5. **glt** (224.6kB)

```
dt : timestamp                    
LandAverageTemperature
LandAverageTemperatureUncertainty
LandMaxTemperature 
LandMaxTemperatureUncertainty
LandMinTemperature
LandMinTemperatureUncertainty
LandAndOceanAverageTemperature
LandAndOceanAverageTemperatureUncertainty
``` 

# Abordagem

## *glt*

- Visão geral sobre os aspectos de temperatura na Terra;
- Gráficos:
  -  *Scatter* para valores médios com incerteza;
  -  *Gauge chart* para mostrar os valores médios evoluindo no tempo
  -  *Filled Area Plots* para os valores máximos e mínimos

Os dados serão analisados durante os anos, portanto os dados referentes aos meses passarão por uma média para obter o valor médio anual daquela grandeza.


# Links

- https://plotly.com/python/
- https://plotly.com/python/continuous-error-bars/
- https://plotly.com/python/mixed-subplots/
- https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html
- https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Scattergeo.html
- https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo

https://plotly.com/python/maps/

https://plotly.com/python/choropleth-maps/

https://plotly.com/python/map-configuration/

https://stackoverflow.com/questions/64428096/plotly-how-to-set-individual-color-for-each-y-error-bar-using-go-figure-and-go

https://www.geeksforgeeks.org/create-error-bars-in-plotly-python/

https://plotly.com/python/continuous-error-bars/

https://plotly.com/python/error-bars/

https://plotly.com/python/gauge-charts/

https://plotly.com/python/line-charts/

https://plotly.com/python/indicator/

https://plotly.com/python/animations/

https://plotly.com/python/sunburst-charts/