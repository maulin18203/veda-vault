# 📚 Vedic Sanatana — shub Library

> Complete offline digital library of Hindu sacred texts — Vedas, Puranas, Upanishads, Itihas, and Smriti — downloaded and organized into category folders.

**Source:** [vedpuran.net](https://vedpuran.net) — Free Hindi/Sanskrit PDF repository  
**Total Files:** 48 PDFs  
**Total Size:** ~2.6 GB  
**Script:** `download_shub.py`

---

## 📁 Folder Structure

```
shub/
├── Vedas/             →   5 files  (~)
├── Puranas/           →  23 files  (~848 MB)
├── Upanishads/        →   5 files  (~173 MB)
├── Itihas/            →  10 files  (~1.4 GB)
├── Smriti/            →   4 files  (~145 MB)
│
├── download_log.txt   →  status of every file
└── failed_urls.txt    →  only created if any file fails
```

---

## ⚙️ Requirements

| Requirement | Details |
|---|---|
| Python | 3.8 or higher |
| Library | `requests` |
| Disk Space | 2.6 GB+ free |
| OS | Windows / Linux / macOS |

---

## 🚀 Setup & Run Steps

### Step 1 — Install Python (if not already)
```bash
# Check if Python is installed
python --version
# or
python3 --version
```
Download from: https://www.python.org/downloads/

---

### Step 2 — Install the `requests` library
```bash
pip install requests
```

---

### Step 3 — Place the script
Put `download_shub.py` anywhere on your computer.  
The `shub/` folder will be created **automatically** in the same directory.

---

### Step 4 — Run the script
```bash
python download_shub.py
```
or on Linux/macOS:
```bash
python3 download_shub.py
```

---

### Step 5 — If any file fails, just re-run
```bash
python download_shub.py
```
The script **resumes from where it stopped** (HTTP Range support).  
Already-complete files are skipped instantly.

---

## 📖 Complete Book List

### 1. 🕉️ Vedas (वेद)
`shub/Vedas/` — 5 files

| # | File Name | Language | Source URL |
|---|---|---|---|
| 1 | `Rigveda_Complete_Hindi_GitaPress.pdf` | Hindi | vedpuran.net/wp-content/uploads/2011/10/rigved.pdf |
| 2 | `Yajurveda_Shukla_Hindi.pdf` | Hindi | vedpuran.net/wp-content/uploads/2011/10/yajurved.pdf |
| 3 | `Samaveda_Hindi.pdf` | Hindi | vedpuran.net/wp-content/uploads/2011/10/samved.pdf |
| 4 | `Atharvaveda_Hindi_Part1.pdf` | Hindi | vedpuran.net/wp-content/uploads/2011/10/arthved-part-1.pdf |
| 5 | `Atharvaveda_Hindi_Part2.pdf` | Hindi | vedpuran.net/wp-content/uploads/2011/10/atharva-2.pdf |

---

### 2. 📜 Puranas (पुराण)
`shub/Puranas/` — 23 files

| # | File Name | Size | Notes |
|---|---|---|---|
| 1 | `Agni_Puran.pdf` | ~57 MB | Agni Purana |
| 2 | `Bhagwat_Puran.pdf` | ~63 MB | Shrimad Bhagavata |
| 3 | `Bhavishya_Puran.pdf` | ~27 MB | Bhavishya Purana |
| 4 | `Brahma_Puran.pdf` | ~36 MB | Brahma Purana |
| 5 | `Brahmand_Puran_Part1.pdf` | ~48 MB | Brahmanda — Part 1 |
| 6 | `Brahmand_Puran_Part2.pdf` | ~25 MB | Brahmanda — Part 2 |
| 7 | `Garuda_Puran.pdf` | ~32 MB | Garuda Purana |
| 8 | `Kurma_Puran.pdf` | ~22 MB | Kurma Purana |
| 9 | `Ling_Puran.pdf` | ~14 MB | Linga Purana |
| 10 | `Markandya_Puran.pdf` | ~18 MB | Markandeya Purana |
| 11 | `Matsya_Puran_Part1.pdf` | ~27 MB | Matsya Purana — Part 1 |
| 12 | `Matsya_Puran_Part2.pdf` | ~26 MB | Matsya Purana — Part 2 |
| 13 | `Narad_Puran.pdf` | ~47 MB | Narada Purana |
| 14 | `Padma_Puran.pdf` | ~72 MB | Padma Purana |
| 15 | `Shiv_Puran.pdf` | ~49 MB | Shiva Purana |
| 16 | `Skand_Puran.pdf` | ~74 MB | Skanda Purana |
| 17 | `BrahmVaivarta_Puran.pdf` | ~52 MB | Brahma Vaivarta Purana |
| 18 | `Vaman_Puran.pdf` | ~12 MB | Vamana Purana |
| 19 | `Varah_Puran.pdf` | ~24 MB | Varaha Purana |
| 20 | `Vishnu_Puran.pdf` | ~40 MB | Vishnu Purana |
| 21 | `Vayu_Puran.pdf` | ~52 MB | Vayu Purana |
| 22 | `Kalki_Puran.pdf` | ~13 MB | Kalki Purana |
| 23 | `Narsimha_Puran_Upapuran.pdf` | ~20 MB | Narasimha Purana *(Upapurana)* |

---

### 3. 🧘 Upanishads (उपनिषद) & Philosophy
`shub/Upanishads/` — 5 files

| # | File Name | Size | Notes |
|---|---|---|---|
| 1 | `108_Upanishads_with_Commentary.pdf` | ~148 MB | All 108 Upanishads with Upanishad Brahmam commentary |
| 2 | `The_Upanishads_Intro_Edition.pdf` | ~1.7 MB | Introductory short edition |
| 3 | `Vedant_Darshan_Brahmasutra_Hindi_Sanskrit.pdf` | ~14 MB | Gita Press — Vedanta Darshan, Brahmasutra |
| 4 | `Brahmasutra_Sanskrit.pdf` | ~2.2 MB | Pure Sanskrit text |
| 5 | `Vivek_Chudamani_Shankaracharya.pdf` | ~7.5 MB | Vivekachudamani by Adi Shankaracharya |

---

### 4. ⚔️ Itihas (इतिहास) — Epics & Major Texts
`shub/Itihas/` — 10 files

| # | File Name | Size | Notes |
|---|---|---|---|
| 1 | `Mahabharat_Complete_GitaPress_7250pages.pdf` | **~710 MB** | Gorakhpur Press, Vol 1–12, 7250 pages |
| 2 | `Mahabharat_Full_with_Geeta_Hindi.pdf` | **~272 MB** | Full Mahabharat + Bhagavad Gita, Hindi |
| 3 | `Valmiki_Ramayan_All_Kands_6191pages.pdf` | **~183 MB** | All Kands, 6191 pages, Hindi-Sanskrit |
| 4 | `Shri_Ramcharitmanas_Complete_Tulsidas.pdf` | ~10 MB | Complete Tulsidas Ramcharitmanas |
| 5 | `Anand_Ramayan_Hindi.pdf` | **~294 MB** | Ananda Ramayana — Hindi |
| 6 | `Shrimad_Bhagavad_Geeta_GitaPress.pdf` | ~486 KB | Bhagavad Gita, Gorakhpur Press |
| 7 | `Yoga_Vashishtha_Maharamayan_Part1.pdf` | ~1.8 MB | Yoga Vasishtha / Maha Ramayana — Part 1 |
| 8 | `Yoga_Vashishtha_Maharamayan_Part2.pdf` | ~1.4 MB | Yoga Vasishtha — Part 2 |
| 9 | `Yoga_Vashishtha_Maharamayan_Part3.pdf` | ~1.3 MB | Yoga Vasishtha — Part 3 |
| 10 | `Yoga_Vashishtha_Maharamayan_Part4.pdf` | ~3.2 MB | Yoga Vasishtha — Part 4 |

> ⚠️ Files marked **bold** are very large. On a 10 Mbps connection, expect 5–15 minutes each.

---

### 5. 📐 Smriti (स्मृति) & Sciences
`shub/Smriti/` — 4 files

| # | File Name | Size | Notes |
|---|---|---|---|
| 1 | `Manusmriti_Hindi_Sanskrit.pdf` | ~21 MB | Manusmriti — Hindi + Sanskrit |
| 2 | `Manusmriti_English.pdf` | ~564 KB | Manusmriti — English translation |
| 3 | `Bhrigu_Samhita_Hindi.pdf` | **~111 MB** | Bhrigu Samhita फलित दर्पण — Hindi (110 MB) |
| 4 | `Vimanika_Shastra_Aeronautical.pdf` | ~13 MB | Vaimanika Shastra — Ancient aeronautical science |

---

## 🔄 How Resume Works

If your internet drops mid-download:

```bash
# Just re-run — the script picks up exactly where it stopped
python download_shub.py
```

The script sends an HTTP `Range: bytes=N-` header to the server, so only the **remaining bytes** are downloaded — not the whole file again.

---

## 📊 Download Summary (example output)

```
╔══════════════════════════════════════════════════════╗
║   VEDIC SANATANA — Full Library Downloader           ║
║   48 files  |  ~2.5 GB total                         ║
╚══════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────
  1. VEDAS  (वेद)
──────────────────────────────────────────────────────
[1/48] Rigveda_Complete_Hindi_GitaPress.pdf
  ✔ Already complete (33.8 MB) — nothing to do

[2/48] Yajurveda_Shukla_Hindi.pdf
  📁  shub/Vedas/
  [███████████████████████████████████] 100.0%  ✔ Done

══════════════════════════════════════════════════════
  DOWNLOAD COMPLETE — SUMMARY
══════════════════════════════════════════════════════
  Total in list    :  48
  ✔ Downloaded now :  3
  ✔ Already had    :  45
  ✘ Failed         :  0
  ✔ Total complete :  48

    📂  Vedas           5 file(s)
    📂  Puranas        23 file(s)   848.5 MB
    📂  Upanishads      5 file(s)   173.4 MB
    📂  Itihas         10 file(s)   1.4 GB
    📂  Smriti          4 file(s)   145.1 MB

  All files downloaded successfully! 🙏
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: requests` | Run `pip install requests` |
| `HTTP 404` error on a file | URL may have changed on server — re-check vedpuran.net |
| Download very slow | Normal for large files; script will not timeout — just wait |
| File stuck at 0% | Check internet connection; Ctrl+C and re-run to resume |
| Partial file after crash | Re-run script — it resumes automatically via HTTP Range |
| `Permission denied` on folder | Run terminal as Administrator (Windows) or use `sudo` (Linux) |
| Python not found | Make sure Python is in your system PATH |

---

## 📝 Log Files

After each run, two files are written inside `shub/`:

**`download_log.txt`** — status of every file:
```
Download started : 2026-06-29 00:07:37

[DONE-EXISTS]  Rigveda_Complete_Hindi_GitaPress.pdf  (33.8 MB)
[OK]           Yajurveda_Shukla_Hindi.pdf  (22.1 MB)
[FAILED]       some_file.pdf  — HTTP 404

Download finished: 2026-06-29 00:09:22
Total: 48  |  Downloaded: 45  |  Already had: 3  |  Failed: 0
```

**`failed_urls.txt`** — only created if something fails:
```
https://some-url.pdf  →  shub/Vedas/some_file.pdf
```

---

## 📦 All 48 Files — Quick Reference

```
shub/
│
├── Vedas/  (5 files)
│   ├── Rigveda_Complete_Hindi_GitaPress.pdf
│   ├── Yajurveda_Shukla_Hindi.pdf
│   ├── Samaveda_Hindi.pdf
│   ├── Atharvaveda_Hindi_Part1.pdf
│   └── Atharvaveda_Hindi_Part2.pdf
│
├── Puranas/  (23 files)
│   ├── Agni_Puran.pdf
│   ├── Bhagwat_Puran.pdf
│   ├── Bhavishya_Puran.pdf
│   ├── Brahma_Puran.pdf
│   ├── Brahmand_Puran_Part1.pdf
│   ├── Brahmand_Puran_Part2.pdf
│   ├── Garuda_Puran.pdf
│   ├── Kurma_Puran.pdf
│   ├── Ling_Puran.pdf
│   ├── Markandya_Puran.pdf
│   ├── Matsya_Puran_Part1.pdf
│   ├── Matsya_Puran_Part2.pdf
│   ├── Narad_Puran.pdf
│   ├── Padma_Puran.pdf
│   ├── Shiv_Puran.pdf
│   ├── Skand_Puran.pdf
│   ├── BrahmVaivarta_Puran.pdf
│   ├── Vaman_Puran.pdf
│   ├── Varah_Puran.pdf
│   ├── Vishnu_Puran.pdf
│   ├── Vayu_Puran.pdf
│   ├── Kalki_Puran.pdf
│   └── Narsimha_Puran_Upapuran.pdf
│
├── Upanishads/  (5 files)
│   ├── 108_Upanishads_with_Commentary.pdf
│   ├── The_Upanishads_Intro_Edition.pdf
│   ├── Vedant_Darshan_Brahmasutra_Hindi_Sanskrit.pdf
│   ├── Brahmasutra_Sanskrit.pdf
│   └── Vivek_Chudamani_Shankaracharya.pdf
│
├── Itihas/  (10 files)
│   ├── Mahabharat_Complete_GitaPress_7250pages.pdf   ⚠ 710 MB
│   ├── Mahabharat_Full_with_Geeta_Hindi.pdf          ⚠ 272 MB
│   ├── Valmiki_Ramayan_All_Kands_6191pages.pdf       ⚠ 183 MB
│   ├── Shri_Ramcharitmanas_Complete_Tulsidas.pdf
│   ├── Anand_Ramayan_Hindi.pdf                       ⚠ 294 MB
│   ├── Shrimad_Bhagavad_Geeta_GitaPress.pdf
│   ├── Yoga_Vashishtha_Maharamayan_Part1.pdf
│   ├── Yoga_Vashishtha_Maharamayan_Part2.pdf
│   ├── Yoga_Vashishtha_Maharamayan_Part3.pdf
│   └── Yoga_Vashishtha_Maharamayan_Part4.pdf
│
└── Smriti/  (4 files)
    ├── Manusmriti_Hindi_Sanskrit.pdf
    ├── Manusmriti_English.pdf
    ├── Bhrigu_Samhita_Hindi.pdf                      ⚠ 111 MB
    └── Vimanika_Shastra_Aeronautical.pdf
```

---

## 🙏 Source & Credits

All PDFs are sourced from **[vedpuran.net](https://vedpuran.net)** — a free public service  
providing Hindu religious texts in PDF format for personal study and spiritual reading.

> *"वेदो अखिलो धर्ममूलम्"* — The Vedas are the root of all Dharma.

**Jai Shri Ram 🙏**
