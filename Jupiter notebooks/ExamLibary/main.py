import numpy as np
import matplotlib.pyplot as plt
import csv
import os


def _detect_delimiter(filepath):
    lines = []
    with open(filepath, 'r') as f:
        for line in f:
            s = line.strip()
            if s and (s[0].isdigit() or s[0] in '-+.'):
                lines.append(line)
            if sum(len(l) for l in lines) >= 2048:
                break
    sample = ''.join(lines)
    try:
        detected = csv.Sniffer().sniff(sample).delimiter
        if detected in (',', ';', '\t', '|'):
            return detected
    except csv.Error:
        pass
    for char in ('\t', ',', ';'):
        if char in sample:
            return char
    return None


def _find_data_start(filepath):
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            s = line.strip()
            if s and (s[0].isdigit() or s[0] in '-+.'):
                return i
    return 0


def load(filepath, skip=None, orientation=None):
    """Return list of 1D arrays — one per column (vertical) or row (horizontal)."""
    delimiter = _detect_delimiter(filepath)
    if skip is None:
        skip = _find_data_start(filepath)
    data = np.genfromtxt(filepath, delimiter=delimiter, skip_header=skip,
                         filling_values=np.nan, invalid_raise=False)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    data = data[~np.isnan(data).all(axis=1)]
    data = data[:, ~np.isnan(data).all(axis=0)]
    horizontal = orientation == 'h' or (orientation is None and data.shape[1] > data.shape[0])
    if horizontal:
        return [data[i, :] for i in range(data.shape[0])]
    return [data[:, i] for i in range(data.shape[1])]


def plot(x, y, xlabel='x', ylabel='y', title='', **kwargs):
    plt.figure()
    plt.plot(x, y, **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.show()


def PMF(data, resolution):
    bin_centers = np.arange(np.min(data), np.max(data) + resolution / 1000, resolution)
    bin_edges = np.linspace(bin_centers[0] - resolution / 2,
                            bin_centers[-1] + resolution / 2, len(bin_centers) + 1)
    hist, _ = np.histogram(data, bin_edges)
    return bin_centers, hist / np.sum(hist)


def FWHM(x, y):
    idx = np.where(y >= np.max(y) / 2)[0]
    return abs(x[idx[-1]] - x[idx[0]])


# keep old names as aliases
FWHM1 = FWHM
FWHM2 = FWHM


def debug_all():
    base = os.path.dirname(os.path.abspath(__file__))
    files = [
        os.path.join(root, f)
        for root, _, filenames in os.walk(base)
        for f in sorted(filenames)
        if f.lower().endswith(('.txt', '.csv'))
    ]
    if not files:
        print(f"Keine Dateien gefunden in {base}")
        return
    for filepath in files:
        rel = os.path.relpath(filepath, base)
        try:
            cols = load(filepath)
            summary = ", ".join(f"col{i+1}({len(c)})" for i, c in enumerate(cols))
            print(f"  OK  {rel} → {summary}")
        except Exception as e:
            print(f"  ERR {rel} → {e}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    files = [(os.path.relpath(os.path.join(r, f), base), os.path.join(r, f))
             for r, _, fs in os.walk(base)
             for f in sorted(fs) if f.lower().endswith(('.txt', '.csv'))]
    if not files:
        print(f"Keine .txt/.csv Dateien in {base}")
    else:
        print('\033[2J\033[H', end='')
        print(f"Dateien in {base}:")
        for i, (display, _) in enumerate(files):
            print(f"  [{i}] {display}")
        try:
            filepath = files[int(input("\nNummer eingeben: ").strip())][1]
            print('\033[2J\033[H', end='')
            print(f"--- {os.path.basename(filepath)} (erste 5 Zeilen) ---")
            with open(filepath) as fh:
                for i, line in enumerate(fh):
                    if i >= 5:
                        break
                    print(f"  {line}", end='')
            print()
            orientation = input(f"[{os.path.basename(filepath)}] Vertikal oder lateral? [v/l]: ").strip().lower()
            skip_raw = input("Zeilen skippen (Enter = auto): ").strip()
            cols = load(filepath,
                        skip=int(skip_raw) if skip_raw.isdigit() else None,
                        orientation='v' if orientation == 'v' else 'h')
            print(f"\n{len(cols)} Spalten geladen:")
            for i, col in enumerate(cols):
                print(f"  data{i+1}: {len(col)} Werte")
        except (ValueError, IndexError):
            pass
