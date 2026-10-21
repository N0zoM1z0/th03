"""Exact historical CPU default fixture for unchanged earlier-owner tests."""
from pathlib import Path
import hashlib
PATH=Path(__file__).resolve().parent/'fixtures/th03_main_cpu_default.toml'
def historical_default_bytes():
 raw=PATH.read_bytes()
 if hashlib.sha256(raw).hexdigest()!='001a6d04b0a7b35667b452d85e288935622597cf051c7c4646e66a5964cbf3c8':raise ValueError('historical CPU default fixture drift')
 return raw
def historical_default_text():return historical_default_bytes().decode('utf-8')
