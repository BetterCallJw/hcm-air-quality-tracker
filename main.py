import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_and_log_air_quality():
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Lấy ngày hôm qua
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    latitude = 10.7626
    longitude = 106.6602

    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm2_5,us_aqi&start_date={api_date}&end_date={api_date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Trích xuất dữ liệu 24 giờ
        pm25_list = [x for x in data['hourly']['pm2_5'] if x is not None]
        us_aqi_list = [x for x in data['hourly']['us_aqi'] if x is not None]

        # Tính trung bình cộng 
        pm25_avg = sum(pm25_list) / len(pm25_list) if pm25_list else 0
        us_aqi_avg = sum(us_aqi_list) / len(us_aqi_list) if us_aqi_list else 0

        # Tạo DataFrame
        new_data = pd.DataFrame({
            'Ngày': [display_date],
            'US AQI Trung bình': [round(us_aqi_avg, 2)],
            'PM2.5 Trung bình (µg/m³)': [round(pm25_avg, 2)]
        })

        file_name = 'hcm_air_quality_log.xlsx'

        # Ghi nối tiếp vào Excel
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã tính trung bình thành công dữ liệu ngày {display_date}")

    except Exception as e:
        print(f"Có lỗi: {e}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
