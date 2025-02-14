
import pytest
from scripts.utils import determine_weather, convert_temperature


def test_determine_weather():
    """
    Test the determine_weather function.

    This function tests the determine_weather function from the utils module.
    It checks different weather conditions based on temperature and humidity thresholds.

    Raises:
        AssertionError: If the output of the determine_weather function does not match the expected result.
    """
    # Test case for sunny weather
    row_sunny = {
        "Max Temperature (C)": 30,
        "Min Temperature (C)": 20,
        "Max Humidity (%)": 60
    }
    sunny_threshold = 25
    rainy_min_temp_threshold = 10
    rainy_humidity_threshold = 80
    expected_sunny = 'Sunny'
    result_sunny = determine_weather(
        row_sunny, sunny_threshold, rainy_min_temp_threshold, rainy_humidity_threshold
    )
    assert result_sunny == expected_sunny

    # Test case for rainy weather
    row_rainy = {
        "Max Temperature (C)": 20,
        "Min Temperature (C)": 5,
        "Max Humidity (%)": 90
    }
    expected_rainy = 'Rainy'
    result_rainy = determine_weather(
        row_rainy, sunny_threshold, rainy_min_temp_threshold, rainy_humidity_threshold
    )
    assert result_rainy == expected_rainy

    # Test case for partly cloudy weather
    row_partly_cloudy = {
        "Max Temperature (C)": 20,
        "Min Temperature (C)": 15,
        "Max Humidity (%)": 70
    }
    expected_partly_cloudy = 'Partly Cloudy'
    result_partly_cloudy = determine_weather(
        row_partly_cloudy, sunny_threshold, rainy_min_temp_threshold, rainy_humidity_threshold
    )
    assert result_partly_cloudy == expected_partly_cloudy


def test_convert_temperature():
    """
    Test the convert_temperature function.

    This function tests the convert_temperature function from the utils module.
    It checks the conversion of temperature from Kelvin to Celsius for different input values.

    Raises:
        AssertionError: If the output of the convert_temperature function does not match the expected result.
    """
    # Test case for 273.15 Kelvin (0 Celsius)
    kelvin_1 = 273.15
    expected_celsius_1 = 0.0
    result_celsius_1 = convert_temperature(kelvin_1)
    assert result_celsius_1 == expected_celsius_1

    # Test case for 0 Kelvin (-273.15 Celsius)
    kelvin_2 = 0
    expected_celsius_2 = -273.15
    result_celsius_2 = convert_temperature(kelvin_2)
    assert result_celsius_2 == expected_celsius_2

    # Test case for 373.15 Kelvin (100 Celsius)
    kelvin_3 = 373.15
    expected_celsius_3 = 100.0
    result_celsius_3 = convert_temperature(kelvin_3)
    assert result_celsius_3 == expected_celsius_3