#Currently only DAX index is implemented (hardcoded)

def GetListOfCompaniesInIndex():
    companies = [
        'Adidas',
        'Allianz',
        'BASF',
        'Bayer',
        'Beiersdorf',
        'BMW',
        'Continental',
        'Covestro',
        'Daimler',
        'Deutsche Bank',
        'Deutsche Börse',
        'Deutsche Post',
        'Deutsche Telekom',
        'Deutsche Wohnen',
        'E.ON',
        'Fresenius',
        'Fresenius Medical Care',
        'HeidelbergCement',
        'Henkel',
        'Infineon Technologies',
        'Linde',
        'Merck',
        'MTU Aero Engines',
        'Munich Re',
        'RWE',
        'SAP',
        'Siemens',
        'Volkswagen Group',
        'Vonovia',
        'Wirecard']

    return(companies)




Tickers = {
    'Adidas':'ADS.DE',
    'Allianz':'ALV.DE',
    'BASF':'BAS.DE',
    'Bayer':'BAYN.DE',
    'Beiersdorf':'BEI.DE',
    'BMW':'BMW.DE',
    'Continental':'CON.DE',
    'Covestro':'1COV.DE',
    'Daimler':'DAI.DE',
    'Deutsche Bank':'DBK.DE',
    'Deutsche Börse':'DB1.DE',
    'Deutsche Post':'DPW.DE',
    'Deutsche Telekom':'DTE.DE',
    'Deutsche Wohnen':'DWNI.DE',
    'E.ON':'EOAN.DE',
    'Fresenius':'FRE.DE',
    'Fresenius Medical Care':'FME.DE',
    'HeidelbergCement':'HEI.DE',
    'Henkel':'HEN3.DE',
    'Infineon Technologies':'IFX.DE',
    'Linde':'LIN.DE',
    'Merck':'MRK.DE',
    'MTU Aero Engines':'MTX.DE',
    'Munich Re':'MUV2.DE',
    'RWE':'RWE.DE',
    'SAP':'SAP.DE',
    'Siemens':'SIE.DE',
    'Volkswagen Group':'VOW3.DE',
    'Vonovia':'VNA.DE',
    'Wirecard':'WDI.DE'
}


def GetCompanyTicker(company):
    return(Tickers[company])