import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Temperature Change visualiser")

st.title("Temperature change visualisation: SDG 13")
st.markdown("""
### Explore how climate has affected temperature in various parts of the world!
Select a location and time range to visualize the changes in temperature over time.
Real-world data provided by the Meteomatics API.
""")

# Predefined countries and their coordinates (latitude, longitude)
country_coords = {
    "Afghanistan": (33.93911, 67.70995),
    "Albania": (41.1533, 20.1683),
    "Algeria": (28.0339, 1.6596),
    "Andorra": (42.5063, 1.5211),
    "Angola": (-11.2027, 17.8739),
    "Antigua and Barbuda": (17.0608, -61.7964),
    "Argentina": (-38.4161, -63.6167),
    "Armenia": (40.0691, 45.0382),
    "Australia": (-25.2744, 133.7751),
    "Austria": (47.5162, 14.5501),
    "Azerbaijan": (40.1431, 47.5769),
    "Bahamas": (25.0343, -77.3963),
    "Bahrain": (25.9304, 50.6379),
    "Bangladesh": (23.685, 90.3563),
    "Barbados": (13.1939, -59.5432),
    "Belarus": (53.9045, 27.559),
    "Belgium": (50.8503, 4.3517),
    "Belize": (17.1899, -88.4976),
    "Benin": (9.3077, 2.3158),
    "Bhutan": (27.5149, 90.4336),
    "Bolivia": (-16.5000, -68.1193),
    "Bosnia and Herzegovina": (43.8486, 17.6791),
    "Botswana": (-22.3285, 24.6849),
    "Brazil": (-23.5505, -46.6333),  # São Paulo
    "Brunei": (4.5353, 114.7277),
    "Bulgaria": (42.7339, 25.4858),
    "Burkina Faso": (12.2383, -1.5616),
    "Burundi": (-3.3731, 29.9189),
    "Cabo Verde": (16.0020, -24.0132),
    "Cambodia": (12.5657, 104.9910),
    "Cameroon": (7.3697, 12.3547),
    "Canada": (56.1304, -106.3468),
    "Central African Republic": (6.6111, 20.9394),
    "Chad": (15.4542, 18.7322),
    "Chile": (-35.6751, -71.5430),
    "China": (39.9042, 116.4074),  # Beijing
    "Colombia": (4.5709, -74.2973),
    "Comoros": (-11.7020, 43.2540),
    "Congo, Democratic Republic of the": (-4.0383, 21.7587),
    "Congo, Republic of the": (-4.4961, 15.8277),
    "Costa Rica": (9.7489, -83.7534),
    "Croatia": (45.1, 15.2),
    "Cuba": (21.5216, -77.7812),
    "Cyprus": (35.1264, 33.4299),
    "Czech Republic": (49.8175, 15.4730),
    "Denmark": (56.2639, 9.5018),
    "Djibouti": (11.8251, 42.5903),
    "Dominica": (15.4150, -61.3710),
    "Dominican Republic": (18.7357, -70.1627),
    "Ecuador": (-1.8312, -78.1834),
    "Egypt": (26.8206, 30.8025),
    "El Salvador": (13.7942, -88.8965),
    "Equatorial Guinea": (1.6508, 10.2679),
    "Eritrea": (15.1792, 39.7823),
    "Estonia": (58.5953, 25.0136),
    "Eswatini": (-26.5225, 31.4659),
    "Ethiopia": (9.1450, 40.4897),
    "Fiji": (-17.7134, 178.0650),
    "Finland": (61.9241, 25.7482),
    "France": (46.6034, 1.8883),
    "Gabon": (-0.8031, 11.6094),
    "Gambia": (13.4662, -16.5780),
    "Georgia": (42.3154, -43.3569),
    "Germany": (51.1657, 10.4515),
    "Ghana": (7.6731, -0.1860),
    "Greece": (39.0742, 21.8243),
    "Grenada": (12.1165, -61.6749),
    "Guatemala": (15.7835, -90.2308),
    "Guinea": (9.9456, -9.6966),
    "Guinea-Bissau": (11.8037, -15.1804),
    "Guyana": (4.8604, -58.9302),
    "Haiti": (18.9712, -72.2852),
    "Honduras": (15.1999, -86.2419),
    "Hungary": (47.1625, 19.5033),
    "Iceland": (64.9631, -19.0208),
    "India": (28.6139, 77.2090),  # New Delhi
    "Indonesia": (-6.2088, 106.8456),  # Jakarta
    "Iran": (32.4279, 53.6880),
    "Iraq": (33.2232, 43.6793),
    "Ireland": (53.4129, -8.2439),
    "Israel": (31.0461, 34.8516),
    "Italy": (41.8719, 12.5674),
    "Jamaica": (18.1096, -77.2975),
    "Japan": (36.2048, 138.2529),
    "Jordan": (30.5852, 36.2384),
    "Kazakhstan": (48.0196, 66.9237),
    "Kenya": (-0.0236, 37.9062),
    "Kiribati": (-3.3704, -168.7340),
    "Korea, North": (40.3399, 127.5101),
    "Korea, South": (35.9078, 127.7669),
    "Kuwait": (29.3759, 47.9774),
    "Kyrgyzstan": (41.2044, 74.7661),
    "Laos": (19.8563, 102.4955),
    "Latvia": (56.8796, 24.6032),
    "Lebanon": (33.8547, 35.8623),
    "Lesotho": (-29.6090, 28.2336),
    "Liberia": (6.4281, -9.4295),
    "Libya": (26.3351, 17.2283),
    "Liechtenstein": (47.1662, 9.5554),
    "Lithuania": (55.1694, 23.8813),
    "Luxembourg": (49.6118, 6.1319),
    "Madagascar": (-18.7669, 46.8691),
    "Malawi": (-13.2543, 34.3015),
    "Malaysia": (4.2105, 101.9758),
    "Maldives": (3.2028, 73.2207),
    "Mali": (17.5707, -3.9962),
    "Malta": (35.9375, 14.3754),
    "Marshall Islands": (7.1095, 171.1851),
    "Mauritania": (20.2540, -10.1401),
    "Mauritius": (-20.348404, 57.552152),
    "Mexico": (23.6345, -102.5528),
    "Micronesia": (7.4256, 150.5508),
    "Moldova": (47.4116, 28.3699),
    "Monaco": (43.7384, 7.4246),
    "Mongolia": (46.8625, 103.8467),
    "Montenegro": (42.7087, 19.3744),
    "Morocco": (31.7917, -7.0926),
    "Mozambique": (-18.6657, 35.5296),
    "Myanmar": (21.9162, 95.9555),
    "Namibia": (-22.9576, 18.4904),
    "Nauru": (-0.5228, 166.9315),
    "Nepal": (28.3949, 84.1240),
    "Netherlands": (52.1326, 5.2913),
    "New Zealand": (-40.9006, 174.886),
    "Nicaragua": (12.8654, -85.2072),
    "Niger": (17.6078, 8.0817),
    "Nigeria": (9.0820, 8.6753),
    "North Macedonia": (41.6086, 21.7453),
    "Norway": (60.4720, 8.4689),
    "Oman": (21.5129, 55.9233),
    "Pakistan": (30.3753, 69.3451),
    "Palau": (7.5149, 134.5825),
    "Palestine": (31.9522, 35.2332),
    "Panama": (8.9824, -79.5199),
    "Papua New Guinea": (-6.31499, 143.9555),
    "Paraguay": (-23.4420, -58.4438),
    "Peru": (-9.1899, -75.0152),
    "Philippines": (12.8797, 121.7740),
    "Poland": (51.9194, 19.1451),
    "Portugal": (39.3999, -8.2245),
    "Qatar": (25.276987, 51.520008),
    "Romania": (45.9432, 24.9668),
    "Russia": (61.5240, 105.3188),
    "Rwanda": (-1.9403, 29.8739),
    "Saint Kitts and Nevis": (17.3578, -62.7832),
    "Saint Lucia": (13.9094, -60.9789),
    "Saint Vincent and the Grenadines": (12.9898, -61.2872),
    "Samoa": (-13.7590, -172.1046),
    "San Marino": (43.9333, 12.4467),
    "Sao Tome and Principe": (0.1864, 6.6131),
    "Saudi Arabia": (23.8859, 45.0792),
    "Senegal": (14.4974, -14.4524),
    "Serbia": (44.0165, 21.0059),
    "Seychelles": (-4.6796, 55.4919),
    "Sierra Leone": (8.4657, -11.7799),
    "Singapore": (1.3521, 103.8198),
    "Slovakia": (48.6690, 19.6990),
    "Slovenia": (46.1512, 14.9955),
    "Solomon Islands": (-9.6457, 160.0240),
    "Somalia": (5.1521, 46.1996),
    "South Africa": (-30.5595, 22.9375),  # Cape Town
    "South Sudan": (6.8769, 31.3069),
    "Spain": (40.4637, -3.7492),
    "Sri Lanka": (7.8731, 80.7718),
    "Sudan": (12.8628, 30.2176),
    "Suriname": (3.9193, -56.0274),
    "Sweden": (60.1282, 18.6435),
    "Switzerland": (46.8182, 8.2275),
    "Syria": (34.8021, 38.9968),
    "Tajikistan": (38.8610, 71.2761),
    "Tanzania": (-6.3690, 34.8888),
    "Thailand": (15.8700, 100.9925),
    "Togo": (8.6195, 0.8248),
    "Tonga": (-21.1789, -175.1982),
    "Trinidad and Tobago": (10.6918, -61.2225),
    "Tunisia": (33.8869, 9.5375),
    "Turkey": (38.9637, 35.2433),
    "Turkmenistan": (40.0622, 59.5563),
    "Tuvalu": (-7.1095, 179.1945),
    "Uganda": (1.3733, 32.2903),
    "Ukraine": (48.3794, 31.1656),
    "United Arab Emirates": (23.4241, 53.8478),
    "United Kingdom": (55.3781, -3.4360),
    "United States": (37.7749, -122.4194),  # San Francisco, CA
    "Uruguay": (-32.5228, -55.7659),
    "Uzbekistan": (41.3775, 64.5852),
    "Vanuatu": (-15.3764, 166.9591),
    "Vatican City": (41.9029, 12.4534),
    "Venezuela": (6.4238, -66.5897),
    "Vietnam": (14.0583, 108.2772),
    "Yemen": (15.5524, 48.5164),
    "Zambia": (-13.1339, 27.8493),
    "Zimbabwe": (-19.0154, 29.1549)
}

