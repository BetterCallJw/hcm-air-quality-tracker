import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_and_log_air_quality():
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    lat, lon = 10.7626, 106.6602

    # 1. Lấy dữ liệu không khí (Bắt buộc dùng HOURLY cho endpoint này)
    aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10,european_aqi,nitrogen_dioxide&start_date={api_date}&end_date={api_date}"
    
    # 2. Lấy dữ liệu UV (Endpoint này có hỗ trợ DAILY)
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=uv_index_max&timezone=Asia/Bangkok&start_date={api_date}&end_date={api_date}"

    try:
        # Xử lý Air Quality
        aq_res = requests.get(aq_url)
        aq_res.raise_for_status()
        aq_data = aq_res.json()['hourly']
        
        # Tính trung bình hoặc Max từ dữ liệu giờ (để có giá trị ngày)
        aqi_max = max(aq_data['european_aqi'])
        pm25_avg = sum(aq_data['pm2_5']) / len(aq_data['pm2_5'])

        # Xử lý UV
        w_res = requests.get(weather_url)
        w_res.raise_for_status()
        uv_max = w_res.json()['daily']['uv_index_max'][0]

        # 3. Tổng hợp vào DataFrame
        new_data = pd.DataFrame({
            'Ngày': [display_date],
            'AQI (Max)': [round(aqi_max, 2)],
            'PM2.5 (Avg)': [round(pm25_avg, 2)],
            'UV Index (Max)': [uv_max]
        })

        file_name = 'hcm_air_quality_log.xlsx'
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã cập nhật thành công dữ liệu ngày {display_date}")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
