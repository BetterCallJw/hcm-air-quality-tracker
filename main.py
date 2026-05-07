import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_hourly_air_quality():
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Lấy ngày hôm qua
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')

    latitude = 10.7626
    longitude = 106.6602

    # Lấy dữ liệu HOURLY (Chỉ số Mỹ US AQI và PM2.5)
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm2_5,us_aqi&start_date={api_date}&end_date={api_date}&timezone=Asia%2FBangkok"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        times = data['hourly']['time']
        pm25_list = data['hourly']['pm2_5']
        us_aqi_list = data['hourly']['us_aqi']

        formatted_times = [t.replace('T', ' ') for t in times]

        # Tạo DataFrame
        new_data = pd.DataFrame({
            'Thời gian': formatted_times,
            'US AQI': us_aqi_list,
            'PM2.5 (µg/m³)': pm25_list
        })

        # Đổi tên file để tránh nhầm lẫn với file trung bình cũ
        file_name = 'hcm_hourly_air_quality.xlsx'

        # Ghi nối tiếp 24 dòng vào file Excel
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã cập nhật thành công 24 giờ của ngày {api_date}")

    except Exception as e:
        print(f"Có lỗi: {e}")

if __name__ == "__main__":
    fetch_hourly_air_quality()
