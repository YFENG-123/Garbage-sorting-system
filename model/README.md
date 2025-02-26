# update the model

## Requirements:
- ncnn==1.0.20240820
- ultralytics==8.3.19

## quick start
- 虚拟环境搭建，与完整项目一致
     ```
    conda create -n <envname> python=3.11.10
    conda activate <envname>
    pip install -r requirements.txt
     ``` 
- requirements.txt 出现error,查看是否有所需环境
     ```
    pip show ultralytics
    pip show ncnn
     ``` 
- 若没有，单独下载所需环境
     ```
    pip install ultralytics==8.3.19
    pip install ncnn==1.0.20240820
     ``` 
- 导出模型为 NCNN 格式
     ```
    python export.py
     ``` 
