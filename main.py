import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_hourly_air_quality():
    # 1. Khai báo múi giờ
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Lấy dữ liệu của ngày hôm qua
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')

    latitude = 10.7626
    longitude = 106.6602

    # 2. Call API
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm2_5,us_aqi&start_date={api_date}&end_date={api_date}&timezone=Asia%2FBangkok"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        times = data['hourly']['time']
        formatted_times = [t.replace('T', ' ') for t in times]

        # Trích xuất toàn bộ 24 giá trị
        pm25_list = data['hourly']['pm2_5']
        us_aqi_list = data['hourly']['us_aqi']

        # 3. DataFrame
        new_data = pd.DataFrame({
            'Thời gian': formatted_times,
            'US AQI': us_aqi_list,
            'PM2.5 (µg/m³)': pm25_list
        })

        file_name = 'hcm_air_quality_log.xlsx'

        # 4. Ghi nối tiếp vào file hoặc tạo mới
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        
        print(f"Đã xuất chi tiết 24 giờ của ngày {api_date} thành công!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    fetch_hourly_air_quality()
