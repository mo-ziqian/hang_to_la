from PIL import Image, ImageDraw, ImageFont
import random
import os

class HangToLaCLI:
    def __init__(self):
        # 加载背景图片
        self.bg_image = Image.open("hang_to_la.jpg")
        self.bg_width, self.bg_height = self.bg_image.size
        
        # 存储添加的文本项
        self.texts = []
    
    def get_area_by_score(self, score):
        """根据评分获取区域"""
        if 0 <= score <= 2:
            # 拉完了：底部区域
            return (0, self.bg_height * 0.7, self.bg_width, self.bg_height)
        elif 3 <= score <= 4:
            # NPC：中下部区域
            return (0, self.bg_height * 0.5, self.bg_width, self.bg_height * 0.7)
        elif 5 <= score <= 6:
            # 人上人：中部区域
            return (0, self.bg_height * 0.3, self.bg_width, self.bg_height * 0.5)
        elif 7 <= score <= 8:
            # 顶级：中上部区域
            return (0, self.bg_height * 0.1, self.bg_width, self.bg_height * 0.3)
        else:  # 9-10
            # 夯：上部区域
            return (0, 0, self.bg_width, self.bg_height * 0.1)
    
    def generate_position(self, area, content, font_size):
        """生成不重叠的位置"""
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
        
        max_attempts = 200
        for attempt in range(max_attempts):
            # 随机生成位置，确保文本完全在区域内
            x = random.randint(area_x1 + text_width//2, area_x2 - text_width//2)
            y = random.randint(area_y1 + text_height//2, area_y2 - text_height//2)
            
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
    
    def add_content(self, content, score, font_size=24, font_color="#000000"):
        """添加内容到图片"""
        if not content:
            return
        
        # 根据评分分配区域
        area = self.get_area_by_score(score)
        
        # 生成不重叠的位置
        x, y = self.generate_position(area, content, font_size)
        
        # 存储文本信息
        self.texts.append({
            "content": content,
            "score": score,
            "font_size": font_size,
            "font_color": font_color,
            "position": (x, y)
        })
        
        print(f"已添加: {content} (评分: {score}, 位置: ({x}, {y}))")
    
    def export_image(self, output_path="hang_to_la_result.jpg"):
        """导出图片"""
        # 创建新图片用于导出
        export_image = self.bg_image.copy()
        draw = ImageDraw.Draw(export_image)
        
        # 添加所有文本到图片
        for text in self.texts:
            content = text["content"]
            x, y = text["position"]
            font_size = text["font_size"]
            font_color = text["font_color"]
            
            # 设置字体
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
            
            # 绘制文本
            draw.text((x, y), content, fill=font_color, font=font, anchor="mm")
        
        # 保存图片
        export_image.save(output_path)
        print(f"图片已导出到: {output_path}")
        return output_path

def main():
    print("=== 从夯到拉 命令行工具 ===")
    print()
    
    app = HangToLaCLI()
    
    while True:
        print("1. 添加内容")
        print("2. 导出图片")
        print("3. 退出")
        
        choice = input("请选择操作 (1-3): ").strip()
        
        if choice == "1":
            content = input("请输入内容: ").strip()
            if not content:
                print("内容不能为空！")
                continue
            
            score_input = input("请输入评分 (0-10): ").strip()
            try:
                score = int(score_input)
                if not 0 <= score <= 10:
                    raise ValueError("评分必须在0-10之间")
            except ValueError:
                print("请输入有效的评分 (0-10)！")
                continue
            
            size_input = input("请输入字体大小 (默认24): ").strip()
            try:
                font_size = int(size_input) if size_input else 24
                if font_size < 12 or font_size > 72:
                    font_size = 24
                    print("字体大小超出范围，已使用默认值24")
            except ValueError:
                font_size = 24
                print("请输入有效的字体大小，已使用默认值24")
            
            color_input = input("请输入颜色代码 (默认#000000): ").strip()
            font_color = color_input if color_input else "#000000"
            
            app.add_content(content, score, font_size, font_color)
            print()
            
        elif choice == "2":
            if not app.texts:
                print("还没有添加任何内容！")
                continue
            
            output_path = input("请输入输出文件名 (默认hang_to_la_result.jpg): ").strip()
            output_path = output_path if output_path else "hang_to_la_result.jpg"
            
            # 确保文件扩展名正确
            if not output_path.lower().endswith((".jpg", ".jpeg", ".png")):
                output_path += ".jpg"
            
            app.export_image(output_path)
            print()
            
        elif choice == "3":
            print("感谢使用！")
            break
        
        else:
            print("请选择有效的操作！")
            print()

if __name__ == "__main__":
    main()