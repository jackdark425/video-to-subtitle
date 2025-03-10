class Config:
    def __init__(self, input_file, output_dir, target_languages, model_size="base", device="cuda", sample_rate=16000):
        self.input_file = input_file
        self.output_dir = output_dir
        self.target_languages = target_languages
        self.model_size = model_size
        self.device = device
        self.sample_rate = sample_rate  # 音频采样率，默认16kHz

    @property
    def model_path(self):
        return f"models/whisper-{self.model_size}.pt"