import pytest
import tkinter as tk
from tkinter import ttk
from scripts.create_dashboard import create_dashboard, update_weather


@pytest.fixture
def root():
    """
    提供一个 Tkinter 根窗口的测试夹具。

    在每个使用该夹具的测试函数执行前创建根窗口，测试结束后销毁。
    """
    root = tk.Tk()
    yield root
    root.destroy()


def test_create_dashboard(root):
    """
    测试 create_dashboard 函数是否正确创建了仪表盘 GUI。

    该函数应创建控制框架、绘图框架、城市选择下拉框、更新天气按钮，并初始化天气数据。
    """
    create_dashboard(root)

    # 检查控制框架是否正确创建
    control_frame = root.grid_slaves(row=0, column=0)[0]
    assert isinstance(control_frame, ttk.Frame)

    # 检查绘图框架是否正确创建
    plot_frame = root.grid_slaves(row=1, column=0)[0]
    assert isinstance(plot_frame, ttk.Frame)

    # 检查城市选择下拉框是否正确创建
    city_dropdown = control_frame.grid_slaves(row=0, column=0)[0]
    assert isinstance(city_dropdown, ttk.Combobox)

    # 检查更新天气按钮是否正确创建
    update_button = control_frame.grid_slaves(row=0, column=1)[0]
    assert isinstance(update_button, ttk.Button)


def test_update_weather(root):
    """
    测试 update_weather 函数是否正确更新天气数据和绘图。

    该函数应获取城市名称，调用 fetch_weather_data 和 process_weather_data 函数，
    确定天气状况，销毁旧的绘图部件，生成新的绘图，并将其添加到绘图框架中。
    """
    # 模拟 plot_frame 和 city_var
    plot_frame = ttk.Frame(root)
    plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    city_var = tk.StringVar(value='Sydney')

    # 模拟 fetch_weather_data 和 process_weather_data 函数
    from unittest.mock import patch

    with patch('scripts.create_dashboard.fetch_weather_data') as mock_fetch, \
            patch('scripts.create_dashboard.process_weather_data') as mock_process:

        update_weather(city_var, plot_frame)

        # 检查函数是否被调用
        mock_fetch.assert_called_once()
        mock_process.assert_called_once()
