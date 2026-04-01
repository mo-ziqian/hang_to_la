import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random

class HangToLaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("从夯到拉")
        # 设置窗口大小为更加紧凑的尺寸
        self.root.geometry("1200x800")
        
        # 加载背景图片
        self.bg_image = Image.open("hang_to_la.jpg")
        self.bg_width, self.bg_height = self.bg_image.size
        
        # 缩放图片以适应窗口
        self.scale_factor = min(800 / self.bg_width, 600 / self.bg_height)
        self.scaled_width = int(self.bg_width * self.scale_factor)
        self.scaled_height = int(self.bg_height * self.scale_factor)
        self.scaled_bg = self.bg_image.resize((self.scaled_width, self.scaled_height), Image.Resampling.LANCZOS)
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, width=self.scaled_width, height=self.scaled_height, bg="white", bd=2, relief="groove")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 显示背景图片
        self.bg_photo = ImageTk.PhotoImage(self.scaled_bg)
        self.bg_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        
        # 存储添加的文本项
        self.text_items = []
        
        # 创建控制面板，使用Notebook实现标签页
        self.control_frame = ttk.Notebook(self.root, width=350, height=600)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        
        # 创建第一个标签页：基本设置
        self.basic_tab = ttk.Frame(self.control_frame)
        self.control_frame.add(self.basic_tab, text="基本设置")
        
        # 内容输入
        ttk.Label(self.basic_tab, text="输入内容:").pack(anchor=tk.W, pady=(10, 5))
        self.content_entry = ttk.Entry(self.basic_tab, width=40)
        self.content_entry.pack(pady=5, fill=tk.X)
        
        # 评分方式选择
        ttk.Label(self.basic_tab, text="评分方式:").pack(anchor=tk.W, pady=(15, 5))
        self.score_mode = tk.StringVar(value="slider")  # slider或level
        
        # 创建评分方式选择框架
        score_mode_frame = ttk.Frame(self.basic_tab)
        score_mode_frame.pack(pady=5, fill=tk.X)
        
        # 滑动分数选项
        ttk.Radiobutton(score_mode_frame, text="滑动分数 (0-10)", variable=self.score_mode, value="slider", command=self.toggle_score_mode).pack(anchor=tk.W, padx=5)
        
        # 五级制度选项
        ttk.Radiobutton(score_mode_frame, text="五级制度", variable=self.score_mode, value="level", command=self.toggle_score_mode).pack(anchor=tk.W, padx=5)
        
        # 滑动分数控件
        self.slider_frame = ttk.Frame(self.basic_tab)
        ttk.Label(self.slider_frame, text="分数 (0-10):").pack(anchor=tk.W, pady=(10, 5))
        
        # 创建滑块变量，范围0-100对应0-10分
        self.score_scale_var = tk.IntVar(value=50)  # 初始值50对应5.0分
        self.score_scale = ttk.Scale(self.slider_frame, from_=0, to=100, variable=self.score_scale_var, orient=tk.HORIZONTAL, length=280)
        self.score_scale.pack(pady=5, fill=tk.X)
        
        # 创建内部变量来存储实际分数值
        self._internal_score = 5.0
        self.score_label = ttk.Label(self.slider_frame, text=f"{self._internal_score:.1f}")
        self.score_label.pack()
        self.slider_frame.pack(pady=5, fill=tk.X)
        
        # 绑定分数变化事件，手动处理分辨率
        self.score_scale.bind("<Motion>", self.update_score_with_resolution)
        self.score_scale.bind("<ButtonRelease-1>", self.update_score_with_resolution)
        
        # 五级制度控件
        self.level_frame = ttk.Frame(self.basic_tab)
        ttk.Label(self.level_frame, text="五级制度:").pack(anchor=tk.W, pady=(10, 5))
        self.level_var = tk.StringVar(value="3")  # 默认NPC
        
        # 创建五级制度选择框架
        level_buttons_frame = ttk.Frame(self.level_frame)
        level_buttons_frame.pack(pady=5, fill=tk.X)
        
        # 五级按钮
        levels = [
            ("夯", "4"),
            ("顶级", "3"),
            ("人上人", "2"),
            ("NPC", "1"),
            ("拉完了", "0")
        ]
        
        for i, (level_name, level_value) in enumerate(levels):
            ttk.Radiobutton(level_buttons_frame, text=level_name, variable=self.level_var, value=level_value).pack(anchor=tk.W, padx=5, pady=2)
        
        self.level_frame.pack(pady=5, fill=tk.X)
        self.level_frame.pack_forget()  # 初始隐藏五级制度框架
        
        # 创建第二个标签页：字体设置
        self.font_tab = ttk.Frame(self.control_frame)
        self.control_frame.add(self.font_tab, text="字体设置")
        
        # 字体大小
        ttk.Label(self.font_tab, text="字体大小:").pack(anchor=tk.W, pady=(10, 5))
        self.font_size_var = tk.IntVar(value=24)
        self.font_size_spinbox = ttk.Spinbox(self.font_tab, from_=12, to=72, textvariable=self.font_size_var, width=35)
        self.font_size_spinbox.pack(pady=5, fill=tk.X)
        
        # 字体颜色
        ttk.Label(self.font_tab, text="字体颜色:").pack(anchor=tk.W, pady=(15, 5))
        self.font_color_var = tk.StringVar(value="#000000")
        
        color_frame = ttk.Frame(self.font_tab)
        color_frame.pack(pady=5, fill=tk.X)
        
        self.color_button = ttk.Button(color_frame, text="选择颜色", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 预览颜色
        self.color_preview = tk.Frame(color_frame, width=100, height=25, bg=self.font_color_var.get(), bd=2, relief="solid")
        self.color_preview.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 创建第三个标签页：操作
        self.action_tab = ttk.Frame(self.control_frame)
        self.control_frame.add(self.action_tab, text="操作")
        
        # 操作按钮，设置统一的宽度
        button_width = 20
        
        self.add_button = ttk.Button(self.action_tab, text="添加内容", command=self.add_content, width=button_width)
        self.add_button.pack(pady=10, fill=tk.X)
        
        self.clear_button = ttk.Button(self.action_tab, text="清空所有", command=self.clear_all, width=button_width)
        self.clear_button.pack(pady=10, fill=tk.X)
        
        self.export_button = ttk.Button(self.action_tab, text="导出图片", command=self.export_image, width=button_width)
        self.export_button.pack(pady=10, fill=tk.X)
        
        # 已经在前面绑定了分数变化事件，这里不再重复绑定
        
        # 初始化文本项存储
        self.texts = []
        
    def update_score_with_resolution(self, event):
        """手动处理分辨率的分数更新"""
        # 获取滑块的原始值（0-100）
        raw_value = self.score_scale_var.get()
        
        # 转换为0-10的范围，分辨率为0.1
        self._internal_score = round(raw_value / 10.0, 1)
        
        # 更新显示
        self.score_label.config(text=f"{self._internal_score:.1f}")
    
    def toggle_score_mode(self):
        """切换评分方式"""
        mode = self.score_mode.get()
        if mode == "slider":
            self.slider_frame.pack(pady=5, fill=tk.X)
            self.level_frame.pack_forget()
        else:
            self.slider_frame.pack_forget()
            self.level_frame.pack(pady=5, fill=tk.X)
        
    def choose_color(self):
        """选择字体颜色"""
        color = colorchooser.askcolor(initialcolor=self.font_color_var.get())
        if color[1]:
            self.font_color_var.set(color[1])
            self.color_preview.config(bg=color[1])
    
    def add_content(self):
        """添加内容到图片，支持两种评分方式"""
        content = self.content_entry.get().strip()
        if not content:
            return
        
        # 根据评分方式获取分数
        mode = self.score_mode.get()
        if mode == "slider":
            # 直接从滑块变量获取最新值，确保使用的是当前设置的分数
            raw_value = self.score_scale_var.get()
            score = round(raw_value / 10.0, 1)
        else:
            # 五级制度转换为分数范围
            level = self.level_var.get()
            if level == "4":  # 夯
                score = random.uniform(8.0, 10.0)
            elif level == "3":  # 顶级
                score = random.uniform(6.0, 8.0)
            elif level == "2":  # 人上人
                score = random.uniform(4.0, 6.0)
            elif level == "1":  # NPC
                score = random.uniform(2.0, 4.0)
            else:  # 拉完了
                score = random.uniform(0.0, 2.0)
        
        font_size = self.font_size_var.get()
        font_color = self.font_color_var.get()
        
        # 根据评分分配区域
        area = self.get_area_by_score(score)
        
        # 生成不重叠的位置
        x, y = self.generate_position(area, content, font_size)
        
        # 在画布上添加文本
        text_id = self.canvas.create_text(x, y, text=content, fill=font_color, font=("Arial", font_size), anchor=tk.CENTER)
        
        # 存储文本信息
        self.texts.append({
            "content": content,
            "score": score,
            "font_size": font_size,
            "font_color": font_color,
            "position": (x, y)
        })
        
        # 清空输入框
        self.content_entry.delete(0, tk.END)
    
    def get_area_by_score(self, score):
        """根据评分获取区域，确保与图片边界精确对齐"""
        # 将图片高度平均分成五个部分，使用整数边界以避免精度问题
        part_height = self.scaled_height // 5
        
        # 严格按照评分范围划分区域
        if 0 <= score < 2:
            # 拉完了：底部第1部分 (0-2分) - 精确到图片底部边缘
            return (0, self.scaled_height - part_height, self.scaled_width, self.scaled_height)
        elif 2 <= score < 4:
            # NPC：底部第2部分 (2-4分)
            return (0, self.scaled_height - 2 * part_height, self.scaled_width, self.scaled_height - part_height)
        elif 4 <= score < 6:
            # 人上人：中间第3部分 (4-6分)
            return (0, self.scaled_height - 3 * part_height, self.scaled_width, self.scaled_height - 2 * part_height)
        elif 6 <= score < 8:
            # 顶级：上部第4部分 (6-8分)
            return (0, self.scaled_height - 4 * part_height, self.scaled_width, self.scaled_height - 3 * part_height)
        else:  # 8 <= score <= 10
            # 夯：顶部第5部分 (8-10分) - 精确到图片顶部边缘
            return (0, 0, self.scaled_width, self.scaled_height - 4 * part_height)
    
    def generate_position(self, area, content, font_size):
        """生成不重叠的位置，避免与左侧标签重叠"""
        area_x1, area_y1, area_x2, area_y2 = area
        
        # 创建一个临时的ImageDraw对象来计算文本大小
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # 计算文本的实际宽度和高度
        text_bbox = temp_draw.textbbox((0, 0), content, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 计算左侧标签区域的宽度（约占图片宽度的1/4）
        label_width = int(self.scaled_width * 0.25)
        
        max_attempts = 200
        for attempt in range(max_attempts):
            # 确保文本完全在图片范围内，并且不与左侧标签重叠
            x_min = int(max(label_width + text_width // 2, text_width // 2))
            x_max = int(self.scaled_width - text_width // 2)
            y_min = int(text_height // 2)
            y_max = int(self.scaled_height - text_height // 2)
            
            # 限制在指定区域内
            x_min = max(x_min, int(area_x1 + text_width // 2))
            x_max = min(x_max, int(area_x2 - text_width // 2))
            y_min = max(y_min, int(area_y1 + text_height // 2))
            y_max = min(y_max, int(area_y2 - text_height // 2))
            
            # 确保范围有效
            if x_min >= x_max or y_min >= y_max:
                x_min = int(max(label_width + text_width // 2, text_width // 2))
                x_max = int(self.scaled_width - text_width // 2)
                y_min = max(int(text_height // 2), int(area_y1))
                y_max = min(int(self.scaled_height - text_height // 2), int(area_y2))
            
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            
            # 检查是否与现有文本重叠
            overlap = False
            for text in self.texts:
                tx, ty = text["position"]
                t_content = text["content"]
                t_size = text["font_size"]
                
                try:
                    t_font = ImageFont.truetype("arial.ttf", t_size)
                except IOError:
                    t_font = ImageFont.load_default()
                
                t_bbox = temp_draw.textbbox((0, 0), t_content, font=t_font)
                t_width = t_bbox[2] - t_bbox[0]
                t_height = t_bbox[3] - t_bbox[1]
                
                # 检查边界框是否重叠
                if (abs(x - tx) < (text_width + t_width) // 2 and 
                    abs(y - ty) < (text_height + t_height) // 2):
                    overlap = True
                    break
            
            if not overlap:
                return x, y
        
        # 如果尝试多次后仍未找到位置，返回随机位置
        return (random.randint(area_x1 + text_width//2, area_x2 - text_width//2), 
                random.randint(area_y1 + text_height//2, area_y2 - text_height//2))
    
    def clear_all(self):
        """清空所有添加的文本"""
        # 删除画布上所有非背景图片的元素
        for item in self.canvas.find_all():
            if item != self.bg_image_id:  # 检查是否是背景图片
                self.canvas.delete(item)
        self.texts = []
    
    def export_image(self):
        """导出图片"""
        # 创建新图片用于导出
        export_image = self.bg_image.copy()
        draw = ImageDraw.Draw(export_image)
        
        # 添加所有文本到图片
        for text in self.texts:
            content = text["content"]
            x, y = text["position"]
            # 转换回原始图片的坐标
            orig_x = int(x / self.scale_factor)
            orig_y = int(y / self.scale_factor)
            font_size = text["font_size"]
            font_color = text["font_color"]
            
            # 设置字体
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
            
            # 绘制文本
            draw.text((orig_x, orig_y), content, fill=font_color, font=font, anchor="mm")
        
        # 保存图片
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG图片", "*.jpg"), ("PNG图片", "*.png"), ("所有文件", "*.*")],
            initialfile="hang_to_la_result"
        )
        
        if file_path:
            export_image.save(file_path)
            tk.messagebox.showinfo("导出成功", "图片已成功导出！")

if __name__ == "__main__":
    root = tk.Tk()
    app = HangToLaApp(root)
    root.mainloop()