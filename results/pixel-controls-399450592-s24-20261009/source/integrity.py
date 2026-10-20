"""Verify FITS CHECKSUM over original HDU bytes, including data and padding."""
import numpy as np


def verify_hdus(path, hdus):
    """FITS one's-complement convention; supports CHECKSUM without DATASUM.

    Astropy 8.0.1 verify_checksum assumes a zero data sum when DATASUM is
    absent. TESS-SPOC products can omit DATASUM while providing valid CHECKSUM.
    https://fits.gsfc.nasa.gov/registry/checksum.html
    """
    results = []
    with path.open("rb") as stream:
        for hdu in hdus:
            if "CHECKSUM" not in hdu.header:
                results.append({"hdu": hdu.name, "checksum": "missing"})
                continue
            info = hdu.fileinfo()
            length = info["datLoc"] + info["datSpan"] - info["hdrLoc"]
            stream.seek(info["hdrLoc"])
            remaining, total = length, 0
            while remaining:
                data = stream.read(min(remaining, 1024 * 1024))
                if not data or len(data) % 4:
                    raise ValueError("Truncated FITS HDU")
                total += int(np.frombuffer(data, dtype=">u4").sum(dtype=np.uint64))
                while total >> 32:
                    total = (total & 0xFFFFFFFF) + (total >> 32)
                remaining -= len(data)
            if total != 0xFFFFFFFF:
                raise ValueError(f"Invalid FITS CHECKSUM for {hdu.name}")
            results.append({"hdu": hdu.name, "checksum": "verified"})
    return results
