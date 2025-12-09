import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import ast

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv('data_viz1.xls')
wordcloud_df= pd.read_csv('wordcloud_df.xls')
feature_text = pickle.load(open('feature_text.pkl','rb'))


group_df = (
    new_df.groupby('location')[['price_in_crore','price_per_sqft','area','latitude','longitude']]
          .mean()
)

st.header('Location Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig, width='stretch')

# Wordcloud section
location_option = wordcloud_df['location'].unique().tolist()
location_option.insert(0, 'overall')

selected_location = st.selectbox('Select Location', location_option)

st.header('Features Wordcloud')

if selected_location == 'overall':
    # Overall wordcloud
    figure = WordCloud(width=800, height=800,
                       background_color='white',
                       stopwords=set(['s']),
                       min_font_size=10).generate(feature_text)
else:
    # Filter by location - use wordcloud_df instead of new_df
    filtered_df = wordcloud_df[wordcloud_df['location'] == selected_location]

    # Extract features from filtered data
    main = []
    for item in filtered_df['features'].dropna().apply(ast.literal_eval):
        main.extend(item)

    location_feature_text = ' '.join(main)

    if location_feature_text.strip():
        figure = WordCloud(width=800, height=800,
                           background_color='white',
                           stopwords=set(['s']),
                           min_font_size=10).generate(location_feature_text)
    else:
        st.warning(f"No features available for {selected_location}")
        figure = None
# Display wordcloud
if figure is not None:
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
    ax.imshow(figure, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)
else:
    st.error("Could not generate wordcloud")



    # Pass the figure to st.pyplot()


st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="area", y="price_in_crore", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, width='stretch')
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="area", y="price_in_crore", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, width='stretch')



st.header('BHK Pie Chart')


sector_options = new_df['location'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select location', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2,  width='stretch')
else:

    fig2 = px.pie(new_df[new_df['location'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, width='stretch')







st.header('Side by Side  price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price_in_crore', title='Price Range')

st.plotly_chart(fig3, width='stretch')

st.header('Side by Side histplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price_in_crore'] , kde =True, label='house')
sns.histplot(new_df[new_df['property_type'] == 'flat']['price_in_crore'] ,kde = True, label='flat')
plt.legend()
st.pyplot(fig3)