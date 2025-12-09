import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.set_page_config(
    page_title="RealEstatePro - Smart Property Management",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    /* Main Colors */
    :root {
        --primary-color: #1a3a52;
        --secondary-color: #d4af37;
        --accent-color: #2c5aa0;
        --light-bg: #f8f9fa;
        --text-dark: #1a1a1a;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Sidebar styling */
    .css-1d58c45 {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
    }

    /* Title styling */
    h1, h2, h3 {
        color: #1a3a52;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
        padding: 60px 40px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    .hero-section h1 {
        color: white;
        font-size: 3.5em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .hero-section p {
        color: #d4af37;
        font-size: 1.3em;
        margin-bottom: 20px;
    }

    /* Header Section for other pages */
    .header-section {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
        padding: 40px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    .header-section h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
    }

    .header-section p {
        color: #d4af37;
        font-size: 1.1em;
        margin: 10px 0 0 0;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 8px;
        border-left: 5px solid #d4af37;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 15px 0;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .feature-card h3 {
        color: #1a3a52;
        margin-top: 0;
    }

    .feature-card p {
        color: #555;
        line-height: 1.6;
    }

    /* Stats section */
    .stat-box {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
        color: white;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .stat-number {
        font-size: 2.5em;
        font-weight: 700;
        color: #d4af37;
        margin: 10px 0;
    }

    .stat-label {
        font-size: 1em;
        color: #e8e8e8;
    }

    /* Form Container */
    .form-container {
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 30px;
        border-top: 5px solid #d4af37;
    }

    /* Section Headers */
    .section-header {
        color: #1a3a52;
        font-weight: 700;
        font-size: 1.3em;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #d4af37;
    }

    /* Result Box */
    .result-box-success {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        margin-top: 30px;
    }

    .result-box-success h2 {
        color: #d4af37;
        margin: 0 0 15px 0;
        font-size: 1.3em;
    }

    .price-range {
        font-size: 2em;
        color: #d4af37;
        font-weight: 700;
        margin: 15px 0;
    }

    .price-label {
        font-size: 1.1em;
        color: #e8e8e8;
        margin-top: 15px;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
        color: white !important;
        font-weight: 600;
        padding: 12px 30px !important;
        border: none !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2c5aa0 0%, #1a3a52 100%) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }

    /* Info Box */
    .info-box {
        background: #f0f4f8;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #d4af37;
        margin: 20px 0;
    }

    .info-box h3 {
        color: #1a3a52;
        margin-top: 0;
    }

    /* Divider */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #1a3a52, #d4af37, #1a3a52);
        margin: 30px 0;
        border-radius: 2px;
    }

    /* Footer section */
    .footer-section {
        background: #1a3a52;
        color: white;
        padding: 40px;
        border-radius: 8px;
        text-align: center;
        margin-top: 60px;
    }

    .footer-section h2 {
        color: #d4af37;
    }

    </style>
    """, unsafe_allow_html=True)

# Load pickle files
try:
    with open('df (1).pkl', 'rb') as file:
        df = pickle.load(file)

    with open('pipeline (1).pkl', 'rb') as file:
        pipeline = pickle.load(file)

    # Try to load analysis files (optional)
    try:
        new_df = pd.read_csv('data_viz1.xls')
        wordcloud_df = pd.read_csv('wordcloud_df.xls')
        feature_text = pickle.load(open('feature_text.pkl', 'rb'))
        analysis_available = True
    except:
        analysis_available = False

    # Try to load recommendation files (optional)
    try:
        location_df = pickle.load(open('location_distance.pkl', 'rb'))
        cosine_sim1 = pickle.load(open('cosine_sim1', 'rb'))
        cosine_sim2 = pickle.load(open('cosine_sim2', 'rb'))
        cosine_sim3 = pickle.load(open('cosine_sim3', 'rb'))
        recommendation_available = True
    except:
        recommendation_available = False

except FileNotFoundError as e:
    st.error(f"⚠️ Error loading files: {str(e)}")
    st.info("Please ensure all pickle files are in the same directory")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "💰 Prediction", "📊 Analytics", "🎯 Recommendations"])

# ===================== TAB 1: HOME PAGE =====================
with tab1:
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1>🏠 RealEstatePro</h1>
            <p>Your Smart Property Management System</p>
            <p style="font-size: 1em; color: white;">Intelligent Solutions for Modern Real Estate</p>
        </div>
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
        <div class="divider"></div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("""
        ## Welcome to RealEstatePro

        Your one-stop solution for intelligent property management and analysis. 
        Leverage the power of **Artificial Intelligence** and **Machine Learning** to make 
        smarter real estate decisions.

        Whether you're a buyer, seller, or property manager, RealEstatePro provides you with 
        comprehensive tools to analyze, predict, and recommend properties with precision.
        """)

    with col2:
        st.markdown("""
        ### 🎯 Our Mission

        To revolutionize real estate by providing:
        - **Accurate Price Predictions**
        - **Market Intelligence**
        - **Smart Recommendations**
        - **Data-Driven Insights**
        """)

    # Features Section
    st.markdown("""
        <div class="divider"></div>
        <h2 style="text-align: center; color: #1a3a52;">✨ Key Features</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    features = [
        {
            "emoji": "📍",
            "title": "Location Intelligence",
            "desc": "Find properties based on location and preferences with advanced filtering"
        },
        {
            "emoji": "💰",
            "title": "Price Prediction",
            "desc": "Get accurate AI-powered price predictions using advanced ML algorithms"
        },
        {
            "emoji": "🏆",
            "title": "Luxury Scoring",
            "desc": "Identify premium properties with our intelligent luxury scoring system"
        },
        {
            "emoji": "📊",
            "title": "Market Analytics",
            "desc": "Analyze trends, patterns, and insights from comprehensive market data"
        }
    ]

    columns = [col1, col2, col3, col4]

    for col, feature in zip(columns, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{feature['emoji']} {feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Stats Section
    st.markdown("""
        <div class="divider"></div>
        <h2 style="text-align: center; color: #1a3a52;">📈 Why Choose RealEstatePro?</h2>
    """, unsafe_allow_html=True)

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-label">Accuracy Rate</div>
            <div class="stat-number">95%</div>
            <div class="stat-label">Price Predictions</div>
        </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-label">Properties Analyzed</div>
            <div class="stat-number">5000+</div>
            <div class="stat-label">Real Estate Data</div>
        </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-label">Locations Covered</div>
            <div class="stat-number">50+</div>
            <div class="stat-label">Across India</div>
        </div>
        """, unsafe_allow_html=True)

    with stat_col4:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-label">User Satisfaction</div>
            <div class="stat-number">4.9★</div>
            <div class="stat-label">Out of 5</div>
        </div>
        """, unsafe_allow_html=True)

    # How It Works
    st.markdown("""
        <div class="divider"></div>
        <h2 style="text-align: center; color: #1a3a52;">⚙️ How It Works</h2>
    """, unsafe_allow_html=True)

    step_col1, step_col2, step_col3, step_col4 = st.columns(4)

    steps = [
        {"num": "01", "title": "Input Details", "desc": "Enter property details"},
        {"num": "02", "title": "AI Analysis", "desc": "Our ML model analyzes"},
        {"num": "03", "title": "Get Predictions", "desc": "Receive accurate results"},
        {"num": "04", "title": "Make Decision", "desc": "Make informed choices"}
    ]

    step_columns = [step_col1, step_col2, step_col3, step_col4]

    for col, step in zip(step_columns, steps):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align: center;">
                <div style="font-size: 2.5em; color: #d4af37; font-weight: 700; margin-bottom: 10px;">
                    {step['num']}
                </div>
                <h4 style="color: #1a3a52; margin: 10px 0;">{step['title']}</h4>
                <p style="color: #666;">{step['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer-section">
            <h2>RealEstatePro © 2024</h2>
            <p>Transforming Real Estate with AI & Machine Learning</p>
            <p style="color: #d4af37;">📧 contact@realestatepro.com | 📱 +91-XXXXXXXXXX</p>
        </div>
    """, unsafe_allow_html=True)

# ===================== TAB 2: PREDICTION PAGE =====================
with tab2:
    st.markdown("""
        <div class="header-section">
            <h1>💰 Property Price Prediction</h1>
            <p>Get accurate AI-powered price predictions for your property</p>
        </div>
        """, unsafe_allow_html=True)

    # Info Section
    st.markdown("""
        <div class="info-box">
            <h3>📋 How It Works</h3>
            <p>Enter your property details below and our advanced machine learning model will predict 
            the price range for your property with high accuracy. All fields are required for accurate predictions.</p>
        </div>
        """, unsafe_allow_html=True)

    # Form Container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">🏠 Property Details</h2>', unsafe_allow_html=True)

    # Row 1: Property Type and Location
    col1, col2 = st.columns(2)

    with col1:
        property_type = st.selectbox(
            'Property Type',
            ['flat', 'house'],
            help="Select whether it's a flat or house"
        )

    with col2:
        location = st.selectbox(
            'Location',
            sorted(df['location'].unique().tolist()),
            help="Select the location of the property"
        )

    # Row 2: Bedrooms and Bathrooms
    st.markdown('<h2 class="section-header">🛏️ Rooms & Facilities</h2>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        bedRooms = float(st.selectbox(
            'Number of Bedrooms',
            sorted(df['bedRoom'].unique().tolist()),
            help="Select number of bedrooms"
        ))

    with col4:
        bathRooms = float(st.selectbox(
            'Number of Bathrooms',
            sorted(df['bathroom'].unique().tolist()),
            help="Select number of bathrooms"
        ))

    # Row 3: Balcony and Store Room
    col5, col6 = st.columns(2)

    with col5:
        balcony = st.selectbox(
            'Balconies',
            [0, 1],
            help="Does the property have a balcony?"
        )

    with col6:
        store_room = st.selectbox(
            'Store Room',
            [0, 1],
            help="Does the property have a store room?"
        )

    # Row 4: Servant Room and Property Age
    st.markdown('<h2 class="section-header">⏳ Property Information</h2>', unsafe_allow_html=True)

    col7, col8 = st.columns(2)

    with col7:
        servant_room = st.selectbox(
            'Servant Room',
            [0, 1],
            help="Does the property have a servant room?"
        )

    with col8:
        Property_Age = st.selectbox(
            'Property Age',
            sorted(df['agePossession'].unique().tolist()),
            help="Select the age of the property"
        )

    # Row 5: Furnishing and Luxury Category
    st.markdown('<h2 class="section-header">✨ Features & Luxury</h2>', unsafe_allow_html=True)

    col9, col10 = st.columns(2)

    with col9:
        furnishing_type = st.selectbox(
            'Furnishing Type',
            sorted(df['furnishing_type'].unique().tolist()),
            help="Select the furnishing type"
        )

    with col10:
        luxury_category = st.selectbox(
            'Luxury Category',
            sorted(df['luxury_category'].unique().tolist()),
            help="Select the luxury category"
        )

    # Row 6: Floor Category and Built-up Area
    col11, col12 = st.columns(2)

    with col11:
        floor_category = st.selectbox(
            'Floor Category',
            sorted(df['floor_category'].unique().tolist()),
            help="Select the floor category"
        )

    with col12:
        built_up_area = float(st.number_input(
            'Built Up Area (sq ft)',
            min_value=0.0,
            step=100.0,
            help="Enter the built-up area in square feet"
        ))

    st.markdown('</div>', unsafe_allow_html=True)

    # Predict Button
    st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        predict_button = st.button('🔍 Predict Property Price', use_container_width=True)

    # Prediction Logic
    if predict_button:
        if built_up_area <= 0:
            st.error("❌ Please enter a valid built-up area")
        else:
            try:
                # Create DataFrame
                data = [[property_type, location, bedRooms, bathRooms, balcony, Property_Age,
                         store_room, servant_room, furnishing_type, luxury_category, floor_category, built_up_area]]

                columns = ['property_type', 'location', 'bedRoom', 'bathroom', 'balcony',
                           'agePossession', 'Store Room', 'Servant Room',
                           'furnishing_type', 'luxury_category', 'floor_category', 'built_up_area']

                one_df = pd.DataFrame(data, columns=columns)

                # Predict
                base_price = np.expm1(pipeline.predict(one_df))[0]
                low = base_price - 0.22
                high = base_price + 0.22

                # Display Result
                st.markdown("""
                    <div class="result-box-success">
                        <h2>✅ Prediction Successful!</h2>
                        <p class="price-label">Estimated Property Price Range:</p>
                        <div class="price-range">
                            PKR {:.2f} Cr - PKR {:.2f} Cr
                        </div>
                        <p class="price-label">
                            <strong>Mid Range Price:</strong> PKR {:.2f} Cr
                        </p>
                        <p style="margin-top: 20px; color: #d4af37; font-size: 0.95em;">
                            💡 This prediction is based on market analysis and property features
                        </p>
                    </div>
                    """.format(low, high, base_price), unsafe_allow_html=True)

                # Additional Info
                st.markdown("""
                    <div class="info-box" style="margin-top: 30px;">
                        <h3>📊 What This Means</h3>
                        <ul style="color: #333;">
                            <li><strong>Low Price:</strong> Conservative estimate based on current market</li>
                            <li><strong>High Price:</strong> Optimistic estimate for prime location/condition</li>
                            <li><strong>Mid Price:</strong> Most likely selling price range</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error in prediction: {str(e)}")
                st.info("Please check your inputs and try again")

    # Footer
    st.markdown("""
        <div style="margin-top: 50px; padding-top: 30px; border-top: 2px solid #d4af37; text-align: center;">
            <p style="color: #666; font-size: 0.9em;">
                <strong>Disclaimer:</strong> Predictions are estimates based on historical data and market trends. 
                Actual prices may vary based on additional factors not captured in the model.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ===================== TAB 3: ANALYTICS PAGE =====================
with tab3:
    if analysis_available:
        st.markdown("""
            <div class="header-section">
                <h1>📊 Market Analytics & Insights</h1>
                <p>Explore comprehensive market data and trends</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<h2 class="section-header">🗺️ Location Price per Sqft Geomap</h2>', unsafe_allow_html=True)

        group_df = (
            new_df.groupby('location')[['price_in_crore', 'price_per_sqft', 'area', 'latitude', 'longitude']]
            .mean()
        )

        fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='area',
                                color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                                mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)

        st.plotly_chart(fig, use_container_width=True)

        # Wordcloud section
        st.markdown('<h2 class="section-header">📝 Features Wordcloud</h2>', unsafe_allow_html=True)

        location_option = wordcloud_df['location'].unique().tolist()
        location_option.insert(0, 'overall')

        selected_location = st.selectbox('Select Location', location_option)

        if selected_location == 'overall':
            figure = WordCloud(width=800, height=800,
                               background_color='white',
                               stopwords=set(['s']),
                               min_font_size=10).generate(feature_text)
        else:
            filtered_df = wordcloud_df[wordcloud_df['location'] == selected_location]
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

        if figure is not None:
            fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
            ax.imshow(figure, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        else:
            st.error("Could not generate wordcloud")

        # Area Vs Price
        st.markdown('<h2 class="section-header">📐 Area Vs Price Analysis</h2>', unsafe_allow_html=True)

        property_type = st.selectbox('Select Property Type', ['flat', 'house'])

        if property_type == 'house':
            fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="area", y="price_in_crore", color="bedRoom",
                              title="Area Vs Price - Houses",
                              labels={"area": "Area (sq ft)", "price_in_crore": "Price (Crore ₹)"})
            st.plotly_chart(fig1, use_container_width=True)
        else:
            fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="area", y="price_in_crore", color="bedRoom",
                              title="Area Vs Price - Flats",
                              labels={"area": "Area (sq ft)", "price_in_crore": "Price (Crore ₹)"})
            st.plotly_chart(fig1, use_container_width=True)

        # BHK Pie Chart
        st.markdown('<h2 class="section-header">🥧 BHK Distribution</h2>', unsafe_allow_html=True)

        sector_options = new_df['location'].unique().tolist()
        sector_options.insert(0, 'overall')

        selected_sector = st.selectbox('Select location for BHK', sector_options)

        if selected_sector == 'overall':
            fig2 = px.pie(new_df, names='bedRoom', title="BHK Distribution - Overall")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            fig2 = px.pie(new_df[new_df['location'] == selected_sector], names='bedRoom',
                          title=f"BHK Distribution - {selected_sector}")
            st.plotly_chart(fig2, use_container_width=True)

        # Price comparison
        st.markdown('<h2 class="section-header">💹 Price Range by BHK</h2>', unsafe_allow_html=True)

        fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price_in_crore',
                      title='Price Range by Number of Bedrooms',
                      labels={"bedRoom": "Number of Bedrooms", "price_in_crore": "Price (Crore ₹)"})

        st.plotly_chart(fig3, use_container_width=True)

        # Histogram
        st.markdown('<h2 class="section-header">📈 Price Distribution by Property Type</h2>', unsafe_allow_html=True)

        fig4 = plt.figure(figsize=(12, 5))
        sns.histplot(new_df[new_df['property_type'] == 'house']['price_in_crore'], kde=True, label='house')
        sns.histplot(new_df[new_df['property_type'] == 'flat']['price_in_crore'], kde=True, label='flat')
        plt.legend()
        st.pyplot(fig4)

    else:
        st.error(
            "⚠️ Analysis files not found. Please ensure data_viz1.xls, wordcloud_df.xls, and feature_text.pkl are available.")

# ===================== TAB 4: RECOMMENDATION PAGE =====================
with tab4:
    if recommendation_available:
        st.markdown("""
            <div class="header-section">
                <h1>🎯 Smart Property Recommendations</h1>
                <p>Find similar properties based on your preferences</p>
            </div>
            """, unsafe_allow_html=True)


        def recommend_properties_with_scores(property_name, top_n=247):
            cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3

            # Get the index location of the property
            property_index = location_df.index.get_loc(property_name)

            # Get the similarity scores for the property using its index
            sim_scores = list(enumerate(cosine_sim_matrix.iloc[property_index]))

            # Sort properties based on the similarity scores
            sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the indices and scores of the top_n most similar properties
            top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
            top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

            # Retrieve the names of the top properties using the indices
            top_properties = location_df.index[top_indices].tolist()

            # Create a dataframe with the results
            recommendations_df = pd.DataFrame({
                'PropertyName': top_properties,
                'SimilarityScore': top_scores
            })

            return recommendations_df


        # Location based search
        st.markdown('<h2 class="section-header">📍 Search Properties by Location & Radius</h2>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            selected_location = st.selectbox('Select Location', sorted(location_df.columns.to_list()))

        with col2:
            radius = st.number_input('Radius (in Kms)', min_value=0.0, step=0.5)

        with col3:
            search_button = st.button('🔍 Search', use_container_width=True)

        if search_button:
            if radius > 0:
                result_ser = location_df[location_df[selected_location] < radius * 1000][
                    selected_location].sort_values()

                if len(result_ser) > 0:
                    st.markdown(f"""
                        <div class="info-box">
                            <h3>✅ Found {len(result_ser)} properties within {radius} km</h3>
                        </div>
                        """, unsafe_allow_html=True)

                    for key, value in result_ser.items():
                        st.text(f"📍 {str(key)} - {str(round(value / 1000, 2))} km")
                else:
                    st.warning(f"⚠️ No properties found within {radius} km of {selected_location}")
            else:
                st.error("❌ Please enter a valid radius")

        # Property Recommendation
        st.markdown('<h2 class="section-header">🎯 Recommend Similar Properties</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            selected_appartment = st.selectbox('Select a property', sorted(location_df.index.to_list()))

        with col2:
            recommend_button = st.button('✨ Recommend', use_container_width=True)

        if recommend_button:
            try:
                recommendation_df = recommend_properties_with_scores(selected_appartment)

                st.markdown("""
                    <div class="info-box">
                        <h3>🏆 Top Similar Properties</h3>
                        <p>These properties are most similar to your selection based on location, features, and market factors.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.dataframe(recommendation_df.head(20), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error generating recommendations: {str(e)}")

    else:
        st.error(
            "⚠️ Recommendation files not found. Please ensure location_distance.pkl and cosine_sim files are available.")


