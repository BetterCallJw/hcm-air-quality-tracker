import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz

def fetch_and_log_air_quality():
    # 1. Thiết lập múi giờ Việt Nam
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Định dạng ngày
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    latitude, longitude = 10.7626, 106.6602

    # 2. Call API
    daily_params = [
        "european_aqi_max", 
        "pm2_5_max", 
        "pm10_max", 
        "nitrogen_dioxide_max", 
        "sulphur_dioxide_max", 
        "carbon_monoxide_max", 
        "uv_index_max"
    ]
    
    params_str = ",".join(daily_params)
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&daily={params_str}&start_date={api_date}&end_date={api_date}&timezone=Asia%2FBangkok"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if 'daily' not in data:
        print("Không tìm thấy dữ liệu 'daily' trong phản hồi.")
        return

    daily_data = data['daily']

    # 3. Trích xuất dữ liệu
    row_data = {'Ngày': display_date}
    for p in daily_params:
        row_data[p] = daily_data[p][0]

    new_data = pd.DataFrame([row_data])
    
    new_data.columns = [
        'Ngày', 'AQI (Max)', 'PM2.5 (Max)', 'PM10 (Max)', 
        'NO2 (Max)', 'SO2 (Max)', 'CO (Max)', 'UV Index (Max)'
    ]

    file_name = 'hcm_air_quality_log.xlsx'

    # 4. Ghi nối tiếp vào file Excel
    if os.path.exists(file_name):
        existing_data = pd.read_excel(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_excel(file_name, index=False)
    print(f"Đã cập nhật thành công dữ liệu ngày {display_date}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
