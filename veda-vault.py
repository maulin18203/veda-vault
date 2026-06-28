#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║       VEDIC SANATANA — Full Library Downloader               ║
║       Python 3  |  Requires: pip install requests            ║
╠══════════════════════════════════════════════════════════════╣
║  Downloads every PDF into:                                   ║
║    shub/Vedas/                                               ║
║    shub/Puranas/                                             ║
║    shub/Upanishads/                                          ║
║    shub/Itihas/                                              ║
║    shub/Smriti/                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Features:                                                   ║
║    ✔ Resume interrupted downloads (HTTP Range)               ║
║    ✔ 3 auto-retries with backoff                             ║
║    ✔ Live progress bar with speed + ETA                      ║
║    ✔ Skips already-complete files                            ║
║    ✔ Saves failed_urls.txt + download_log.txt                ║
║    ✔ Final summary with per-folder stats                     ║
╠══════════════════════════════════════════════════════════════╣
║  Run:  python download_shub.py                               ║
║  Disk: ~2.5 GB+ free space needed                           ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import datetime
import requests
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ── ANSI colours ──────────────────────────────────────────────
R  = "\033[0;31m"    # red
G  = "\033[0;32m"    # green
Y  = "\033[1;33m"    # yellow
C  = "\033[0;36m"    # cyan
B  = "\033[1m"       # bold
NC = "\033[0m"       # reset

# ── Base directory ────────────────────────────────────────────
BASE = Path("shub")

