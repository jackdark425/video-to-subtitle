# 视频转字幕 AI 助手项目

这是一个基于 OpenAI Whisper 模型的视频字幕生成工具，可以自动从视频中提取音频并生成多语言字幕。本项目由 **Roo Code AI 编程助手**全程辅助开发，展示了AI辅助编程的强大能力。

## AI 辅助开发说明

本项目是在 Roo Code AI 编程助手的全程协助下完成的，包括：
- 项目架构设计
- 代码实现与优化
- 错误处理和异常恢复
- 文档生成和项目配置
- 代码审查和质量保证

通过 AI 辅助开发，我们实现了：
- 快速高效的项目开发
- 标准化的代码结构
- 完善的错误处理机制
- 详尽的文档说明

## 功能特点

- 自动视频音频提取
- 自动语言检测
- 支持多语言字幕生成
- GPU 加速支持
- 标准SRT格式输出
- 错误恢复机制

## 系统要求

- Python 3.8+
- CUDA 支持 (推荐用于 GPU 加速)
- FFmpeg

## 环境准备

1. 安装 FFmpeg
   - Windows: 从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载并配置环境变量
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 下载Whisper模型
- 默认使用medium模型，需要手动下载并放置在正确位置：
```bash
# 创建模型目录
mkdir -p whisper

# 下载medium模型（约1.5GB）
# 从官方仓库下载: https://huggingface.co/openai/whisper-medium
# 下载完成后将模型文件重命名为medium.pt并放置在whisper目录下
```

## 使用方法

### 基本用法

```bash
python process_deal.py [视频文件路径] --model_size [模型大小] --device [设备] --output_dir [输出目录]
```

### 参数说明

- `视频文件路径`: 待处理视频文件的路径
- `--model_size`: Whisper模型大小,可选值: 
  * tiny: 最小模型,速度最快
  * base: 基础模型,平衡速度和准确性
  * small: 小型模型
  * medium: 中型模型(默认)
  * large: 大型模型,最高准确性
- `--device`: 运行设备,可选值:
  * cuda: 使用GPU加速(默认)
  * cpu: 使用CPU处理
- `--output_dir`: 输出目录,默认为'output'

### 示例

```bash
# 使用中型模型,GPU加速处理视频
python process_deal.py test/TV-20250211.mp4 --model_size medium --device cuda --output_dir test

# 使用CPU处理视频
python process_deal.py video.mp4 --device cpu

# 使用小型模型快速处理
python process_deal.py video.mp4 --model_size small
```

## 项目结构

```
video-to-subtitle/
├── config.py            # 配置管理
├── process_deal.py      # 命令行接口和主流程
├── video_processor.py   # 视频处理和音频提取
├── whisper_handler.py   # Whisper模型处理
├── requirements.txt     # 项目依赖
├── test/               # 测试文件夹
│   ├── TV-20250211.mp4     # 测试视频范例
│   ├── TV-20250211.wav     # 生成的音频
│   └── TV-20250211_en.srt  # 生成的字幕
└── whisper/            # 模型目录
    └── medium.pt       # Whisper模型(需下载)
```

## 主要组件说明

### 1. 配置管理 (config.py)
管理项目配置,包括:
- 输入输出路径
- 目标语言设置
- 模型参数
- 设备选择
- 音频采样率等

### 2. 视频处理 (video_processor.py)
处理视频相关操作:
- FFmpeg检测和配置
- 音频提取
- 音频加载和预处理
- 错误处理

### 3. Whisper模型处理 (whisper_handler.py)
管理Whisper模型相关功能:
- 模型加载
- 语音识别
- 自动语言检测
- 字幕生成
- 内存管理和错误恢复

### 4. 主程序接口 (process_deal.py)
提供命令行接口:
- 参数解析
- 流程控制
- 输出格式化
- 错误处理

## AI 开发流程亮点

1. 智能代码生成
- 基于最佳实践的代码架构
- 自动处理边界情况
- 优化的性能实现

2. 自动化测试与验证
- 完整的测试用例
- 自动错误检测
- 性能优化建议

3. 文档自动生成
- 详细的API文档
- 使用示例
- 故障排除指南

## 性能优化

1. GPU加速
- 支持CUDA加速
- 自动显存管理
- 显存不足时自动降级到CPU

2. 错误处理
- FFmpeg环境检查
- 音频提取失败恢复
- 模型处理错误恢复
- 自动降级处理机制

3. 内存管理
- 流式音频处理
- 自动清理临时文件
- 大文件处理优化

## 常见问题

1. FFmpeg未找到
   - 解决: 检查FFmpeg是否正确安装并添加到环境变量

2. GPU内存不足
   - 解决1: 使用较小的模型 (small或base)
   - 解决2: 切换到CPU模式 (--device cpu)

3. 音频提取失败
   - 解决: 检查视频文件格式是否受支持
   - 检查FFmpeg是否支持该格式

## 开发说明

本项目使用Python开发,主要依赖:
- torch: 深度学习框架
- openai-whisper: 语音识别模型
- ffmpeg-python: 音视频处理
- numpy: 数据处理
- tqdm: 进度显示

## 致谢

- Roo Code AI 编程助手 - 项目全程开发支持
- OpenAI Whisper 团队 - 提供强大的语音识别模型
- FFmpeg 项目 - 提供音视频处理支持

## 许可证

MIT License