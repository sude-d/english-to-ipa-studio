import subprocess
from pathlib import Path
VOICES = {
    "American English": "en-us",
    "British English": "en-gb"
}
ESPEAK_PATHS = [
    Path(r"C:\Program Files\eSpeak NG\espeak-ng.exe"),
    Path(r"C:\Program Files (x86)\eSpeak NG\espeak-ng.exe")
]
def convert_to_ipa(text, accent):
    text = text.strip()
    if not text:
        raise ValueError("Please enter some text.")
    if len(text) > 5000:
        raise ValueError("Text must not exceed 5000 characters.")
    if accent not in VOICES:
        raise ValueError("Unsupported accent.")
    executable = next(
        (path for path in ESPEAK_PATHS if path.is_file()),
        None
    )
    if executable is None:
        raise FileNotFoundError(
            "eSpeak NG was not found. Please check the installation path."
        )
    result = subprocess.run(
        [
            str(executable),
            "-q",
            "--ipa=3",
            "-v",
            VOICES[accent],
            text
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "IPA conversion failed."
        )
    if not result.stdout.strip():
        raise RuntimeError("No IPA output was generated.")
    return result.stdout.strip()
