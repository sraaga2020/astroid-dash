import pandas as pd
import requests
from datetime import datetime, timedelta
import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Setting page configuration
st.set_page_config(
    page_title="Asteroid Impact Simulator",
    page_icon=":comet:",
    layout="wide"
)

import streamlit as st

# Custom CSS for Twinkling Stars Effect
st.markdown(
    """
    <style>
    body {
        background-color: black;
        overflow: hidden;
    }

    .stars {
        width: 2px;
        height: 2px;
        background: transparent;
        box-shadow: 
            25vw 20vh #fff,
            50vw 30vh #fff,
            75vw 80vh #fff,
            90vw 50vh #fff,
            10vw 70vh #fff,
            40vw 60vh #fff,
            70vw 10vh #fff,
            80vw 90vh #fff,
            60vw 20vh #fff,
            30vw 40vh #fff,
            85vw 85vh #fff,
            15vw 60vh #fff,
            20vw 90vh #fff,
            5vw 10vh #fff,
            55vw 15vh #fff,
            65vw 75vh #fff,
            35vw 30vh #fff,
            95vw 65vh #fff;
        animation: twinkle 2s infinite ease-in-out alternate;
    }

    @keyframes twinkle {
        from {
            opacity: 0.3;
        }
        to {
            opacity: 1;
        }
    }
    </style>
    """, unsafe_allow_html=True
)

# Add a div with the class 'stars' to render the stars
st.markdown("<div class='stars'></div>", unsafe_allow_html=True)

