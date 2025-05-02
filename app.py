import streamlit as st
import joblib
import pandas as pd


model = joblib.load("linear_model.pkl")
expected_cols = joblib.load("feature_names.pkl")  

st.set_page_config(page_title="Car Price Predictor", layout="wide")
st.title("Used Car Price Predictor")

if 'name' not in st.session_state:
    st.session_state.name = "Maruti Wagon R LXI CNG"
    st.session_state.mileage = "26.6"
    st.session_state.power = "58.16"
    st.session_state.transmission = "Manual"
    st.session_state.owner_type = "First"
    st.session_state.location = "Mumbai"
    st.session_state.engine = "998"
    st.session_state.fuel = "Petrol"
    st.session_state.year = 2010
    st.session_state.seats = 5
    st.session_state.km_driven = 72000
    st.session_state.new_price = "0"

# --- Input UI Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.name = st.selectbox("Car Name", ["Maruti Wagon R LXI CNG", "Hyundai i20", "Honda City", "Other"], index=["Maruti Wagon R LXI CNG", "Hyundai i20", "Honda City", "Other"].index(st.session_state.name))
    st.session_state.mileage = st.text_input("Mileage (e.g. 26.6)", st.session_state.mileage)
    st.session_state.power = st.text_input("Power (bhp)", st.session_state.power)
    st.session_state.transmission = st.selectbox("Transmission", ["Manual", "Automatic"], index=["Manual", "Automatic"].index(st.session_state.transmission))
    st.session_state.owner_type = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"], index=["First", "Second", "Third", "Fourth & Above"].index(st.session_state.owner_type))

with col2:
    st.session_state.location = st.selectbox("Location", ["Mumbai", "Delhi", "Bangalore", "Chennai", "Other"], index=["Mumbai", "Delhi", "Bangalore", "Chennai", "Other"].index(st.session_state.location))
    st.session_state.engine = st.text_input("Engine (CC)", st.session_state.engine)
    st.session_state.fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"], index=["Petrol", "Diesel", "CNG", "LPG", "Electric"].index(st.session_state.fuel))
    st.session_state.year = st.slider("Year of Manufacture", 2000, 2025, st.session_state.year)
    st.session_state.seats = st.slider("Number of Seats", 2, 10, st.session_state.seats)

with col3:
    st.session_state.km_driven = st.number_input("Kilometers Driven", 0, 500000, st.session_state.km_driven, step=1000)
    st.session_state.new_price = st.text_input("Original New Price (Lakhs)", st.session_state.new_price)

# --- Input Summary ---
st.sidebar.subheader("Input Summary")
st.sidebar.write(f"**Car Name**: {st.session_state.name}")
st.sidebar.write(f"**Location**: {st.session_state.location}")
st.sidebar.write(f"**Year of Manufacture**: {st.session_state.year}")
st.sidebar.write(f"**Kilometers Driven**: {st.session_state.km_driven}")
st.sidebar.write(f"**Fuel Type**: {st.session_state.fuel}")
st.sidebar.write(f"**Transmission**: {st.session_state.transmission}")
st.sidebar.write(f"**Owner Type**: {st.session_state.owner_type}")
st.sidebar.write(f"**Mileage (km/l or km/kg)**: {st.session_state.mileage}")
st.sidebar.write(f"**Engine (CC)**: {st.session_state.engine}")
st.sidebar.write(f"**Power (bhp)**: {st.session_state.power}")
st.sidebar.write(f"**Seats**: {st.session_state.seats}")
st.sidebar.write(f"**Original New Price (Lakhs)**: {st.session_state.new_price}")

# --- Handle Prediction Logic After Button Press ---
predict_btn = st.button("Predict Price")

if predict_btn:
    try:
        # Convert numeric fields
        mileage_val = float(st.session_state.mileage.strip().split()[0]) if st.session_state.mileage else 0.0
        engine_val = float(st.session_state.engine.strip().split()[0]) if st.session_state.engine else 0.0
        power_val = float(st.session_state.power.strip().split()[0]) if st.session_state.power else 0.0
        new_price_val = float(st.session_state.new_price.strip()) if st.session_state.new_price else 0.0

        row = {
            "Year": st.session_state.year,
            "Kilometers_Driven": st.session_state.km_driven,
            "Mileage": mileage_val,
            "Engine": engine_val,
            "Power": power_val,
            "Seats": st.session_state.seats,

            "Transmission_Manual": 1 if st.session_state.transmission == "Manual" else 0,

            "Owner_Type_Second": 1 if st.session_state.owner_type == "Second" else 0,
            "Owner_Type_Third": 1 if st.session_state.owner_type == "Third" else 0,
            "Owner_Type_Fourth & Above": 1 if st.session_state.owner_type == "Fourth & Above" else 0,

            "Region_South": 1 if st.session_state.location in ["Bangalore", "Chennai"] else 0,
            "Region_North": 1 if st.session_state.location == "Delhi" else 0,
            "Region_East": 1 if st.session_state.location == "Kolkata" else 0,

            "Car_Type_Tier2": 1 if "Maruti" in st.session_state.name else 0,
            "Car_Type_Tier3": 1 if "Hyundai" in st.session_state.name else 0,
            "Car_Type_Tier4": 1 if "Honda" in st.session_state.name else 0,
            "Car_Type_Tier5": 1 if "Toyota" in st.session_state.name else 0,
            "Car_Type_Tier6": 1 if "BMW" in st.session_state.name else 0
        }

        input_df = pd.DataFrame([row])
        input_df = input_df.reindex(columns=expected_cols, fill_value=0)

        # Predict price
        pred = model.predict(input_df)
        st.success(f"Estimated Resale Price: ₹ {pred[0][0]:,.2f} lakhs")
        if new_price_val > 0:
            depreciation = new_price_val - pred[0][0]
            st.info(f"Estimated Depreciation: ₹ {depreciation:,.2f} lakhs")

    except ValueError as e:
        st.error(f"Error in input conversion: {e}")