# ── File manifest  ────────────────────────────────────────────
# Format: (subfolder, filename, url)
MANIFEST = [

    # ── 1. VEDAS ─────────────────────────────────────────────
    ("Vedas", "Rigveda_Complete_Hindi_GitaPress.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/rigved.pdf"),

    ("Vedas", "Yajurveda_Shukla_Hindi.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/yajurved.pdf"),

    ("Vedas", "Samaveda_Hindi.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/samved.pdf"),

    ("Vedas", "Atharvaveda_Hindi_Part1.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/arthved-part-1.pdf"),

    ("Vedas", "Atharvaveda_Hindi_Part2.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/atharva-2.pdf"),

    # ── 2. PURANAS ───────────────────────────────────────────
    ("Puranas", "Agni_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/agni-puran.pdf"),

    ("Puranas", "Bhagwat_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/bhagwat-puran.pdf"),

    ("Puranas", "Bhavishya_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/bavishya-puran.pdf"),

    ("Puranas", "Brahma_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/bramha.pdf"),

    ("Puranas", "Brahmand_Puran_Part1.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/brahamand.pdf"),

    ("Puranas", "Brahmand_Puran_Part2.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/brahamandp.pdf"),

    ("Puranas", "Garuda_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/garuda1.pdf"),

    ("Puranas", "Kurma_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/kurma.pdf"),

    ("Puranas", "Ling_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/ling.pdf"),

    ("Puranas", "Markandya_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/markende-puran.pdf"),

    ("Puranas", "Matsya_Puran_Part1.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/matsya-puran-1.pdf"),

    ("Puranas", "Matsya_Puran_Part2.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/matsya-puran-2.pdf"),

    ("Puranas", "Narad_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/nard-puran.pdf"),

    ("Puranas", "Padma_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/padam-puran.pdf"),

    ("Puranas", "Shiv_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/shiv-puran.pdf"),

    ("Puranas", "Skand_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/sakand-puran.pdf"),

    ("Puranas", "BrahmVaivarta_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/vaivtpuran.pdf"),

    ("Puranas", "Vaman_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/vamanpuran.pdf"),

    ("Puranas", "Varah_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/varaha-puran.pdf"),

    ("Puranas", "Vishnu_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/vishnu-puran.pdf"),

    ("Puranas", "Vayu_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2016/07/vayu-puran.pdf"),

    ("Puranas", "Kalki_Puran.pdf",
     "https://vedpuran.net/wp-content/uploads/2012/12/kalkipuranhindi1.pdf"),

    ("Puranas", "Narsimha_Puran_Upapuran.pdf",
     "https://vedpuran.net/wp-content/uploads/2011/10/narsihma-puran.pdf"),

    # ── 3. UPANISHADS ────────────────────────────────────────
    ("Upanishads", "108_Upanishads_with_Commentary.pdf",
     "https://vedpuran.net/wp-content/uploads/2014/02/108-upanishads-with-upanishad-brahmam-commentary.pdf"),

    ("Upanishads", "The_Upanishads_Intro_Edition.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/03/the_upanishads.pdf"),

    ("Upanishads", "Vedant_Darshan_Brahmasutra_Hindi_Sanskrit.pdf",
     "https://vedpuran.net/wp-content/uploads/2013/04/gita-press-vedant-darshan-brahmasutra-sanskrit-hindi.pdf"),

    ("Upanishads", "Brahmasutra_Sanskrit.pdf",
     "https://vedpuran.net/wp-content/uploads/2013/04/bramsutr.pdf"),

    ("Upanishads", "Vivek_Chudamani_Shankaracharya.pdf",
     "https://vedpuran.net/wp-content/uploads/2013/04/vivakchudamani.pdf"),

    # ── 4. ITIHAS ────────────────────────────────────────────
    ("Itihas", "Mahabharat_Complete_GitaPress_7250pages.pdf",       # ~709 MB
     "https://vedpuran.net/wp-content/uploads/2021/03/mahabhart-gorkhpur.pdf"),

    ("Itihas", "Mahabharat_Full_with_Geeta_Hindi.pdf",              # ~271 MB
     "https://vedpuran.net/wp-content/uploads/2012/07/mahabhart-full-with-geeta-hindi.pdf"),

    ("Itihas", "Valmiki_Ramayan_All_Kands_6191pages.pdf",           # ~182 MB
     "https://vedpuran.net/wp-content/uploads/2012/08/ramayana_all_kand_6191_pages.pdf"),

    ("Itihas", "Shri_Ramcharitmanas_Complete_Tulsidas.pdf",
     "https://vedpuran.net/wp-content/uploads/2026/05/shree-ram-charit-manas.pdf"),

    ("Itihas", "Anand_Ramayan_Hindi.pdf",                           # ~293 MB
     "https://vedpuran.net/wp-content/uploads/2013/04/anandramayan.pdf"),

    ("Itihas", "Shrimad_Bhagavad_Geeta_GitaPress.pdf",
     "https://vedpuran.net/wp-content/uploads/2012/03/unencrypted-geeta.pdf"),

    ("Itihas", "Yoga_Vashishtha_Maharamayan_Part1.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/04/shri-yogavasishtha-1.pdf"),

    ("Itihas", "Yoga_Vashishtha_Maharamayan_Part2.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/04/shri-yogavasishtha-2.pdf"),

    ("Itihas", "Yoga_Vashishtha_Maharamayan_Part3.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/04/shri-yogavasishtha-3.pdf"),

    ("Itihas", "Yoga_Vashishtha_Maharamayan_Part4.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/04/shri-yogavasishtha-4.pdf"),

    # ── 5. SMRITI ────────────────────────────────────────────
    ("Smriti", "Manusmriti_Hindi_Sanskrit.pdf",
     "https://vedpuran.net/wp-content/uploads/2016/07/manusmiriti.pdf"),

    ("Smriti", "Manusmriti_English.pdf",
     "https://vedpuran.net/wp-content/uploads/2013/04/manusmriti.pdf"),

    ("Smriti", "Bhrigu_Samhita_Hindi.pdf",                         # ~110 MB
     "https://vedpuran.net/wp-content/uploads/2013/02/bhrigu-samhita-hindi1.pdf"),

    ("Smriti", "Vimanika_Shastra_Aeronautical.pdf",
     "https://vedpuran.net/wp-content/uploads/2021/03/vimanika-shaster.pdf"),
]

# ── Minimum valid file size (10 KB) ──────────────────────────
MIN_SIZE = 10 * 1024

# ── Human-readable byte sizes ─────────────────────────────────
def fmt_size(n_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} GB"

