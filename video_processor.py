import ffmpeg
import os
from typing import Optional
import numpy as np
import subprocess
from config import Config

class VideoProcessor:
    def __init__(self, config: Config):
        self.config = config
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """检查FFmpeg是否已安装"""
        try:
            # 使用subprocess直接检查ffmpeg命令
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg未安装或不在系统路径中。请安装FFmpeg: https://ffmpeg.org/download.html"
            )

    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        从视频文件中提取音频
        
        Args:
            video_path: 视频文件路径
            output_path: 音频输出路径（可选）
            
        Returns:
            str: 提取的音频文件路径
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")

        if output_path is None:
            output_path = os.path.splitext(video_path)[0] + '.wav'

        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

            # 使用FFmpeg提取音频
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                acodec='pcm_s16le',
                ac=1,
                ar=self.config.sample_rate
            )
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

            if not os.path.exists(output_path):
                raise RuntimeError("音频提取失败")

            return output_path

        except ffmpeg.Error as e:
            print(f"FFmpeg错误: {e.stderr.decode() if e.stderr else str(e)}")
            raise

    def load_audio(self, audio_path: str) -> np.ndarray:
        """
        加载音频文件到numpy数组
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            np.ndarray: 音频数据
        """
        try:
            # 使用FFmpeg读取音频数据
            out, _ = (
                ffmpeg.input(audio_path)
                .output('pipe:', format='f32le', acodec='pcm_f32le', ac=1, ar=self.config.sample_rate)
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            # 将字节转换为numpy数组
            audio_data = np.frombuffer(out, np.float32)
            return audio_data

        except ffmpeg.Error as e:
            print(f"音频加载错误: {e.stderr.decode() if e.stderr else str(e)}")
            raise