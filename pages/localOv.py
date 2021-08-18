from imports import *

def local_overview(state):
    GLT = state.__getitem__('df')

    st.title(':house_with_garden: Local overview')

    justBegin = "<p style='text-align: justify;'> "
    justEnd = " </p>"

    mdown = 'Looks likes things are getting warmer. Despite the global overview shows the data of every country and continent in the globe, it laks a more deep analysis into each one of them.'
    mdown += ' So the local overview analysis has the intention to give a deep meaning about the climate change in a country/state/city level, allowing the viewer to focus in specific places such as his/her hometown. Fun is it not? Keep up with the analysis below and check for yourself.'
    st.markdown(justBegin+mdown+justEnd, unsafe_allow_html=True)

    st.header('Country analysis')

    st.header('State analysis')

    st.header('City analysis')