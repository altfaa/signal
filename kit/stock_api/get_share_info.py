from kit.tokens.tinkoff import token
from tinkoff.invest import Client, InstrumentIdType
from kit.catalog.get_full_moex_dicts import figi_to_name_dict

print("")
# figi_to_name_dict
figi = "BBG004730N88"
with Client(token) as client:
    for figi in figi_to_name_dict:
        share = client.instruments.share_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=figi
        )
        print(f"{figi};{share.instrument.ticker};{share.instrument.name};{share.instrument.country_of_risk};{share.instrument.currency};{share.instrument.lot}")

