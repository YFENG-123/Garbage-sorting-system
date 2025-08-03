import tkinter as tk
from PIL import Image, ImageTk

class ImageList(tk.Frame):
    def __init__(self, parent, headers, column_widths=None, row_height=40, min_width=500, min_height=800):
        """
        初始化图片列表组件
        
        Args:
            parent: 父容器
            headers: 表头图片路径列表，四张图片的路径
            column_widths: 每列宽度列表 [col1_width, col2_width, col3_width, col4_width]
            row_height: 每行高度（不包括边框和间距）
            min_width: 组件最小宽度
            min_height: 组件最小高度
        """
        super().__init__(parent)
        self.column_widths = column_widths or [64, 64, 64, 64]  # 默认列宽
        self.row_height = row_height  # 每行高度
        self.min_width = min_width
        self.min_height = min_height
        
        # 设置自身的最小尺寸
        self.config(width=self.min_width, height=self.min_height)
        
        # 创建固定表头
        self.header_frame = tk.Frame(self, bd=2, relief="groove")
        self.header_frame.pack(side="top", fill="x")
        self.create_header(headers)
        
        # 创建主体区域（包含滚动列表）
        body_container = tk.Frame(self)
        body_container.pack(side="top", fill="both", expand=True)
        
        # 确保主体区域填充空间
        body_container.grid_rowconfigure(0, weight=1)
        body_container.grid_columnconfigure(0, weight=1)
        
        # 创建主画布和滚动条
        self.canvas = tk.Canvas(body_container)
        self.scrollbar = tk.Scrollbar(body_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # 创建内部容器框架
        self.items_frame = tk.Frame(self.canvas)
        self.items_frame_id = self.canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
        
        # 绑定配置事件
        self.items_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # 跟踪当前项目列表
        self.items = []
    
    def create_header(self, header_paths):
        """创建固定表头行，每列为一张图片"""
        # 验证输入的图片路径数量
        if len(header_paths) != 4:
            raise ValueError("表头必须包含4张图片路径")
        
        # 配置表头布局权重
        for col in range(4):
            self.header_frame.grid_columnconfigure(
                col, 
                weight=1, 
                minsize=self.column_widths[col]  # 设置最小列宽
            )
        
        # 加载并添加四列图片
        for col, path in enumerate(header_paths):
            try:
                pil_img = Image.open(path)
                # 调整图片大小为列宽的一半和高度的70%，保持比例
                height = int(self.row_height)
                pil_img.thumbnail((self.column_widths[col] , height))
                tk_img = ImageTk.PhotoImage(pil_img)
                label = tk.Label(
                    self.header_frame, 
                    image=tk_img, 
                    width=self.column_widths[col],
                    height=self.row_height
                )
                label.image = tk_img  # 保持引用
                label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            except Exception as e:
                print(f"无法加载表头图片: {path}, 错误: {e}")
                tk.Label(
                    self.header_frame, 
                    text=f"Header {col+1}", 
                    font=("Arial", 10, "bold"),
                    width=self.column_widths[col],
                    height=self.row_height
                ).grid(row=0, column=col, sticky="nsew")
    
    def on_frame_configure(self, event):
        """更新画布的滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """调整内部框架宽度以适应画布并确保最小尺寸"""
        # 确保宽度不小于最小值
        calculated_width = max(self.min_width, event.width)
        self.canvas.itemconfigure(self.items_frame_id, width=calculated_width)
    def add_item(self, text1, photo1, text2, photo2):
        """
        添加列表项（插入到顶部）
        
        Args:
            text1: 第一列文本（可以是字符串或数字）
            photo1: 第二列的ImageTk.PhotoImage对象
            text2: 第三列文本（可以是字符串或数字）
            photo2: 第四列的ImageTk.PhotoImage对象
        """
        # 创建列表项容器
        item_frame = tk.Frame(
            self.items_frame, 
            bd=1, 
            relief="groove",
            height=self.row_height  # 设置行高度
        )
        item_frame.pack_propagate(False)  # 阻止内容改变框架大小
        
        # 将所有已有项下移一行（使用保存的引用列表）
        for i, (item, row) in enumerate(self.items):
            # 更新网格位置
            item.grid(row=i + 1)
            # 更新内部存储的行号
            self.items[i] = (item, i + 1)
        
        # 将新项添加到列表顶部（第0行）
        item_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        # 插入到列表开头
        self.items.insert(0, (item_frame, 0))
        
        # 配置四列权重相等
        for col in range(4):
            item_frame.grid_columnconfigure(
                col, 
                weight=1, 
                minsize=self.column_widths[col]  # 设置最小列宽
            )
        
        # 第一列: 文本
        # 确保文本是字符串类型
        text1_str = str(text1)
        # 设置最大宽度为列宽减20（避免内容溢出）
        text1_label = tk.Label(
            item_frame, 
            text=text1_str, 
            font=("Arial", 11),
            anchor="center",
            wraplength=self.column_widths[0] ,  # 设置自动换行
            justify="left"
        )
        text1_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # 第二列: 图片
        if photo1 is not None:
            # 设置图片容器框架
            img_frame1 = tk.Frame(
                item_frame, 
                width=self.column_widths[1],
                height=self.row_height
            )
            img_frame1.pack_propagate(False)  # 保持固定大小
            img_frame1.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
            
            img_label1 = tk.Label(img_frame1, image=photo1)
            img_label1.image = photo1  # 保持引用
            img_label1.pack(expand=True)  # 在容器中居中显示
        else:
            error_label1 = tk.Label(
                item_frame, 
                text="[Image Error]", 
                font=("Arial", 9), 
                fg="red",
                anchor="center"
            )
            error_label1.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # 第三列: 文本
        # 确保文本是字符串类型
        text2_str = str(text2)
        text2_label = tk.Label(
            item_frame, 
            text=text2_str, 
            font=("Arial", 11),
            anchor="center",
            wraplength=self.column_widths[2],  # 设置自动换行
            justify="left"
        )
        text2_label.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        
        # 第四列: 图片
        if photo2 is not None:
            img_frame2 = tk.Frame(
                item_frame, 
                width=self.column_widths[3],
                height=self.row_height
            )
            img_frame2.pack_propagate(False)  # 保持固定大小
            img_frame2.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")
            
            img_label2 = tk.Label(img_frame2, image=photo2)
            img_label2.image = photo2  # 保持引用
            img_label2.pack(expand=True)  # 在容器中居中显示
        else:
            error_label2 = tk.Label(
                item_frame, 
                text="[Image Error]", 
                font=("Arial", 9), 
                fg="red",
                anchor="center"
            )
            error_label2.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

# 使用示例
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("四列图片列表（带列宽控制）")
#     root.geometry("800x500")
    
#     # 表头图片路径 (应替换为实际图片路径)
#     headers = [
#         "gui_images/food_waste_logo.png",
#         "gui_images/food_waste_logo.png",
#         "gui_images/food_waste_logo.png",
#         "gui_images/food_waste_logo.png"
#     ]
    
#     # 定义列宽 [文本列1, 图片列1, 文本列2, 图片列2]
#     column_widths = [200, 100, 200, 100]
#     row_height = 50
    
#     # 创建带列宽控制的列表
#     image_list = ImageList(root, headers, column_widths=column_widths, row_height=row_height)
#     image_list.pack(fill="both", expand=True, padx=10, pady=10)
    
#     # 在外部加载图片并创建PhotoImage对象
#     def load_image(path, target_width=None, target_height=None):
#         try:
#             pil_img = Image.open(path)
#             if target_width and target_height:
#                 pil_img = pil_img.resize((target_width, target_height))
#             return ImageTk.PhotoImage(pil_img)
#         except:
#             return None
    
#     # 加载图片，调整到对应列的大小
#     img_col1 = load_image("gui_images/food_waste_logo.png", column_widths[1]-10, row_height-10)
#     img_col2 = load_image("gui_images/food_waste_logo.png", column_widths[3]-10, row_height-10)
    
#     # 长文本示例
#     long_text = "这是一个较长的文本示例，它将自动换行以适应列的宽度设置"
    
#     # 添加初始数据（包含整数和字符串）
#     image_list.add_item(1, img_col1, "描述 A", img_col2)  # 整数作为文本
#     image_list.add_item("条目 2", None, 12345, img_col2)  # 整数作为文本
#     image_list.add_item(long_text, img_col1, long_text, img_col2)
    
#     # 添加按钮用于测试添加新项
#     counter = 4
#     test_button = tk.Button(root, text="添加新项", command=lambda: [
#         image_list.add_item(
#             f"新项 {counter}", 
#             img_col1 if counter % 2 else None, 
#             counter,  # 整数作为文本
#             img_col2 if counter % 3 else None
#         ),
#         counter := counter + 1
#     ])
#     test_button.pack(pady=10)
    
#     root.mainloop()