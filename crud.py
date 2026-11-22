import logging
from sqlmodel import Session, select

from models import engine, envanter
from contextlib import contextmanager
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


class VeritabaniHatasi(Exception):
    pass


@contextmanager
def oturum():
    try:
        with Session(engine) as session:
            yield session
    except OperationalError as e:
        logger.exception("Veritabanı bağlantı hatası: %s", e.orig)
        raise VeritabaniHatasi("Veritabanına bağlanılamadı") from e


# CRUD
# SELECT, veritabanında olamayan bir şey için exception,sql hatası dönmesin belirli hata dönsün,
# logger kullanalım,veritabanı bağlantısı için exception, hata alırsak ai,

class UrunBulunamadi(Exception):
    pass


def urun_getir(urun_id):
    with Session(engine) as session:
        urun = session.get(envanter, urun_id)
        if urun is None:
            raise UrunBulunamadi(f"{urun_id} numaralı ürün bulunamadı")
        return urun


def urun_listele(aranan=None):
    with Session(engine) as session:
        sorgu = select(envanter)
        if aranan is not None:
            sorgu = sorgu.where(envanter.ad.icontains(aranan))
        result = session.exec(sorgu).all()
        return result


def urun_ekle(data):
    urun = envanter.model_validate(data)
    with Session(engine) as session:
        session.add(urun)
        session.commit()
        session.refresh(urun)
        logger.info("Ürün Eklendi: id=%s", urun.id)
        return urun


def urun_sil(urun_id):
    with Session(engine) as session:
        urun = session.get(envanter, urun_id)
        if urun is None:
            raise UrunBulunamadi(f"{urun_id} numaralı ürün bulunamadı")
        session.delete(urun)
        session.commit()
        logger.info("Ürün Silindi: id=%s", urun.id)
        return True


def urun_guncelle(urun_id, stok, fiyat):
    with Session(engine) as session:
        urun = session.get(envanter, urun_id)
        if urun is None:
            raise UrunBulunamadi(f"{urun_id} numaralı ürün bulunamadı")
        urun.stok = stok
        urun.fiyat = fiyat
        session.add(urun)
        session.commit()
        session.refresh(urun)
        logger.info("Ürün Güncellendi: id=%s", urun.id)
        return urun
