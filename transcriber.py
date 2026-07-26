"""Whisper transcription via faster-whisper."""

import os
import shutil
from pathlib import Path

import numpy as np

# Ensure CUDA DLLs are accessible to ctranslate2
_site_pkgs = Path(__file__).parent
_nvidia_dir = _site_pkgs / "nvidia"
_ct2_dir = _site_pkgs / "ctranslate2"
if _nvidia_dir.exists() and _ct2_dir.exists():
    _needed = {"cublas64_12.dll", "cublasLt64_12.dll", "cudart64_12.dll", "nvrtc64_120_0.dll"}
    _missing = [dll for dll in _needed if not (_ct2_dir / dll).is_file()]
    if _missing:
        for _pkg_dir in sorted(_nvidia_dir.iterdir()):
            _src = _pkg_dir / "bin"
            if _src.is_dir():
                for _dll in _missing:
                    _dll_path = _src / _dll
                    if _dll_path.is_file():
                        shutil.copy2(str(_dll_path), str(_ct2_dir / _dll))

from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self, model_size: str = "medium", device: str = "auto"):
        self.model_size = model_size
        self.device = device
        self._model = None

    def load_model(self) -> None:
        import torch
        if self.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        compute = "float16" if self.device == "cuda" else "int8"
        print(f"Transcriber: device={self.device}, compute={compute}")
        self._model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=compute,
        )

    def transcribe(
        self,
        audio: np.ndarray,
        language: str = "auto",
        punctuation: bool = True,
    ) -> str:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        lang = None if language == "auto" else language
        segments, info = self._model.transcribe(
            audio,
            language=lang,
            beam_size=5,
            vad_filter=True,
        )

        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())

        text = " ".join(text_parts)

        if not punctuation:
            import string
            for char in string.punctuation + "\u2014\u2013\u00ab\u00bb\u2026":
                text = text.replace(char, "")

        return text.strip()
