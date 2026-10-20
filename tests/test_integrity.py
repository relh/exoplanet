import numpy as np
import pytest
from astropy.io import fits
from exoplanet.integrity import verify_hdus


def test_valid_checksum_without_datasum_and_corruption(tmp_path):
    path = tmp_path / 'test.fits'
    hdu = fits.PrimaryHDU(np.arange(32, dtype=np.int32))
    hdu.add_checksum(override_datasum=True)
    assert 'DATASUM' not in hdu.header
    hdu.writeto(path)
    with fits.open(path) as hdus:
        assert verify_hdus(path, hdus)[0]['checksum'] == 'verified'
        loc = hdus[0].fileinfo()['datLoc']
    with path.open('r+b') as stream:
        stream.seek(loc)
        stream.write(b'\xff')
    with fits.open(path) as hdus, pytest.raises(ValueError, match='Invalid FITS CHECKSUM'):
        verify_hdus(path, hdus)
