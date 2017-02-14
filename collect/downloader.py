import requests

url = "http://sisweb.tesouro.gov.br/apex/COSIS_SISTD.obtem_arquivo?p_id=248:9319"

r = requests.get(url)
with open('../Download/teste.xls', 'wb') as test:
    test.write(r.content)