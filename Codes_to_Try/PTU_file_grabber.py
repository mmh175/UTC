"""
Acquire 10 s of raw TTTR data with snAPI and save it to a PTU file.
"""

from snAPI.Main import *          # snAPI v1.0.7 or later
import os

# ──────────────── user‑adjustable parameters ────────────────
ACQ_TIME_MS  = 10_000                 # 10 s expressed in milliseconds
BUFFER_BYTES = 256 * 1024 * 1024      # 256 MB in‑RAM ring buffer (adjust to taste)
CONFIG_INI   = r"config\MH.ini"       # Harp‑specific thresholds etc. (optional)
OUT_DIR      = r"C:\Data\PicoQuant"   # where the PTU should be written
PTU_FILE     = os.path.join(OUT_DIR, "raw_10s_run.ptu")
# ────────────────────────────────────────────────────────────

os.makedirs(OUT_DIR, exist_ok=True)

sn = snAPI()                              # creates and initAPI() internally
try:
    sn.getDevice()                        # first available device :contentReference[oaicite:0]{index=0}
    sn.initDevice(MeasMode.T3)            # T3 = traditional TTTR mode
    sn.loadIniConfig(CONFIG_INI)          # optional: thresholds, dead‑times, …
    sn.setPTUFilePath(PTU_FILE)           # tell snAPI where to put the PTU :contentReference[oaicite:1]{index=1}

    print(f"Recording {ACQ_TIME_MS/1000:.1f}s of raw data to {PTU_FILE} …")

    #                                     ┌ acquisition time (ms)
    #                                     │      ┌ buffer size   ┌ write PTU?
    #                                     │      │               │       ┌ block until finished?
    sn.raw.measure(ACQ_TIME_MS, BUFFER_BYTES, True,  True)   # :contentReference[oaicite:2]{index=2}

    sn.getMeasDescription()               # updates sn.measDescription :contentReference[oaicite:3]{index=3}
    print(f"Finished – {sn.measDescription['NumRecs']} records written.")

finally:
    sn.closeDevice()                      # releases the hardware
    sn.exitAPI()                          # flush logs & free DLL
