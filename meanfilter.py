class MeanFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = [11.0,11.0,11.0,11.0,11.0]

    def update(self, new_value):
        # 将新值添加到窗口
        self.window.append(new_value)
        
        # 如果窗口大小超过设定的窗口大小，移除最旧的值
        if len(self.window) > self.window_size:
            self.window.pop(0)
        
        # 计算窗口内数值的平均值
        mean_value = sum(self.window) / len(self.window)
        
        return mean_value
    
    def clear_window(self):
        # 清空窗口
        self.window = [11.0,11.0,11.0,11.0,11.0]

# 示例使用
if __name__ == "__main__":
    window_size = 5  # 设置滑动窗口的大小
    mean_filter = MeanFilter(window_size)

    # 模拟实时输入信号
    input_signal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 对每个输入信号进行滤波
    for value in input_signal:
        filtered_value = mean_filter.update(value)
        print(f"Input: {value}, Filtered: {filtered_value}")