# ── Progress bar ──────────────────────────────────────────────
def progress_bar(done: int, total: int, speed: float, elapsed: float) -> str:
    bar_w = 35
    pct = done / total if total else 0
    filled = int(bar_w * pct)
    bar = "█" * filled + "░" * (bar_w - filled)
    eta = ""
    if speed > 0 and total > done:
        secs = int((total - done) / speed)
        eta = f"ETA {secs // 60}m{secs % 60:02d}s"
    return (f"\r  [{bar}] {pct*100:5.1f}%  "
            f"{fmt_size(done)}/{fmt_size(total)}  "
            f"{fmt_size(int(speed))}/s  {eta}   ")

# ── Build a session with retry ────────────────────────────────
def make_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,          # 2 s, 4 s, 8 s between retries
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://",  adapter)
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
        )
    })
    return s

# ── Download one file ─────────────────────────────────────────
def download_file(
    session: requests.Session,
    folder: str,
    filename: str,
    url: str,
    index: int,
    total_files: int,
    log_lines: list,
    failed_lines: list,
) -> str:
    """
    Returns: "ok" | "skipped" | "failed"
    """
    dest = BASE / folder / filename

    # ── Already complete? ─────────────────────────────────────
    existing = dest.stat().st_size if dest.exists() else 0
    if existing > MIN_SIZE:
        print(f"\n{B}[{index}/{total_files}] {Y}{filename}{NC}")
        print(f"  {G}✔ Already complete ({fmt_size(existing)}) — nothing to do{NC}")
        log_lines.append(f"[DONE-EXISTS]  {filename}  ({fmt_size(existing)})")
        return "skipped"

    print(f"\n{B}[{index}/{total_files}] {Y}{filename}{NC}")
    print(f"  📁  shub/{folder}/")

    # ── Attempt download with resume ──────────────────────────
    headers = {}
    mode = "wb"
    if existing > 0:
        headers["Range"] = f"bytes={existing}-"
        mode = "ab"
        print(f"  {C}↻  Resuming from {fmt_size(existing)}{NC}")

    try:
        resp = session.get(url, headers=headers, stream=True, timeout=60)

        # Server doesn't support range — restart
        if existing > 0 and resp.status_code == 200:
            existing = 0
            mode = "wb"

        if resp.status_code not in (200, 206):
            raise requests.HTTPError(f"HTTP {resp.status_code}")

        total = int(resp.headers.get("Content-Length", 0)) + existing
        downloaded = existing
        chunk_size = 512 * 1024   # 512 KB chunks
        t0 = time.time()
        t_last = t0
        bytes_since_last = 0
        speed = 0.0

        with open(dest, mode) as fh:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                fh.write(chunk)
                downloaded += len(chunk)
                bytes_since_last += len(chunk)

                now = time.time()
                dt = now - t_last
                if dt >= 0.5:                       # update every 0.5 s
                    speed = bytes_since_last / dt
                    t_last = now
                    bytes_since_last = 0

                if total:
                    sys.stdout.write(
                        progress_bar(downloaded, total, speed, now - t0)
                    )
                    sys.stdout.flush()

        print()   # newline after progress bar

        final_size = dest.stat().st_size
        if final_size < MIN_SIZE:
            raise ValueError(f"File too small ({fmt_size(final_size)}) — likely an error page")

        elapsed = time.time() - t0
        avg_speed = final_size / elapsed if elapsed > 0 else 0
        print(f"  {G}✔ Done  {fmt_size(final_size)}  "
              f"(avg {fmt_size(int(avg_speed))}/s,  {elapsed:.0f}s){NC}")
        log_lines.append(f"[OK]       {filename}  ({fmt_size(final_size)})")
        return "ok"

    except Exception as exc:
        print(f"\n  {R}✘ FAILED: {exc}{NC}")
        # Remove corrupt partial only if very small
        if dest.exists() and dest.stat().st_size < MIN_SIZE:
            dest.unlink()
        log_lines.append(f"[FAILED]   {filename}  — {exc}")
        failed_lines.append(f"{url}  →  shub/{folder}/{filename}")
        return "failed"


