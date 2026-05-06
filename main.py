import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz
import time # Thêm thư viện time

def fetch_and_log_air_quality():
    # 1. Múi giờ Việt Nam
    vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vn_time_now = datetime.now(vn_timezone)
    
    # Biến dùng để gọi API (Định dạng bắt buộc YYYY-MM-DD)
    api_date = (vn_time_now - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Biến hiển thị trong Excel (Định dạng dd MM yyyy)
    display_date = (vn_time_now - timedelta(days=1)).strftime('%d %m %Y')

    latitude = 10.7626
    longitude = 106.6602

    # 2. Call API
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm2_5,european_aqi&start_date={api_date}&end_date={api_date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        pm25_list = [x for x in data['hourly']['pm2_5'] if x is not None]
        aqi_list = [x for x in data['hourly']['european_aqi'] if x is not None]

        pm25_avg = sum(pm25_list) / len(pm25_list) if pm25_list else 0
        aqi_avg = sum(aqi_list) / len(aqi_list) if aqi_list else 0

        # 3. Tạo DataFrame (Sử dụng display_date)
        new_data = pd.DataFrame({
            'Ngày': [display_date],
            'AQI Trung bình': [round(aqi_avg, 2)],
            'PM2.5 Trung bình (µg/m³)': [round(pm25_avg, 2)]
        })

        file_name = 'hcm_air_quality_log.xlsx'

        # 4. Ghi đè hoặc tạo mới Excel
        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(file_name, index=False)
        print(f"Đã cập nhật thành công dữ liệu ngày {display_date}")
        
        # Thêm khoảng nghỉ 5 phút (300 giây) sau khi thực thi xong
        time.sleep(300) 

    except Exception as e:
        print(f"Có lỗi: {e}")

if __name__ == "__main__":
    fetch_and_log_air_quality()
