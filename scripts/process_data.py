import os
import pandas as pd


def parse_weather(entry):
    """
    Parse a single weather entry into a structured format.

    Args:
        entry (dict): A dictionary containing weather data.

    Returns:
        dict: A dictionary with parsed weather data including datetime, temperature, humidity,
              wind speed, and weather description. Returns None if the entry is None.
    """
    if entry is None:
        return None
    return {
        'Datetime': pd.to_datetime(entry['dt'], unit='s'),
        'Temperature (C)': entry['main']['temp'] - 273.15,
        'Humidity (%)': entry['main']['humidity'],
        'Wind Speed (m/s)': entry['wind']['speed'],
        'Weather': entry['weather'][0]['description']
    }


def save_to_csv(data, filename):
    """
    Save a list of dictionaries to a CSV file.

    Args:
        data (list): A list of dictionaries containing data to save.
        filename (str): The name of the file to save the data to.

    Returns:
        None
    """
    if data is None:
        print(f"No data to save for {filename}")
        return
    # 构建上级目录中的 data 文件夹路径
    target_folder = os.path.join(os.pardir, 'data','processed')
    # 规范化路径，确保在不同操作系统上路径格式正确
    target_folder = os.path.normpath(target_folder)
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    # 构建新的文件路径，将目标文件夹和原文件名组合
    new_file_path = os.path.join(target_folder, filename)
    df = pd.DataFrame(data)
    # 使用新的文件路径保存数据到 CSV 文件
    df.to_csv(new_file_path, index=False)


def calculate_daily_stats(forecast_data):
    """
    Calculate daily statistics from forecast data.

    Args:
        forecast_data (list): A list of dictionaries containing forecast data.

    Returns:
        pd.DataFrame: A DataFrame containing daily minimum and maximum temperature, humidity, and wind speed.
                      Returns None if the forecast data is None.
    """
    if forecast_data is None:
        return None

    df_forecast = pd.DataFrame(forecast_data)
    df_forecast['Date'] = df_forecast['Datetime'].dt.date

    daily_stats = df_forecast.groupby('Date').agg({
        'Temperature (C)': ['min', 'max'],
        'Humidity (%)': ['min', 'max'],
        'Wind Speed (m/s)': ['min', 'max']
    })

    daily_stats.columns = ['Min Temperature (C)', 'Max Temperature (C)', 
                           'Min Humidity (%)', 'Max Humidity (%)', 
                           'Min Wind Speed (m/s)', 'Max Wind Speed (m/s)']

    daily_stats.reset_index(inplace=True)

    return daily_stats


def process_weather_data(current_data, forecast_data):
    """
    Process current and forecast weather data, save to CSV files, and calculate daily statistics.

    Args:
        current_data (dict): A dictionary containing current weather data.
        forecast_data (dict): A dictionary containing forecast weather data.

    Returns:
        tuple: A tuple containing three elements:
            - pd.DataFrame: A DataFrame containing the current weather data.
            - pd.DataFrame: A DataFrame containing the hourly forecast weather data.
            - pd.DataFrame: A DataFrame containing the daily weather statistics.
    """
    current_weather = parse_weather(current_data)
    forecast_weather = [parse_weather(entry) for entry in forecast_data['list']]

    save_to_csv([current_weather], 'current_weather_data.csv')
    save_to_csv(forecast_weather, 'hourly_weather_data.csv')

    daily_stats = calculate_daily_stats(forecast_weather)
    save_to_csv(daily_stats, 'daily_weather_stats.csv')

    return pd.DataFrame([current_weather]), pd.DataFrame(forecast_weather), daily_stats