# Set the background color to black and apply starry animation for space theme
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #98eff5;  /* green blue color for headings */
        }
        .streamlit-expanderHeader {
            color: #1E90FF; /* Sky Blue for expander header */
        }
        .streamlit-expanderContent {
            background-color: rgba(0, 0, 0, 0.8);
        }
        .css-1d391kg {
            background-color: rgba(0, 0, 0, 0.8) !important;
        }
        .css-16toavk {
            background-color: rgba(0, 0, 0, 0.8) !important;
        }
        .twinkling-stars {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://media.giphy.com/media/6hgmw8zFqVwne/giphy.gif') repeat;
            animation: twinkle 1.5s infinite linear;
        }
        @keyframes twinkle {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
    </style>
    <div class="twinkling-stars"></div>
    """, unsafe_allow_html=True
)

# Define NASA API key and endpoint
API_KEY = "rb2YlKiDL61HAOxF394nFFWbA8bDxSal10d1Cr8y"
API_ENDPOINT = "https://api.nasa.gov/neo/rest/v1/feed"

# Fetch Asteroid Data using NASA API
@st.cache_data
def fetch_asteroid_data(start_date, end_date):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    
    asteroids = []
    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            asteroids.append({
                'name': asteroid['name'],
                'diameter_m': asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
                'speed_kmh': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                'distance_km': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                'orbiting_body': asteroid['close_approach_data'][0]['orbiting_body'],
                'hazardous': asteroid['is_potentially_hazardous_asteroid']
            })
    
    return pd.DataFrame(asteroids)

# Fetch data for the next 7 days (simulating real-time data)
start_date = datetime.now().strftime('%Y-%m-%d')
end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
asteroid_df = fetch_asteroid_data(start_date, end_date)

# Layout the Streamlit App
st.markdown(
    "<h1 style='text-align: center; color: #f56531;'>Asteroid Impact Simulator 🚀</h1>",
    unsafe_allow_html=True
)

# Display Data Metrics
st.markdown("---")
st.subheader("Asteroid Metrics Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Asteroids", len(asteroid_df))
col2.metric("Average Diameter (m)", f"{asteroid_df['diameter_m'].mean():.2f}")
col3.metric("Average Speed (km/h)", f"{asteroid_df['speed_kmh'].mean():.2f}")

# Select an Asteroid for Detailed Analysis
st.subheader("Select an Asteroid for Detailed Analysis")
selected_asteroid = st.selectbox("Choose an Asteroid", asteroid_df['name'].unique())
selected_data = asteroid_df[asteroid_df['name'] == selected_asteroid]

# Impact Simulation (For demonstration)
diameter = selected_data['diameter_m'].values[0]
speed = selected_data['speed_kmh'].values[0]  # Speed in km/h
distance = selected_data['distance_km'].values[0]  # Distance from Earth in km

# Let's assume that a larger diameter and speed leads to a bigger impact radius
impact_radius = np.log(diameter) * np.random.uniform(2,7)  # Scale impact radius by the diameter
impact_speed = np.log(speed) * 10  # Speed factor on impact

# Simulate the impact location based on distance and speed (for simplicity)
impact_location = [20 + np.random.uniform(-50, 50), 0 + np.random.uniform(-50, 50)]  # Random location on Earth map

# Create a Scatter Plot for the asteroid impact
trace = go.Scattergeo(
    lon=[impact_location[1]],
    lat=[impact_location[0]],
    mode="markers+text",
    marker=dict(
        size=impact_radius,  # Impact radius
        color='red',
        opacity=0.7,
        line=dict(width=1, color='black')
    ),
    textposition="bottom center"
)

layout = go.Layout(
    geo=dict(
        scope='world',
        projection_type='equirectangular',
        showland=True,
        landcolor='white',
        subunitwidth=1,
        countrywidth=1,
        coastlinewidth=1,
        projection_scale=1.0
    ),
    title={
            'text': "Asteroid Impact Simulation",
            'font': {'size': 36, 'color': '#db6060'}  # Adjust title size here
        },
    showlegend=False,
    geo_showcoastlines=True
)

fig = go.Figure(data=[trace], layout=layout)

# Display the impact animation in the app
st.plotly_chart(fig, use_container_width=True)

# Add a brief caption about the impact

# Display Selected Asteroid Details
st.markdown(f"### Asteroid Details: {selected_asteroid}")
st.write(f"Diameter: {selected_data['diameter_m'].values[0]} meters")
st.write(f"Speed: {selected_data['speed_kmh'].values[0]} km/h")
st.write(f"Distance from Earth: {selected_data['distance_km'].values[0]} km")
st.write(f"Orbiting Body: {selected_data['orbiting_body'].values[0]}")
st.write(f"Potentially Hazardous: {selected_data['hazardous'].values[0]}")
st.markdown(
    """
    <hr style="border: 2px solid #FFD700;"/>
    """, unsafe_allow_html=True
)

hazardous_asteroids = asteroid_df[asteroid_df['hazardous'] == True]
non_hazardous_asteroids = asteroid_df[asteroid_df['hazardous'] == False]

# Hazardous Asteroids Pie Chart
hazardous_count = len(asteroid_df[asteroid_df['hazardous'] == True])
non_hazardous_count = len(asteroid_df[asteroid_df['hazardous'] == False])

hazardous_pie_chart = go.Figure(
    data=[go.Pie(
        labels=['Hazardous', 'Non-Hazardous'],
        values=[hazardous_count, non_hazardous_count],
        hole=0.4,  # Donut chart
        marker=dict(colors=['#ff6666', '#66b3ff']),
        textinfo='percent+label',
        textfont=dict(size=14),
        name='Asteroid Risk'
    )],
    layout=go.Layout(
        title={
            'text': "Hazardous vs Non-Hazardous Asteroids",
            'font': {'size': 36, 'color': '#db6060'}  # Adjust title size here
        },
        showlegend=True
    )
)
st.plotly_chart(hazardous_pie_chart)

# Add description for Hazardous vs Non-Hazardous Asteroids
st.markdown(
    f"""
    ### Hazardous vs Non-Hazardous Asteroids:
    This pie chart displays the proportion of **hazardous** versus **non-hazardous** asteroids in the dataset. 
    - **Hazardous asteroids**: These are asteroids that could potentially impact Earth based on their size, speed, and proximity to the planet. 
    - **Non-hazardous asteroids**: These objects do not pose a direct threat to Earth at the moment.
    """
)

st.markdown(
    """
    <hr style="border: 2px solid #FFD700;"/>
    """, unsafe_allow_html=True
)


# Scatter Plot: Speed Distribution of Hazardous Asteroids
hazardous_speed_scatter = go.Figure(
    data=[go.Scatter(
        x=hazardous_asteroids['name'], 
        y=hazardous_asteroids['speed_kmh'], 
        mode='markers',
        marker=dict(size=8, color='rgba(255, 99, 132, 0.8)', symbol='circle'),
        text=hazardous_asteroids['name'],
        name='Speed (km/h)'
    )],
    layout=go.Layout(
        title={
            'text': "Speed Distribution of Hazardous Asteroids",
            'font': {'size': 36, 'color': '#db6060'}  # Adjust title size here
        },
        xaxis_title="Asteroid Name",
        yaxis_title="Speed (km/h)",
        showlegend=False,
        xaxis=dict(tickangle=90)
    )
)
st.plotly_chart(hazardous_speed_scatter)

# Add description for Speed Distribution
st.markdown(
    f"""
    ### Speed Distribution of Hazardous Asteroids:
    This scatter plot shows the distribution of **hazardous asteroids' speeds**. 
    The speed of an asteroid is an important factor in determining the impact risk:
    - Faster asteroids have higher kinetic energy, making them more dangerous upon impact.
    - Slower asteroids are less likely to cause significant damage, though they are still of interest.
    """
)

st.markdown(
    """
    <hr style="border: 2px solid #FFD700;"/>
    """, unsafe_allow_html=True
)

# Box Plot: Diameter Distribution of Hazardous Asteroids
hazardous_diameter_box = go.Figure(
    data=[go.Box(
        y=hazardous_asteroids['diameter_m'], 
        boxmean='sd',  # Shows the mean with the standard deviation
        name='Diameter (m)',
        marker=dict(color='rgba(54, 162, 235, 0.7)')
    )],
    layout=go.Layout(
        title={
            'text': "Diameter Distribution of Hazardous Asteroids",
            'font': {'size': 36, 'color': '#db6060'}  # Adjust title size here
        },
        yaxis_title="Diameter (meters)"
    )
)
st.plotly_chart(hazardous_diameter_box)

# Add description for Diameter Distribution
st.markdown(
    f"""
    ### Diameter Distribution of Hazardous Asteroids:
    This box plot illustrates the **diameter distribution** of hazardous asteroids in the dataset. 
    - **Larger asteroids** have the potential to cause more damage upon impact due to their mass.
    - **Smaller asteroids**, although still potentially dangerous, generally pose a lower risk of causing widespread destruction.
    """
)

# Custom CSS for Twinkling Stars Effect
st.markdown(
    """
    <style>
    body {
        background-color: black;
        overflow: hidden;
    }

    .stars {
        width: 2px;
        height: 2px;
        background: transparent;
        box-shadow: 
            25vw 20vh #fff,
            50vw 30vh #fff,
            75vw 80vh #fff,
            90vw 50vh #fff,
            10vw 70vh #fff,
            40vw 60vh #fff,
            70vw 10vh #fff,
            80vw 90vh #fff,
            60vw 20vh #fff,
            30vw 40vh #fff,
            85vw 85vh #fff,
            15vw 60vh #fff,
            20vw 90vh #fff,
            5vw 10vh #fff,
            55vw 15vh #fff,
            65vw 75vh #fff,
            35vw 30vh #fff,
            95vw 65vh #fff;
        animation: twinkle 2s infinite ease-in-out alternate;
    }

    @keyframes twinkle {
        from {
            opacity: 0.3;
        }
        to {
            opacity: 1;
        }
    }
    </style>
    """, unsafe_allow_html=True
)

# Add a div with the class 'stars' to render the stars
st.markdown("<div class='stars'></div>", unsafe_allow_html=True)

# Set the background color to black and apply starry animation for space theme
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #98eff5;  /* green blue color for headings */
        }
        .streamlit-expanderHeader {
            color: #1E90FF; /* Sky Blue for expander header */
        }
        .streamlit-expanderContent {
            background-color: rgba(0, 0, 0, 0.8);
        }
        .css-1d391kg {
            background-color: rgba(0, 0, 0, 0.8) !important;
        }
        .css-16toavk {
            background-color: rgba(0, 0, 0, 0.8) !important;
        }
        .twinkling-stars {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://media.giphy.com/media/6hgmw8zFqVwne/giphy.gif') repeat;
            animation: twinkle 1.0s infinite linear;
        }
        @keyframes twinkle {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
    </style>
    <div class="twinkling-stars"></div>
    """, unsafe_allow_html=True
)

# Add a button at the bottom to redirect to the external website
# Add a link button at the bottom to redirect to the external website
if st.button("Visit Asteroid Alien Attack"):
    st.write("[Click here to play and ML powered astroid alien game!](https://asteroid.streamlit.app)")

