# 从夯到拉 / From Hang to La

一个简单易用的图片生成工具，让你可以根据评分将内容实现快速导出“从夯到拉”图片之功能。

A simple and easy-to-use image generation tool that allows you to quickly export "From Hang to La" images based on ratings.

## 梗的历史 / History of the Meme

"从夯到拉" (From Hang to La) 是一种源自B站(哔哩哔哩)的网络流行文化现象，最初在电竞圈和短视频平台兴起。这个梗用"夯"(hāng)代表强大、厉害的状态，用"拉"(lā)代表拉胯、低级的状态，中间通过"顶级"、"人上人"、"NPC"等细分等级，形成了一个完整的评价体系。

"From Hang to La" is a popular internet culture phenomenon originating from Bilibili, initially emerging in the gaming community and short video platforms. This meme uses "Hang" (powerful, excellent) to represent strong status, and "La" (weak, inferior) to represent poor status, with intermediate levels like "Top Level", "Elite", "NPC" forming a complete evaluation system.

该梗通常用于对事物进行排名和分类，尤其是在音乐、电影、游戏等娱乐领域。用户可以将不同的内容按照自己的喜好和评价，放置在从"夯"到"拉"的不同等级区域中，形成直观的对比和展示。

The meme is commonly used for ranking and categorizing things, especially in entertainment fields like music, movies, and games. Users can place different contents in various level areas from "Hang" to "La" according to their preferences and evaluations, forming intuitive comparisons and displays.

## 功能特点 / Features

- **Two Rating Methods**
  - **Five-Level System**：夯 (Hang, 8-10), 顶级 (Top Level, 6-8), 人上人 (Elite, 4-6), NPC (2-4), 拉完了 (La, 0-2)
  - **Precise Rating**：0-10 slider with 0.1 precision

- **Customizable Font**
  - Adjustable font size (12-72)
  - Customizable font color

- **Smart Layout**
  - Automatic text size calculation
  - Avoid text overlapping
  - Ensure content stays within image boundaries

- **Image Export**
  - Export as JPG or PNG format
  - Preserve original image quality

## 安装方法 / Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hang-to-la.git
cd hang-to-la
```

### 2. Install Dependencies

```bash
pip install pillow
```

## 使用说明 / Usage

### GUI Version

#### 1. Launch the Program

```bash
python hang_to_la_app.py
```

#### 2. Basic Operations

1. **Input Content**：Enter the content you want to add in the input box on the "Basic Settings" tab

2. **Choose Rating Method**：
   - **Slider Rating**：Drag the slider to select a score between 0-10 (precision to 0.1)
   - **Five-Level System**：Directly select "夯" (Hang), "顶级" (Top Level), "人上人" (Elite), "NPC", or "拉完了" (La)

3. **Adjust Font**：Adjust font size and color in the "Font Settings" tab

4. **Add Content**：Click the "Add Content" button in the "Operations" tab to add content to the image

5. **Export Image**：Click the "Export Image" button, select the save path and format to export the final image

### Command Line Version

#### 1. Launch the Program

```bash
python hang_to_la_cli.py
```

#### 2. Basic Operations

1. **Add Content**：Select option 1, enter content, rating, and optional font settings
2. **Export Image**：Select option 2, enter output filename
3. **Exit**：Select option 3

#### 3. Example Operation

```
=== From Hang to La Command Line Tool ===

1. Add Content
2. Export Image
3. Exit

Please select operation (1-3): 1
Please enter content: This code is terrible
Please enter rating (0-10): 2
Please enter font size (default 24): 32
Please enter color code (default #000000): #FF0000
Added: This code is terrible (Rating: 2, Position: (356, 680))

Please select operation (1-3): 2
Please enter output filename (default hang_to_la_result.jpg): rating_result.png
Image exported to: rating_result.png
```

### 评分与区域对应关系 / Rating and Area Mapping

| Score Range | Corresponding Area |
|-------------|--------------------|
| 0-2         | 拉完了 (La, Bottom) |
| 2-4         | NPC (Lower Middle) |
| 4-6         | 人上人 (Elite, Middle) |
| 6-8         | 顶级 (Top Level, Upper Middle) |
| 8-10        | 夯 (Hang, Top) |

> **Note**：The score range division in the command line version is consistent with the GUI version to ensure the same image effect.

## 技术栈 / Technology Stack

- **Python 3.7+**：Main development language
- **Tkinter**：GUI interface development
- **Pillow**：Image processing and text drawing

## 文件说明 / File Description

- `hang_to_la_app.py`：Main program file, GUI version with all functions
- `hang_to_la_cli.py`：Command line version, suitable for script calls and batch processing
- `hang_to_la.jpg`：Background image file with five rating areas pre-divided
- `README.md`：Project documentation
- `debug.log`：Debug log file (automatically generated when the program runs)

## 示例 / Example

![Example Image](https://example.com/hang_to_la_example.jpg)  <!-- Replace with actual example image link -->

## 许可证 / License

This project is licensed under the MIT License, see the LICENSE file for details.

## 贡献指南 / Contributing

Welcome to submit Issues and Pull Requests to improve this project!

1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 版本历史 / Version History

### v1.0.0 (2023-06-15)
- Initial version release
- Support for both GUI and command line operation modes
- Implementation of five-level system and precise rating function
- Support for custom font size and color
- Automatic text overlap avoidance
- Image export function

## 故障排除 / Troubleshooting

### Problem: PIL module not found
**Solution**: Install the Pillow library
```bash
pip install pillow
```

### Problem: Program won't start or crashes
**Solution**:
1. Ensure Python version is 3.7 or above
2. Check if any dependencies are missing
3. Check the debug.log file for detailed error information

### Problem: Text display is abnormal or garbled
**Solution**:
1. Ensure common fonts (like Arial) are installed on your system
2. Try using default font settings

## 致谢 / Acknowledgments

- Thanks for using Pillow and Tkinter libraries
- Thanks to all contributors and users

## 联系方式 / Contact

If you have any questions or suggestions, please contact us through:

- GitHub Issues: https://github.com/yourusername/hang-to-la/issues
- Submit Pull Request to improve code

> **Tip**: When submitting an Issue, please provide detailed error information and operation steps so that we can quickly locate and solve the problem!
