"""Plot an overview of one BIDMC recording and print basic sanity checks."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.load_data import load_recording


def main(rec_num: int) -> None:
    rec = load_recording(rec_num)
    print(f"{rec.rec_id}: PPG {len(rec.ppg)} samples at {rec.fs_wave} Hz "
          f"({len(rec.ppg) / rec.fs_wave:.1f} s)")
    print(f"{rec.rec_id}: HR {len(rec.hr_ref)} samples at {rec.fs_num} Hz")
    for label, x in [("ppg", rec.ppg), ("ecg", rec.ecg),
                     ("hr_ref", rec.hr_ref), ("pulse_monitor", rec.pulse_monitor)]:
        print(f"  {label}: NaNs={int(np.isnan(x).sum())} "
              f"min={np.nanmin(x):.2f} max={np.nanmax(x):.2f}")

    t_wave = np.arange(len(rec.ppg)) / rec.fs_wave
    t_num = np.arange(len(rec.hr_ref)) / rec.fs_num
    seg = t_wave < 10

    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    axes[0].plot(t_wave[seg], rec.ppg[seg])
    axes[0].set_title(f"{rec.rec_id} PPG (PLETH), first 10 s")
    axes[0].set_ylabel("NU")
    axes[1].plot(t_wave[seg], rec.ecg[seg])
    axes[1].set_title("ECG lead II, first 10 s")
    axes[1].set_ylabel("mV")
    axes[2].plot(t_num, rec.hr_ref, label="HR (ECG-derived reference)")
    axes[2].plot(t_num, rec.pulse_monitor, label="PULSE (monitor, from PPG)")
    axes[2].set_title("1 Hz numerics, full recording")
    axes[2].set_xlabel("time (s)")
    axes[2].set_ylabel("bpm")
    axes[2].legend()
    fig.tight_layout()
    out = f"results/figures/{rec.rec_id}_overview.png"
    fig.savefig(out, dpi=150)
    print(f"Saved {out}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
