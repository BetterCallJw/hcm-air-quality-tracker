import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz
import time

def fetch_and_log_air_quality():
    # 1. Thiết lập múi giờ Việt Nam
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Định dạng ngày cho API (YYYY-MM-DD) và Excel (dd mm yyyy)
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    latitude = 10.7626
    longitude = 106.6602

    # 2. Call API
    # Lấy Max cho AQI/UV và Mean cho các loại nồng độ chất
    daily_params = [
        "european_aqi_max",
        "pm2_5_mean",
        "pm10_mean",
        "nitrogen_dioxide_mean",
        "sulphur_dioxide_mean",
        "carbon_monoxide_mean",
        "uv_index_max"
    ]
    
    params_str = ",".join(daily_params)
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&daily={params_str}&start_date={api_date}&end_date={api_date}&timezone=Asia%2FBangkok"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['daily']

        # 3. Trích xuất dữ liệu (Chỉ lấy phần tử đầu tiên [0] vì kết quả daily trả về 1 giá trị/ngày)
        row_data = {'Ngày': display_date}
        for p in daily_params:
            row_data[p] = data[p][0]

        new_data = pd.DataFrame([row_data])

        # Đổi tên cột cho dễ hiểu
        new_data.columns = [
            'Ngày', 'AQI (Max)', 'PM2.5 (Mean)', 'PM10 (Mean)', 
            'NO2 (Mean)', 'SO2 (Mean)', 'CO (Mean)', 'UV Index (Max)'
        ]

        file_name = 'hcm_air_quality_log.xlsx'

        # 4. Ghi nối tiếp vào file Excel
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã cập nhật thành công dữ liệu trực tiếp ngày {display_date}")
        
        # Khoảng nghỉ trước khi kết thúc
        time.sleep(60) 

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
