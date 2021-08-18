# Is climate change real?

This repository hosts a streamlit app that analyze climate change data in the effort to generate good visualizations about the increase in the world temperature at different levels:

- Global;
- Continent;
- Country;
- State;
- City;

## Data frames

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

## Links

- Cover image source: [NY times](https://www.nytimes.com/interactive/2019/04/30/dining/climate-change-food-eating-habits.html?mtrref=www.google.com.br&gwh=5DCD4703C1C8C68507FB492B4CFA62DA&gwt=pay&assetType=PAYWALL)
- [Country mapping dataset](https://www.kaggle.com/andradaolteanu/country-mapping-iso-continent-region)
- [Climate change dataset](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
- [Notebook from Kaggle with initial analyses in the data](https://www.kaggle.com/andradaolteanu/plotly-advanced-global-warming-analysis)
- [Emojis](https://gist.github.com/rxaviers/7360908)
- [Streamlit documentation](https://docs.streamlit.io/en/stable/api.html)
- [Plotly documentation for Python](https://plotly.com/python/)

