import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_and_log_air_quality():
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Ngày hôm qua
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    lat, lon = 10.7626, 106.6602

    # API 1: Air Quality (Chỉ có Hourly)
    aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10,european_aqi&start_date={api_date}&end_date={api_date}"
    
    # API 2: Weather 
    uv_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=uv_index_max&timezone=Asia/Bangkok&start_date={api_date}&end_date={api_date}"

    try:
        # Lấy dữ liệu không khí
        aq_res = requests.get(aq_url)
        aq_res.raise_for_status()
        aq_hourly = aq_res.json()['hourly']
        
        aqi_val = sum(aq_hourly['european_aqi']) / len(aq_hourly['european_aqi'])
        pm25_val = sum(aq_hourly['pm2_5']) / len(aq_hourly['pm2_5'])

        # Lấy dữ liệu UV 
        uv_res = requests.get(uv_url)
        uv_res.raise_for_status()
        uv_val = uv_res.json()['daily']['uv_index_max'][0]

        # Tổng hợp
        new_data = pd.DataFrame({
            'Ngày': [display_date],
            'AQI (Avg)': [round(aqi_val, 2)],
            'PM2.5 (Avg)': [round(pm25_val, 2)],
            'UV Index (Daily Direct)': [uv_val]
        })

        file_name = 'hcm_air_quality_log.xlsx'
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã cập nhật thành công ngày {display_date}")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
