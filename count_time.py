import time

def get_elapsed_time(start_time):
    """
    计算从 start_time 开始经过的时间，返回 "分:秒:毫秒" 格式的字符串。
    """
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
    return f"{minutes:02d}:{seconds:02d}'{milliseconds:02d}"

