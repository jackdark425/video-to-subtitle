import whisper
import torch
import numpy as np
from typing import Dict, List
from tqdm import tqdm
from config import Config

class WhisperHandler:
    def __init__(self, config: Config):
        self.config = config
        self.device = config.device
        self.model = self._load_model()

    def _load_model(self) -> whisper.Whisper:
        """
        加载Whisper模型
        """
        try:
            print(f"正在加载Whisper {self.config.model_size} 模型...")
            model = whisper.load_model(
                self.config.model_size,
                device=self.device
            )
            print("模型加载完成")
            return model
        except Exception as e:
            raise RuntimeError(f"模型加载失败: {str(e)}")

    def process_audio(self, audio_data: np.ndarray, target_language: str = "zh", source_language: str = None) -> List[Dict]:
        """
        处理音频数据并返回识别结果，直接转录为目标语言
        
        Args:
            audio_data: 音频数据numpy数组
            target_language: 目标语言代码（默认为中文）
            source_language: 源语言代码（如果为None则自动检测）
            
        Returns:
            List[Dict]: 识别结果列表，每个字典包含时间戳和文本
        """
        try:
            # 确保音频数据在正确的设备上
            if isinstance(audio_data, np.ndarray):
                audio_data = torch.from_numpy(audio_data).float()
            
            audio_data = audio_data.to(self.device)

            print("正在处理音频...")
            with torch.no_grad(), tqdm(total=1, desc="音频处理进度") as pbar:
                # 配置Whisper选项
                options = dict(
                    task="translate",
                    language=source_language,  # 如果为None，Whisper会自动检测语言
                    verbose=False,
                    fp16=False if self.device == "cpu" else True
                )
                
                try:
                    result = self.model.transcribe(
                        audio_data,
                        **options
                    )
                    pbar.update(1)
                except torch.cuda.OutOfMemoryError:
                    print("GPU内存不足，尝试在CPU上处理...")
                    # 转移到CPU处理
                    audio_data = audio_data.cpu()
                    options["fp16"] = False
                    result = self.model.transcribe(
                        audio_data,
                        **options
                    )
                    pbar.update(1)

            # 提取并验证segments信息
            segments = []
            with tqdm(total=len(result["segments"]), desc="处理字幕片段") as pbar:
                for segment in result["segments"]:
                    text = segment["text"].strip()
                    if text:  # 只添加非空文本
                        segments.append({
                            "start": segment["start"],
                            "end": segment["end"],
                            "text": text,
                            "language": result.get("language", "unknown")  # 记录检测到的语言
                        })
                    pbar.update(1)

            print(f"处理完成: 检测到的语言为 {result.get('language', 'unknown')}")
            print(f"生成了 {len(segments)} 个有效字幕片段")
            
            return segments

        except Exception as e:
            print(f"音频处理错误: {str(e)}")
            print("尝试进行错误恢复...")
            
            try:
                # 尝试使用较小的模型重新处理
                if self.config.model_size != "base":
                    print("切换到base模型重试...")
                    backup_model = whisper.load_model("base", device=self.device)
                    with torch.no_grad():
                        result = backup_model.transcribe(audio_data)
                    return [
                        {
                            "start": segment["start"],
                            "end": segment["end"],
                            "text": segment["text"].strip(),
                            "language": result.get("language", "unknown"),
                            "recovered": True  # 标记为恢复的结果
                        }
                        for segment in result["segments"]
                        if segment["text"].strip()
                    ]
            except Exception as backup_error:
                print(f"错误恢复失败: {str(backup_error)}")
                raise RuntimeError("音频处理失败，且无法恢复") from e

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """
        将秒数格式化为字幕时间戳格式 (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace(".", ",")