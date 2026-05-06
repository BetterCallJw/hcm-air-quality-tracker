import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_daily_air_quality():
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Ngày hôm qua (định dạng YYYY-MM-DD cho API)
    target_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    lat, lon = 10.7626, 106.6602

    # Lấy TRỰC TIẾP giá trị theo ngày (Daily)
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=european_aqi_max,pm2_5_max,pm10_max,uv_index_max&" # Đây là các giá trị trực tiếp theo ngày
        f"start_date={target_date}&end_date={target_date}&"
        f"timezone=Asia%2FBangkok"
    )
    
    response = requests.get(url)
    response.raise_for_status()
    
    daily_results = response.json()['daily']

    # Tạo DataFrame từ giá trị trả về trực tiếp
    new_data = pd.DataFrame({
        'Ngày': [display_date],
        'AQI (Giá trị ngày)': [daily_results['european_aqi_max'][0]],
        'PM2.5 (Giá trị ngày)': [daily_results['pm2_5_max'][0]],
        'UV Index (Giá trị ngày)': [daily_results['uv_index_max'][0]]
    })

    file_name = 'hcm_air_quality_log.xlsx'
    
    if os.path.exists(file_name):
        existing_data = pd.read_excel(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_excel(file_name, index=False)
    print(f"Đã lấy trực tiếp và cập nhật dữ liệu ngày {display_date}")

if __name__ == "__main__":
    fetch_daily_air_quality()
