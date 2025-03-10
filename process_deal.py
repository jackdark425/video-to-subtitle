import argparse
from video_processor import VideoProcessor
from whisper_handler import WhisperHandler
from config import Config
import os

def main():
    """处理视频文件并生成英文字幕"""
    parser = argparse.ArgumentParser(description='将视频转换为英文字幕')
    parser.add_argument('video_path', help='输入视频文件路径')
    parser.add_argument('--model_size', default='medium', choices=['tiny', 'base', 'small', 'medium', 'large'], 
                      help='Whisper模型大小 (默认: medium)')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'], 
                      help='运行设备 (默认: cuda)')
    parser.add_argument('--output_dir', default='output', 
                      help='输出目录 (默认: output)')

    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.video_path):
        print(f"错误: 视频文件不存在: {args.video_path}")
        return 1

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)

    # 初始化配置
    config = Config(
        input_file=args.video_path,
        output_dir=args.output_dir,
        target_languages=['en'],
        model_size=args.model_size,
        device=args.device
    )

    print(f"\n配置信息:")
    print(f"- 输入文件: {config.input_file}")
    print(f"- 输出目录: {config.output_dir}")
    print(f"- 目标语言: {', '.join(config.target_languages)}")
    print(f"- 使用设备: {config.device}")
    print(f"- Whisper模型: {config.model_size}")

    # 初始化处理器
    video_proc = VideoProcessor(config)
    whisper = WhisperHandler(config)

    try:
        # 提取音频
        print('\n1. 正在从视频提取音频...')
        output_name = os.path.splitext(os.path.basename(args.video_path))[0]
        audio_path = video_proc.extract_audio(args.video_path)
        print(f'✓ 音频已提取到: {audio_path}')

        # 加载音频数据
        print('\n2. 正在加载音频数据...')
        audio_data = video_proc.load_audio(audio_path)
        print('✓ 音频数据加载完成')

        # 识别并直接翻译为英语
        print('\n3. 正在识别并翻译为英语...')
        segments = whisper.process_audio(audio_data, target_language='en')
        
        # 保存字幕
        output_path = os.path.join(args.output_dir, f'{output_name}_en.srt')
        print(f'\n4. 正在保存字幕到: {output_path}')
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = whisper.format_timestamp(segment['start'])
                end_time = whisper.format_timestamp(segment['end'])
                text = segment['text']
                f.write(f'{i}\n{start_time} --> {end_time}\n{text}\n\n')
        
        print('✓ 处理完成！')
        print(f'字幕文件已保存到: {output_path}')
        
    except Exception as e:
        print(f'\n处理过程中出错: {str(e)}')
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