st.sidebar.header("Select Input Method")
input_method = st.sidebar.radio("Choose how to enter the location:", ("Select Country", "Enter Coordinates"))

if input_method == "Select Country":
    country = st.sidebar.selectbox("Select Country", list(country_coords.keys()))
    latitude, longitude = country_coords[country]
else:
    st.sidebar.header("Enter Coordinates Manually")
    latitude = st.sidebar.text_input("Latitude", "37.7749")  # Default: San Francisco
    longitude = st.sidebar.text_input("Longitude", "-122.4194")

st.sidebar.header("Select Time Period")
start_year = st.sidebar.slider("Start Year", 1941, 2020, 1941)
end_year = st.sidebar.slider("End Year", 1941, 2023, 2023)

st.sidebar.header("Select Parameters to Graph")
parameters_to_graph = st.sidebar.multiselect("Choose Parameters", ["Temperature", "Humidity", "Cloud Cover", "Evaporation"], default="Temperature")

st.sidebar.header("Customize Chart Appearance")
line_color = st.sidebar.color_picker("Select Line Color", "#1f77b4")
marker_style = st.sidebar.selectbox("Select Marker Style", ["Circle", "Square", "Diamond"])

API_USERNAME = st.secrets["general"]["API_USERNAME"]
API_PASSWORD = st.secrets["general"]["API_PASSWORD"]