# ── Main ──────────────────────────────────────────────────────
def main():
    print(f"""
{B}{C}╔══════════════════════════════════════════════════════╗
║   VEDIC SANATANA — Full Library Downloader           ║
║   {len(MANIFEST)} files  |  ~2.5 GB total                      ║
╚══════════════════════════════════════════════════════╝{NC}
""")

    # ── Create folders ────────────────────────────────────────
    for sub in ("Vedas", "Puranas", "Upanishads", "Itihas", "Smriti"):
        (BASE / sub).mkdir(parents=True, exist_ok=True)

    log_lines: list[str] = [
        f"Download started : {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", ""
    ]
    failed_lines: list[str] = []

    counters = {"ok": 0, "skipped": 0, "failed": 0}
    session  = make_session()

    current_section = ""

    for idx, (folder, filename, url) in enumerate(MANIFEST, start=1):
        # ── Section header ────────────────────────────────────
        if folder != current_section:
            current_section = folder
            section_map = {
                "Vedas":      "1. VEDAS  (वेद)",
                "Puranas":    "2. PURANAS  (पुराण)",
                "Upanishads": "3. UPANISHADS  (उपनिषद)",
                "Itihas":     "4. ITIHAS  (इतिहास)",
                "Smriti":     "5. SMRITI  (स्मृति)",
            }
            label = section_map.get(folder, folder)
            print(f"\n{B}{C}{'─'*54}")
            print(f"  {label}")
            print(f"{'─'*54}{NC}")

        result = download_file(
            session, folder, filename, url,
            idx, len(MANIFEST),
            log_lines, failed_lines,
        )
        counters[result] += 1

    # ── Totals ────────────────────────────────────────────────
    total_size = sum(
        f.stat().st_size
        for f in BASE.rglob("*.pdf")
        if f.is_file()
    )

    summary = [
        "",
        f"{'═'*54}",
        f"  DOWNLOAD COMPLETE — SUMMARY",
        f"{'═'*54}",
        f"  Total in list    :  {len(MANIFEST)}",
        f"  ✔ Downloaded now :  {counters['ok']}",
        f"  ✔ Already had    :  {counters['skipped']}",
        f"  ✘ Failed         :  {counters['failed']}",
        f"  ✔ Total complete :  {counters['ok'] + counters['skipped']}",
        f"  Disk used        :  {fmt_size(total_size)}",
        "",
    ]

    for line in summary:
        print(f"{B}{C}{line}{NC}" if "═" in line else f"{B}{line}{NC}")

    # ── Per-folder stats ──────────────────────────────────────
    print(f"  {C}Folder breakdown:{NC}")
    for sub in ("Vedas", "Puranas", "Upanishads", "Itihas", "Smriti"):
        d = BASE / sub
        files = list(d.glob("*.pdf"))
        size  = sum(f.stat().st_size for f in files)
        print(f"    📂  {sub:<12}  {len(files):>2} file(s)   {fmt_size(size)}")

    if counters["failed"]:
        print(f"\n  {R}✘ {counters['failed']} file(s) failed.{NC}")
        print(f"  {Y}Re-run script — downloads will resume from where they stopped.{NC}")
        print(f"  Failed URLs → shub/failed_urls.txt")
    else:
        print(f"\n  {G}All files downloaded successfully! 🙏{NC}")

    print(f"\n  {C}Jai Shri Ram 🙏{NC}\n")

    # ── Write logs ────────────────────────────────────────────
    log_lines += [
        "",
        f"Download finished: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        f"Total: {len(MANIFEST)}  |  Downloaded: {counters['ok']}  "
        f"|  Already had: {counters['skipped']}  |  Failed: {counters['failed']}",
    ]
    (BASE / "download_log.txt").write_text("\n".join(log_lines), encoding="utf-8")

    if failed_lines:
        (BASE / "failed_urls.txt").write_text(
            "\n".join(failed_lines), encoding="utf-8"
        )

    print(f"  Log  → shub/download_log.txt")


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Missing dependency. Run:  pip install requests")
        sys.exit(1)
    main()
