"""Global hotkey listener using pynput."""

from pynput import keyboard
from enum import Enum


def _vk(key):
    """Extract virtual key code from a pynput key."""
    if hasattr(key, 'value') and hasattr(key.value, 'vk'):
        return key.value.vk
    if hasattr(key, 'vk'):
        return key.vk
    return None


HOTKEY_VK = {
    "ctrl_r": _vk(keyboard.Key.ctrl_r),
    "ctrl_l": _vk(keyboard.Key.ctrl_l),
    "alt_r": _vk(keyboard.Key.alt_r),
}

ALT_R_VKS = {_vk(keyboard.Key.alt_r), _vk(keyboard.Key.alt_gr)} if hasattr(keyboard.Key, 'alt_gr') else {_vk(keyboard.Key.alt_r)}


class TriggerMode(Enum):
    HOLD = "hold"
    TOGGLE = "toggle"


class HotkeyManager:
    def __init__(self, mode: TriggerMode = TriggerMode.HOLD, hotkey: str = "ctrl_r"):
        self.mode = mode
        self._hotkey_vk = HOTKEY_VK.get(hotkey, _vk(keyboard.Key.ctrl_r))
        self._listener = None
        self._recording = False
        self._alt_r_held = False
        self.on_start = None
        self.on_stop = None
        self.on_cancel = None
        self.on_settings = None

    def start(self) -> None:
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _is_hotkey(self, key):
        return _vk(key) == self._hotkey_vk

    def _is_alt_r(self, key):
        return _vk(key) in ALT_R_VKS

    def _on_press(self, key):
        if self._is_hotkey(key):
            if self.mode == TriggerMode.HOLD:
                if not self._recording:
                    self._recording = True
                    if self.on_start:
                        self.on_start()
            elif self.mode == TriggerMode.TOGGLE:
                if self._recording:
                    self._recording = False
                    if self.on_stop:
                        self.on_stop()
                else:
                    self._recording = True
                    if self.on_start:
                        self.on_start()
        elif self._is_alt_r(key):
            self._alt_r_held = True
        elif hasattr(key, 'char') and key.char == 'p' and self._alt_r_held:
            if self.on_settings:
                self.on_settings()
        elif key == keyboard.Key.esc:
            if self._recording:
                self._recording = False
                if self.on_cancel:
                    self.on_cancel()

    def _on_release(self, key):
        if self._is_alt_r(key):
            self._alt_r_held = False
        if self._is_hotkey(key) and self.mode == TriggerMode.HOLD:
            if self._recording:
                self._recording = False
                if self.on_stop:
                    self.on_stop()

    @property
    def is_recording(self) -> bool:
        return self._recording