def get_weather_data(latitude, longitude, start_year, end_year):
    base_url = "https://api.meteomatics.com"
    start_date = f"{start_year}-07-22T15:00:00Z"
    end_date = f"{end_year}-07-22T15:00:00Z"
    location = f"{latitude},{longitude}"
    parameter = "t_2m:F,relative_humidity_2m:p,effective_cloud_cover:octas,evaporation_24h:mm"
    query = f"/{start_date}--{end_date}:P1Y/{parameter}/{location}/json?model=mix"
    url = f"{base_url}{query}"
    response = requests.get(url, auth=(API_USERNAME, API_PASSWORD))

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None
    
def plot_chart(df, param, unit):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df[param], mode='markers+lines',
                                name=param,
                                marker=dict(symbol=marker_style.lower(), size=8, color=line_color),
                                line=dict(color=line_color)))
    x_min = df['Date'].min()
    x_max = df['Date'].max()
    r = df[param].max() - df[param].min()
    y_min = df[param].min() - int(r * 0.1)
    y_max = df[param].max() + int(r * 0.1)

    fig.update_layout(
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[y_min, y_max]),
    )

    z = np.polyfit(df['Date'].astype(int), df[param], 1)  # Linear regression
    p = np.poly1d(z)

    fig.add_trace(go.Scatter(x=df['Date'], y=p(df['Date'].astype(int)), mode='lines',
                            name='Trendline', line=dict(color='red', dash='dash')))

    frames = []
    for k in range(len(df)):
        trend_y = p(df['Date'][:k+1].astype(int))
        frames.append(go.Frame(data=[
            go.Scatter(x=df['Date'][:k+1], y=df[param][:k+1],
                        mode='markers+lines',
                        marker=dict(symbol=marker_style.lower(), size=8, color=line_color),
                        line=dict(color=line_color)),
            go.Scatter(x=df['Date'][:k+1], y=trend_y,
                        mode='lines',
                        name='Trendline', line=dict(color='red', dash='dash'))
        ],
        name=str(df['Date'][k].year)))

    fig.frames = frames

    fig.update_layout(
        title=f'{param} Over Time',
        xaxis_title='Year',
        yaxis_title=f'{param} ({unit})',
        xaxis_tickformat='%Y',
        template='plotly_white',
        height=600,
        width=1000,
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'mode': 'immediate'}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'mode': 'immediate'}, 'mode': 'immediate'}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

data = get_weather_data(latitude, longitude, start_year, end_year)

if data:
    times = [entry['date'] for entry in data['data'][0]['coordinates'][0]['dates']]
    temps = [entry['value'] for entry in data['data'][0]['coordinates'][0]['dates']]
    humidities = [entry['value'] for entry in data['data'][1]['coordinates'][0]['dates']]
    cloud = [entry['value'] for entry in data['data'][2]['coordinates'][0]['dates']]
    evaporation = [entry['value'] for entry in data['data'][3]['coordinates'][0]['dates']]

    df = pd.DataFrame({"Date": pd.to_datetime(times), "Temperature": temps, 'Humidity': humidities, "Cloud Cover": cloud, "Evaporation": evaporation})

    for param in parameters_to_graph:
        unit = {"Temperature": "F", "Humidity": "p", "Cloud Cover": "octas", "Evaporation": "mm"}[param]
        plot_chart(df, param, unit)

else:
    st.write("No data available for the selected location or time range.")

