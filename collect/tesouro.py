import csv
import json
from findt import FinDt


def ir(dias_uteis):
    retorno = None
    if dias_uteis < 180:
        retorno = 22.5
    if 181 <= dias_uteis < 360:
        retorno = 20
    if 361 <= dias_uteis < 720:
        retorno = 17.5
    if dias_uteis > 720:
        retorno = 15

    return retorno / 100.0


def csvtojson(file): # TODO copiado, refatorar para funcionar no código
    csvfile = open('file.csv', 'r')
    jsonfile = open('file.json', 'w')

    fieldnames = ("FirstName", "LastName", "IDNumber", "Message")
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')


class Tselic:
    def __init__(self, valor_investido=None, taxa_periodo=None, dCompra=None, dVenda=None, dVencimento=None,
                 txCustodia=None, txAdm=None):
        self.dCompra = dCompra
        self.dVencimento = dVencimento
        self.dVenda = dVenda
        self.VI = valor_investido
        self.VU = None
        self.taxaAdm = txAdm
        self.taxaCustodia = txCustodia
        self.taxaSelicPeriodo = taxa_periodo
        self.lucroBruto = None
        self.lucroliq = None
        self.lucro = None
        self.custototal = None

    def calc(self):
        # try:
        periodo = FinDt.DatasFinanceiras(self.dCompra, self.dVenda)
        diasuteis = len(periodo.dias(2, 'str'))
        self.faturamento = self.VI * (1 + self.taxaSelicPeriodo) ** (diasuteis / 252.0)  # qto vale o investimento
        self.lucroBruto = self.faturamento - self.VI  # diferença entre o eu tenho hj e o que eu investi
        self.rendimentobruto = self.faturamento / self.VI
        taxaCustodiaResgate = ((self.faturamento - self.VI) / 2 + self.VI) * (
            (1 + self.taxaCustodia) ** (diasuteis / 252.0) - 1)
        taxaAdmResgate = ((self.faturamento - self.VI) / 2 + self.VI) * (
            (1 + self.taxaAdm) ** ((diasuteis - 252.0) / 252.0) - 1)
        aliquotaIR = ir(diasuteis)
        DescontoIR = (self.lucroBruto - taxaCustodiaResgate - taxaAdmResgate) * aliquotaIR
        self.custototal = taxaAdmResgate + taxaCustodiaResgate + DescontoIR
        self.lucroliq = self.faturamento - self.custototal
        rend_liq = (self.lucroliq / self.VI) ** (252.0 / diasuteis) - 1
        retorno = rend_liq

        return retorno


class Tipca:
    def __init__(self, valor_investido=None, taxa_periodo=None, taxa_compra=None, dCompra=None, dVenda=None,
                 dVencimento=None,
                 txCustodia=None, txAdm=None):
        self.dCompra = dCompra  # data de compra
        self.dVencimento = dVencimento  # data de vencimento
        self.dVenda = dVenda  # Data de Venda
        self.VI = valor_investido  # Valor Investido
        self.TxCompra = taxa_compra  # Taxa de compra
        self.TxAdm = txAdm  # Taxa de Administração
        self.TxCustodia = txCustodia  # Taxa de Custódia
        self.IPCAprd = taxa_periodo  # IPCA do período
        self.VU = None  # Valor Unitário de investimento
        self.lucroBruto = None
        self.lucroliq = None
        self.lucro = None
        self.custototal = None

    def calc(self):
        periodo = FinDt.DatasFinanceiras(self.dCompra, self.dVenda)
        diasuteis = len(periodo.dias(2, 'str'))
        self.faturamento = self.VI * ((1 + self.IPCAprd) * (1 + self.TxCompra)) ** (diasuteis / 252.0)
        self.lucroBruto = self.faturamento - self.VI
        taxaCustodiaResgate = (self.lucroBruto / self.VI) ** (252.0 / diasuteis)
        taxaAdmResgate = ((self.lucroBruto - self.VI) / 2.0 + self.VI) * (
            (1 + self.TxAdm) ** ((diasuteis - 252.0) / 252.0) - 1)
        aliquotaIR = ir(diasuteis)
        descontoIR = (self.lucroBruto - taxaCustodiaResgate - taxaAdmResgate) * aliquotaIR
        self.custototal = taxaAdmResgate + taxaCustodiaResgate + descontoIR
        self.lucroliq = self.faturamento - self.custototal
        rend_liq = (self.lucroliq / self.VI) ** (252.0 / diasuteis) - 1
        retorno = rend_liq

        return retorno


# TODO Incluir feriados na conta
if __name__ == "__main__":
    # Declaração dos parâmetros
    vi = 1000
    txp = 0.1
    txc = 0.04
    data_compra = '01/01/2016'
    data_venda = '01/02/2016'
    txCustodia = 0.03
    txAdm = 0

    # Declaração dos Investimentos
    print('Investimento Tesouro Selic')
    t = Tselic(vi, txp, data_compra, data_venda, txCustodia=txCustodia, txAdm=txAdm)
    t.calc()
    print('%s reais a %s %% no período' % (vi, txp))
    print('Lucro Bruto: %s, Lucro Liq: %s, Descontos: %s' % (t.lucroBruto, t.lucroliq, t.custototal))
    print('%f %%' % (t.calc() * 100))

    print('Investimento Tesouro IPCA')
    t = Tipca(vi, txp, txc, data_compra, data_venda, txCustodia=txCustodia, txAdm=txAdm)
    t.calc()
    print('%s reais a %s %% no período' % (vi, txp))
    print('Lucro Bruto: %s, Lucro Liq: %s, Descontos: %s' % (t.lucroBruto, t.lucroliq, t.custototal))
    print('%f %%' % (t.calc() * 100))
