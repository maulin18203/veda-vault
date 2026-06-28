#!/usr/bin/env python3
"""
Vedic Sanatana PDF Downloader
──────────────────────────────
Downloads all available PDFs from vedicsanatana.com into an organised
folder tree.  Features:
  • Concurrent downloads (configurable workers)
  • Auto-retry with exponential back-off
  • Resume / skip already-complete files
  • Per-file progress bars (tqdm)
  • Coloured summary table
  • Dry-run mode  (--dry-run)
  • Custom output directory  (--out DIR)
  • Configurable parallelism (--workers N)

Usage:
    python download_vedic_pdfs.py
    python download_vedic_pdfs.py --out ~/Books/Vedic --workers 6
    python download_vedic_pdfs.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import requests
from tqdm import tqdm

# ─────────────────────────────────────────────────────────────────────────────
# ANSI colour helpers (auto-disabled on non-TTY)
# ─────────────────────────────────────────────────────────────────────────────
_USE_COLOR = sys.stdout.isatty()

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text

def green(t):  return _c("32", t)
def red(t):    return _c("31", t)
def yellow(t): return _c("33", t)
def cyan(t):   return _c("36", t)
def bold(t):   return _c("1",  t)
def dim(t):    return _c("2",  t)


# ─────────────────────────────────────────────────────────────────────────────
# Catalogue  —  (category_folder, filename, upload_base_url)
# All filenames verified directly from each book's page on vedicsanatana.com
# ─────────────────────────────────────────────────────────────────────────────
_B10  = "https://vedicsanatana.com/wp-content/uploads/2024/10/"
_B12  = "https://vedicsanatana.com/wp-content/uploads/2024/12/"
_B26a = "https://vedicsanatana.com/wp-content/uploads/2026/01/"
_B26b = "https://vedicsanatana.com/wp-content/uploads/2026/02/"

CATALOGUE: list[tuple[str, str, str]] = [

    # ── वेद / Vedas ──────────────────────────────────────────────────────────
    ("01_Veda", "1.-Rigveda.pdf",     _B10),
    ("01_Veda", "2.-Yajurveda.pdf",   _B10),
    ("01_Veda", "3.-Samveda.pdf",     _B10),
    ("01_Veda", "4.-Atharvaveda.pdf", _B10),

    # ── पुराण / Puranas ───────────────────────────────────────────────────────
    ("02_Puran", "1.-vishnu-puran.pdf",           _B10),
    ("02_Puran", "2.-Shiva-Purana.pdf",           _B10),
    ("02_Puran", "3.-Brahama-Purana.pdf",         _B10),
    ("02_Puran", "4.-Agni-purana.pdf",            _B10),
    ("02_Puran", "5.-Bhagvad-puran.pdf",          _B10),
    ("02_Puran", "6.-bhavishya-puran.pdf",        _B10),
    ("02_Puran", "7.-Garuda-Purana.pdf",          _B10),
    ("02_Puran", "8.-Kurma-Puran.pdf",            _B10),
    ("02_Puran", "9.-Linga-Puran.pdf",            _B10),
    ("02_Puran", "10.-Markandey-Puran.pdf",       _B10),
    ("02_Puran", "11.-Matasya-Puran.pdf",         _B10),
    ("02_Puran", "12.-Narad-Puran.pdf",           _B10),
    ("02_Puran", "13.-Padma-Purana.pdf",          _B10),
    ("02_Puran", "14.-Skanda-Puran.pdf",          _B10),
    ("02_Puran", "15.-Brahma-Vaivarta-Puran.pdf", _B10),
    ("02_Puran", "16.-Vaman-Puran.pdf",           _B10),
    ("02_Puran", "17.-Varaha-Puran.pdf",          _B10),
    ("02_Puran", "18.-Vayu-Puran.pdf",            _B10),

    # ── उपनिषद् / Upanishads ─────────────────────────────────────────────────
    ("03_Upanishad", "1.-108-Upanishad.pdf",                _B10),
    ("03_Upanishad", "2.-Nirvana-Upanishad.pdf",            _B10),
    ("03_Upanishad", "3.-Isavasyopanishad.pdf",             _B10),
    ("03_Upanishad", "4.-Isha-Upanishad.pdf",               _B10),
    ("03_Upanishad", "5.-Kaivalya-Upanishad.pdf",           _B10),
    ("03_Upanishad", "6.-Prashnopanishad.pdf",              _B10),
    ("03_Upanishad", "7.-Mandukya-Upanishad.pdf",           _B10),
    ("03_Upanishad", "8.-Kena-Upanishad.pdf",               _B10),
    ("03_Upanishad", "9.-Kathopanishad.pdf",                _B10),
    ("03_Upanishad", "10.-Mundkopanishad.pdf",              _B10),
    ("03_Upanishad", "11.-Aitareya-Upanishad-in-Hindi.pdf", _B10),
    ("03_Upanishad", "12.-Taittiriyopanishad-Hindi.pdf",    _B10),
    ("03_Upanishad", "13.-Chandogya-Upanishad.pdf",         _B10),
    ("03_Upanishad", "14.-Brihadaranyaka-Upanishad.pdf",    _B10),

    # ── प्रमुख धार्मिक ग्रंथ / Major Religious Texts ────────────────────────
    ("04_Dharmik_Granth", "1.-Ravan-Samhita.pdf",                   _B10),
    ("04_Dharmik_Granth", "2.-Mahabharat.pdf",                      _B10),
    ("04_Dharmik_Granth", "3.-Bhavishya-Malika.pdf",                _B10),
    ("04_Dharmik_Granth", "4.-Shrimad-Bhagvad-Gita.pdf",           _B10),
    ("04_Dharmik_Granth", "4.1.-Yatharth-Geeta.pdf",               _B10),
    ("04_Dharmik_Granth", "5.-Shrimad-Valmiki-Ramayana.pdf",       _B10),
    ("04_Dharmik_Granth", "6.-Shri-Ramcharitmanas.pdf",            _B10),
    ("04_Dharmik_Granth", "7.-Bhrigu-Sanhita.pdf",                 _B10),
    ("04_Dharmik_Granth", "8.-Saral-bhagwad-gita-saar.pdf",        _B10),
    ("04_Dharmik_Granth", "9.-Shrimad-Bhagwa-Geeta-Mahatmaya.pdf", _B10),
    ("04_Dharmik_Granth", "10.-Yoga-Vasishtha.pdf",                _B10),
    ("04_Dharmik_Granth", "11.-Ashtavakra-Gita_in_Hindi.pdf",      _B10),
    ("04_Dharmik_Granth", "12.-Adbhut-Ramayan-in-hindi.pdf",       _B10),
    ("04_Dharmik_Granth", "13.-Surya-Siddhanta-In-Hindi.pdf",      _B10),
    ("04_Dharmik_Granth", "18.-ManuSmriti.pdf",                    _B10),
    ("04_Dharmik_Granth", "Satyarth-Prakash-Hindi.pdf",            _B12),

    # ── दर्शन / Philosophy ────────────────────────────────────────────────────
    ("05_Darshan", "Mimansa-Darshan-in-Hindi.pdf",             _B26a),
    ("05_Darshan", "Vaisheshik-Darshan-in-Hindi.pdf",          _B26a),
    ("05_Darshan", "Yoga-Darshan-in-hindi.pdf",                _B26a),
    ("05_Darshan", "Sankhy-Darshan-in-Hindi.pdf",              _B26a),
    ("05_Darshan", "Nyay-Shastra-in-hindi.pdf",                _B26b),
    ("05_Darshan", "Vedant-Darshan-Brahma-Sutra-in-hindi.pdf", _B26b),
]


# ─────────────────────────────────────────────────────────────────────────────
# Result tracking
# ─────────────────────────────────────────────────────────────────────────────
Status = Literal["downloaded", "skipped", "failed"]

@dataclass
class Result:
    folder:   str
    filename: str
    status:   Status
    size_kb:  int   = 0
    reason:   str   = ""
    elapsed:  float = 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Download constants
# ─────────────────────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept":   "application/pdf,*/*",
    "Referer":  "https://vedicsanatana.com/",
}

MIN_FILE_BYTES  = 4_096   # smaller → treat as error page
CONNECT_TIMEOUT = 15      # seconds
READ_TIMEOUT    = 90      # seconds
CHUNK_SIZE      = 65_536  # 64 KB read chunks


def _human(kb: int) -> str:
    """Human-friendly file size."""
    if kb < 1_024:
        return f"{kb} KB"
    return f"{kb / 1_024:.1f} MB"


# ─────────────────────────────────────────────────────────────────────────────
# Core download worker
# ─────────────────────────────────────────────────────────────────────────────
def download_one(
    folder: str,
    filename: str,
    base_url: str,
    root: Path,
    *,
    dry_run: bool,
    retries: int,
    position: int,
) -> Result:
    """Download a single PDF with retry, resume-check, and progress bar."""
    t0        = time.perf_counter()
    url       = base_url + filename
    dest_dir  = root / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename
    tmp_path  = dest_path.with_suffix(".tmp")

    # ── already complete? ────────────────────────────────────────────────────
    if dest_path.exists() and dest_path.stat().st_size >= MIN_FILE_BYTES:
        return Result(
            folder, filename, "skipped",
            size_kb=dest_path.stat().st_size // 1024,
            elapsed=time.perf_counter() - t0,
        )

    if dry_run:
        return Result(folder, filename, "downloaded",
                      reason="[dry-run]", elapsed=time.perf_counter() - t0)

    # ── retry loop ───────────────────────────────────────────────────────────
    last_error = "unknown error"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(
                url,
                headers=HEADERS,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                stream=True,
            )

            if resp.status_code == 404:
                last_error = "HTTP 404 – file not found on server"
                break                       # no point retrying

            if resp.status_code != 200:
                last_error = f"HTTP {resp.status_code}"
                time.sleep(2 ** attempt)
                continue

            total_bytes = int(resp.headers.get("content-length", 0))

            bar = tqdm(
                total=total_bytes or None,
                unit="B", unit_scale=True, unit_divisor=1024,
                desc=dim(f"  {filename[:46]:<46}"),
                leave=False,
                position=position,
                dynamic_ncols=True,
            )

            try:
                with tmp_path.open("wb") as fh:
                    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            fh.write(chunk)
                            bar.update(len(chunk))
            finally:
                bar.close()

            written = tmp_path.stat().st_size
            if written < MIN_FILE_BYTES:
                tmp_path.unlink(missing_ok=True)
                last_error = f"truncated response ({written} B)"
                time.sleep(2 ** attempt)
                continue

            tmp_path.rename(dest_path)
            return Result(
                folder, filename, "downloaded",
                size_kb=dest_path.stat().st_size // 1024,
                elapsed=time.perf_counter() - t0,
            )

        except requests.exceptions.Timeout:
            last_error = f"timeout (attempt {attempt}/{retries})"
        except requests.exceptions.ConnectionError as exc:
            last_error = f"connection error: {exc}"
        except OSError as exc:
            last_error = f"disk error: {exc}"
            break       # disk errors won't fix themselves

        if attempt < retries:
            time.sleep(2 ** attempt)

    tmp_path.unlink(missing_ok=True)
    return Result(folder, filename, "failed",
                  reason=last_error, elapsed=time.perf_counter() - t0)


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
def print_summary(results: list[Result], root: Path, elapsed: float) -> None:
    downloaded = [r for r in results if r.status == "downloaded"]
    skipped    = [r for r in results if r.status == "skipped"]
    failed     = [r for r in results if r.status == "failed"]

    dl_kb  = sum(r.size_kb for r in downloaded)
    all_kb = sum(r.size_kb for r in downloaded + skipped)

    print()
    print(bold("─" * 62))
    print(bold("  📚  Download Complete"))
    print(bold("─" * 62))
    print(f"  {green('✅  Downloaded')}   {len(downloaded):>3}  "
          f"  {dim(_human(dl_kb))} fetched this run")
    print(f"  {cyan('⏭   Skipped')}     {len(skipped):>3}  "
          f"  {dim('already on disk')}")
    print(f"  {red('❌  Failed') if failed else dim('❌  Failed')}       "
          f"{len(failed):>3}")
    print(bold("─" * 62))
    print(f"  💾  Total on disk   {_human(all_kb)}")
    print(f"  ⏱   Total time      {elapsed:.1f} s")
    print(f"  📁  Output folder   {root.resolve()}")

    if failed:
        print()
        print(bold(red(f"  Failed ({len(failed)}):")))
        for r in failed:
            print(f"    {red('✗')} {r.folder}/{r.filename}")
            if r.reason:
                print(f"        {dim(r.reason)}")

    print(bold("─" * 62))
    print()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download all Vedic Sanatana PDFs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--out",     "-o", default="Vedic_Sanatana_PDFs",
                   metavar="DIR",  help="Root output directory")
    p.add_argument("--workers", "-w", type=int, default=4,
                   metavar="N",   help="Parallel download threads (1–16)")
    p.add_argument("--retries", "-r", type=int, default=3,
                   metavar="N",   help="Max retry attempts per file")
    p.add_argument("--dry-run",       action="store_true",
                   help="Show what would download without writing files")
    return p.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> int:
    args    = parse_args()
    root    = Path(args.out)
    workers = max(1, min(args.workers, 16))
    retries = max(1, args.retries)
    total   = len(CATALOGUE)

    print()
    print(bold("  📚  Vedic Sanatana PDF Downloader"))
    print(f"  {dim('Saving to :')}  {root.resolve()}")
    print(f"  {dim('Files     :')}  {total}  │  "
          f"{dim('Workers:')} {workers}  │  "
          f"{dim('Retries:')} {retries}")
    if args.dry_run:
        print(f"  {yellow('⚠  DRY-RUN — nothing will be written to disk')}")
    print()

    results: list[Result] = [None] * total   # type: ignore[list-item]
    t_start = time.perf_counter()

    overall = tqdm(
        total=total,
        desc=bold("  Overall"),
        unit="file",
        position=0,
        dynamic_ncols=True,
    )

    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_idx = {
            pool.submit(
                download_one,
                folder, filename, base, root,
                dry_run=args.dry_run,
                retries=retries,
                position=(i % workers) + 1,
            ): i
            for i, (folder, filename, base) in enumerate(CATALOGUE)
        }

        for future in as_completed(future_to_idx):
            idx    = future_to_idx[future]
            result = future.result()
            results[idx] = result
            overall.update(1)

            if result.status == "downloaded":
                size_str = f"  {dim(_human(result.size_kb))}" if result.size_kb else ""
                overall.write(
                    f"  {green('✅')} {result.folder}/{result.filename}{size_str}"
                )
            elif result.status == "skipped":
                overall.write(
                    f"  {cyan('⏭')}  {result.folder}/{result.filename}"
                    f"  {dim('already exists')}"
                )
            else:
                overall.write(
                    f"  {red('❌')} {result.folder}/{result.filename}"
                    + (f"  {dim(result.reason)}" if result.reason else "")
                )

    overall.close()

    # filter out any None slots (shouldn't happen, but be safe)
    clean_results = [r for r in results if r is not None]
    print_summary(clean_results, root, time.perf_counter() - t_start)

    return 1 if any(r.status == "failed" for r in clean_results) else 0


if __name__ == "__main__":
    sys.exit(main())
