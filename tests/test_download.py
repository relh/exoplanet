from types import SimpleNamespace
import pytest
import requests
from exoplanet.pipeline import fetch


def test_transient_failure_retries_without_creating_false_cache(tmp_path,monkeypatch):
    attempts=[];delays=[]
    def get(url,**kwargs):
        attempts.append(url)
        if len(attempts)==1:raise requests.ConnectionError('temporary DNS failure')
        return SimpleNamespace(url=url,content=b'actual archive content',raise_for_status=lambda:None)
    monkeypatch.setattr('exoplanet.pipeline.requests.get',get)
    monkeypatch.setattr('exoplanet.pipeline.time.sleep',delays.append)
    path=tmp_path/'archive.bin';meta=fetch('https://example.org/data',path)
    assert path.read_bytes()==b'actual archive content'
    assert meta['download_attempts']==2 and len(meta['transient_failures'])==1
    assert delays==[2]
    assert fetch('https://example.org/data',path)==meta
    assert len(attempts)==2


def test_http_error_is_not_retried_or_saved_as_data(tmp_path,monkeypatch):
    attempts=[]
    def error():raise requests.HTTPError('404')
    def get(url,**kwargs):
        attempts.append(url)
        return SimpleNamespace(raise_for_status=error)
    monkeypatch.setattr('exoplanet.pipeline.requests.get',get)
    path=tmp_path/'absent.bin'
    with pytest.raises(requests.HTTPError):fetch('https://example.org/absent',path)
    assert len(attempts)==1 and not path.exists()
