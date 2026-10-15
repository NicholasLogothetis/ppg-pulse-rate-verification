"""Load BIDMC recordings, selecting signals by name (never by column position)."""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import wfdb

DATA_DIR = Path("data/bidmc")


def clean_name(name: str) -> str:
    """wfdb keeps the trailing comma from the header, e.g. 'PLETH,' -> 'PLETH'."""
    return name.strip().rstrip(",").strip()


def get_signal(record, name: str) -> np.ndarray:
    names = [clean_name(n) for n in record.sig_name]
    if name not in names:
        raise KeyError(f"Signal '{name}' not found. Available: {names}")
    return record.p_signal[:, names.index(name)]


@dataclass
class Recording:
    rec_id: str
    fs_wave: float
    fs_num: float
    ppg: np.ndarray
    ecg: np.ndarray
    hr_ref: np.ndarray
    pulse_monitor: np.ndarray
    comments: str


def load_recording(rec_num: int, data_dir: Path = DATA_DIR) -> Recording:
    rec_id = f"bidmc{rec_num:02d}"
    wave = wfdb.rdrecord(str(data_dir / rec_id))
    nums = wfdb.rdrecord(str(data_dir / f"{rec_id}n"))
    return Recording(
        rec_id=rec_id,
        fs_wave=wave.fs,
        fs_num=nums.fs,
        ppg=get_signal(wave, "PLETH"),
        ecg=get_signal(wave, "II"),
        hr_ref=get_signal(nums, "HR"),
        pulse_monitor=get_signal(nums, "PULSE"),
        comments=" ".join(wave.comments),
    )
