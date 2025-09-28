
import streamlit as st 
import base64 

# --- Page Config --- 
st.set_page_config( 
    page_title="Stock Data Analysis", 
    page_icon="heavy_dollar_sign", 
    layout="wide" 
) 

# --- SVG Page Heading (smaller) --- 
st.markdown( 
    """ 
    <h1 style="font-size:2rem;"> 
        <svg height="32" width="32" style="vertical-align:middle; margin-right:10px;"> 
            <rect width="6" height="20" x="0" y="4" fill="#4CAF50"></rect> 
            <rect width="6" height="14" x="10" y="10" fill="#2196F3"></rect> 
            <rect width="6" height="10" x="20" y="16" fill="#FF9800"></rect> 
        </svg> 
        Stock Data Analysis 
    </h1> 
    """, unsafe_allow_html=True 
) 

# --- Convert Local Image to Base64 --- 
def get_base64(file): 
    with open(file, "rb") as f: 
        return base64.b64encode(f.read()).decode() 

img_base64 = get_base64("stock_photo.png") 

# --- Custom CSS for Background + Overlay + Service Boxes --- 
st.markdown( 
    f""" 
    <style> 
    /* Background Image with Dark Overlay */ 
    .stApp {{ 
        background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url("data:image/png;base64,{img_base64}"); 
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed; 
    }} 

    /* Hero Section Overlay */ 
    .overlay {{ 
        padding: 4rem; 
        border-radius: 10px; 
        text-align: center; 
        margin-bottom: 3rem; 
    }} 
    .overlay h1 {{ 
        color: white !important; 
        font-size: 4rem; 
        font-weight: bold; 
    }} 
    .overlay p {{ 
        color: white !important; 
        font-size: 1.1rem; 
    }} 

    /* Service Boxes */ 
    .service-box {{ 
        background-color: rgba(0,0,0,0.15); 
        padding: 1.5rem; 
        border-radius: 10px; 
        margin-bottom: 1rem; 
        transition: transform 0.3s, box-shadow 0.3s; 
    }} 
    .service-box:hover {{ 
        transform: translateY(-5px); 
        box-shadow: 0 8px 20px rgba(0,0,0,0.3); 
    }} 
    .service-box h3 {{ 
        color: white; 
        margin-bottom: 0.5rem; 
    }} 
    .service-box p {{ 
        color: white; 
        margin: 0; 
    }} 
    </style> 
    """, unsafe_allow_html=True 
) 

# --- Hero Section --- 
st.markdown( 
    """ 
    <div class="overlay"> 
        <h1>Market Insights & Forecasts</h1> 
        <p> 
            Welcome to the <b>Stock Data Analysis App</b>. 
            Here you can <b>explore real stock information, predict future trends, and evaluate risk & returns</b> using modern financial models. 
        </p> 
    </div> 
    """, unsafe_allow_html=True 
) 

st.markdown("---") 

# --- Services Section --- 
st.markdown( 
    "<h2 style='text-align:center; font-size:3rem; margin-bottom:2rem;'>Features & Services</h2>", 
    unsafe_allow_html=True 
) 

# Service 1 - Cyan (faded) 
st.markdown(
    """
    <a href='Stock_Analysis' style="text-decoration: none; color: inherit;">
        <div class="service-box" style="background-color: rgba(0, 188, 212, 0.15); cursor: pointer;">
            <h3>1. Stock Information</h3>
            <p>View detailed information about selected stocks including historical prices, volumes, and company data.</p>
        </div>
    </a>
    """,
    unsafe_allow_html=True
)


# Service 2 - Blue (faded) 
st.markdown( 
    """  
    <a href='/Stock_Prediction' style="text-decoration: none; color: inherit;">
        <div class="service-box" style="background-color: rgba(33, 150, 243, 0.15);"> 
            <h3>2. Stock Prediction</h3> 
            <p>Predict closing prices for the next <b>30 days</b> using advanced forecasting models based on historical data.</p> 
        </div> 
    </a>
    """, unsafe_allow_html=True 
) 

# Service 3 - Orange (faded) 
st.markdown( 
    """ 
    <div class="service-box" style="background-color: rgba(255, 152, 0, 0.15);"> 
        <h3>3. CAPM Return</h3> 
        <p>Discover how the <b>Capital Asset Pricing Model (CAPM)</b> calculates expected returns based on risk.</p> 
    </div> 
    """, unsafe_allow_html=True 
) 

# Service 4 - Red (faded) 
st.markdown( 
    """ 
    <div class="service-box" style="background-color: rgba(244, 67, 54, 0.15);"> 
        <h3>4. CAPM Beta</h3> 
        <p>Calculate <b>Beta</b> and <b>Expected Return</b> for individual stocks to evaluate their market sensitivity.</p> 
    </div> 
    """, unsafe_allow_html=True 
) 

st.markdown("---") 
st.caption("⚡ Powered by Python • Streamlit • Finance APIs") 
