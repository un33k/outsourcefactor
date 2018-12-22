# coding: utf-8
import urllib2, urllib, json, re, random, json
from decimal import Decimal
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.cache import cache
from uuslug import uuslug as slugify

PRIORITY_CURRENCIES = [
    ('PHP', _('Philippine - Peso [PHP]')),
    ('KES', _('Kenya - Schilling [KES]')),
    ('PKR', _('Pakistan - Rupee [PKR]')),
    ('INR', _('India - Rupee [INR]')),
    ('BDT', _('Bangladesh - Taka [BDT]')),
    ('IDR', _('Indonesia - Rupiah [IDR]')),
    ('EUR', _('Europe - Euro [EUR]')),
    ('CAD', _('Canada - Dollar [CAD]')),
    ('AUD', _('Australia - Dollar [AUD]')),
    ('NZD', _('New Zealand - Dollar [NZD]')),
    ('USD', _('United States - Dollar [USD]')),
    ('GBP', _('United Kingdom - Pound [GBP]')),

    ('', _('___________')),
]

ALL_CURRENCIES = [
    ('AED', _('United Arab Emirates - Dirham [AED]')),
    ('AFN', _('Afghanistan - Afghani [AFN]')),
    ('ALL', _('Albania - Lek [ALL]')),
    ('AMD', _('Armenia - Dram [AMD]')),
    ('ANG', _('Netherlands Antilles - Guilder [ANG]')),
    ('AOA', _('Angola - Kwanza [AOA]')),
    ('ARS', _('Argentina - Peso [ARS]')),
    ('AUD', _('Australia - Dollar [AUD]')),
    ('AWG', _('Aruba - Florin [AWG]')),
    ('AZN', _('Azerbaijan - Manat [AZN]')),
    ('BAM', _('Bosnia and Herzegovina - Convertible Mark [BAM]')),
    ('BBD', _('Barbados - Dollar [BBD]')),
    ('BDT', _('Bangladesh - Taka [BDT]')),
    ('BGN', _('Bulgaria - Lev [BGN]')),
    ('BHD', _('Bahrain - Dinar [BHD]')),
    ('BIF', _('Burundi - Franc [BIF]')),
    ('BMD', _('Bermuda - Dollar [BMD]')),
    ('BND', _('Brunei Darussalam - Dollar [BND]')),
    ('BOB', _('Bolivia - Boliviano [BOB]')),
    ('BRL', _('Brazil - Real [BRL]')),
    ('BSD', _('Bahama - Dollar [BSD]')),
    ('BTN', _('Bhutan - Ngultrum [BTN]')),
    ('BWP', _('Botswana - Pula [BWP]')),
    ('BYR', _('Belarus - Ruble [BYR]')),
    ('BZD', _('Belize - Dollar [BZD]')),
    ('CAD', _('Canada - Dollar [CAD]')),
    ('CDF', _('Congo - Franc [CDF]')),
    ('CHF', _('Switzerland - Franc [CHF]')),
    ('CLP', _('Chile - Peso [CLP]')),
    ('CNY', _('China - Yuan Renminbi [CNY]')),
    ('COP', _('Colombia - Peso [COP]')),
    ('CRC', _('Costa Rica - Colon [CRC]')),
    ('CUP', _('Cuba - Peso [CUP]')),
    ('CVE', _('Cape Verde - Escudo [CVE]')),
    ('CZK', _('Czech Republic - Koruna [CZK]')),
    ('DJF', _('Djibouti - Franc [DJF]')),
    ('DKK', _('Denmark - Krone [DJF]')),
    ('DMA', _('Dominica - Peso [DMA]')),
    ('DOP', _('Dominican Republic - Peso [DOP]')),
    ('DZD', _('Algeria - Dinar [DZD]')),
    ('EEK', _('Estonia - Kroon [EEK]')),
    ('EGP', _('Egypt - Pound [EGP]')),
    ('ERN', _('Eritrea - Nakfa [ERN]')),
    ('ETB', _('Ethiopia - Birr [ETB]')),
    ('FJD', _('Fiji - Dollar [FJD]')),
    ('FKP', _('Falkland Islands (Malvinas) - Pound [FKP]')),
    ('GBP', _('United Kingdom - Pound Sterling [GBP]')),
    ('GEL', _('Georgia - Lari [GEL]')),
    ('GHS', _('Ghana - Cedi [GHS]')),
    ('GIP', _('Gibraltar - Pound [GIP]')),
    ('GMD', _('Gambia - Dalasi [GMD]')),
    ('GNF', _('Guinea - Franc [GNF]')),
    ('GTQ', _('Guatemala - Quetzal [GTQ]')),
    ('GTQ', _('Guyana - Dollar [GTQ]')),
    ('HKD', _('Hong Kong - Dollar [HKD]')),
    ('HNL', _('Honduras - Lempira [HNL]')),
    ('HRK', _('Croatia - Kuna [HRK]')),
    ('HTG', _('Haiti - Gourde [HTG]')),
    ('HUF', _('Hungary - Forint [HUF]')),
    ('IDR', _('Indonesia - Rupiah [IDR]')),
    ('ILS', _('Israel - New Shekel [ILS]')),
    ('INR', _('India - Rupee [INR]')),
    ('IQD', _('Iraq - Dinar [IQD]')),
    ('IRR', _('Iran - Rial [IRR]')),
    ('ISK', _('Iceland - Krona [ISK]')),
    ('JMD', _('Jamaica - Dollar [JMD]')),
    ('JOD', _('Jordan - Dinar [JOD]')),
    ('JPY', _('Japan - Yen [JPY]')),
    ('KES', _('Kenya - Schilling [KES]')),
    ('KGS', _('Kyrgyzstan - Som [KGS]')),
    ('KHR', _('Cambodia - Riel [KHR]')),
    ('KMF', _('Comoros - Franc [KMF]')),
    ('KPW', _('North Korea - Won [KPW]')),
    ('KRW', _('South Korea - Won [KRW]')),
    ('KWD', _('Kuwait - Dinar [KWD]')),
    ('KYD', _('Cayman Islands - Dollar [KYD]')),
    ('KZT', _('Kazakhstan - Tenge [KZT]')),
    ('LAK', _('Lao - Kip [LAK]')),
    ('LBP', _('Lebanon - Pound [LBP]')),
    ('LKR', _('Sri Lanka - Rupee [LKR]')),
    ('LRD', _('Liberia - Dollar [LRD]')),
    ('LSL', _('Lesotho - Loti [LSL]')),
    ('LTL', _('Lithuania - Litas [LTL]')),
    ('LVL', _('Latvia - Lats [LVL]')),
    ('LYD', _('Libya - Dinar [LYD]')),
    ('MAD', _('Morocco - Dirham [MAD]')),
    ('MDL', _('Moldova - Leu [MDL]')),
    ('MGA', _('Madagascar - Ariary [MGA]')),
    ('MNT', _('Mongolia - Tugrik [MNT]')),
    ('MMK', _('Myanmar - Kyat [MMK]')),
    ('MOP', _('Macau - Pataca [MOP]')),
    ('MRO', _('Mauritania - Ouguiya [MRO]')),
    ('MUR', _('Mauritius - Rupee [MUR]')),
    ('MVR', _('Maldives - Rufiyaa [MVR]')),
    ('MWK', _('Malawi - Kwacha [MWK]')),
    ('MXN', _('Mexico - Peso [MXN]')),
    ('MYR', _('Malaysia - Ringgit [MYR]')),
    ('MZN', _('Mozambique - New Metical [MZN]')),
    ('NAD', _('Namibia - Dollar [NAD]')),
    ('NGN', _('Nigeria - Naira [NGN]')),
    ('NIO', _('Nicaragua - Cordoba Oro [NIO]')),
    ('NOK', _('Norway - Kroner [NOK]')),
    ('NPR', _('Nepal - Rupee [NPR]')),
    ('NZD', _('New Zealand - Dollar [NZD]')),
    ('OMR', _('Oman - Rial [OMR]')),
    ('PAB', _('Panama - Balboa [PAB]')),
    ('PEN', _('Peru - Nuevo Sol [PEN]')),
    ('PGK', _('Papua New Guinea - Kina [PGK]')),
    ('PHP', _('Philippines - Peso [PHP]')),
    ('PKR', _('Pakistan - Rupee [PKR]')),
    ('PLN', _('Poland - Zloty [PLN]')),
    ('PYG', _('Paraguay - Guarani [PYG]')),
    ('QAR', _('Qatar - Rial [QAR]')),
    ('RON', _('Romania - New Leu [RON]')),
    ('RUB', _('Russia - Rouble [RUB]')),
    ('RWF', _('Rwanda - Franc [RWF]')),
    ('SAR', _('Saudi Arabia - Riyal [SAR]')),
    ('SBD', _('Solomon Islands - Dollar [SBD]')),
    ('SCR', _('Seychelles - Rupee [SCR]')),
    ('SDG', _('Sudan - Pound [SDG]')),
    ('SEK', _('Sweden - Krona [SEK]')),
    ('SGD', _('Singapore - Dollar [SGD]')),
    ('SHP', _('St. Helena - Pound [SHP]')),
    ('SKK', _('Slovakia - Koruna [SKK]')),
    ('SLL', _('Sierra Leone - SLL [SLL]')),
    ('SOS', _('Somalia - Schilling [SOS]')),
    ('SRD', _('Suriname - Dollar [SRD]')),
    ('STD', _('Sao Tome - Dobra [STD]')),
    ('SVC', _('El Salvador - Colon [SVC]')),
    ('SYP', _('Syria - Pound [SYP]')),
    ('SZL', _('Swaziland - Lilangeni [SZL]')),
    ('THB', _('Thailand - Baht [THB]')),
    ('TJS', _('Tajikistan - Somoni [TJS]')),
    ('TMT', _('Turkmenistan - Manat [TMT]')),
    ('TND', _('Tunisia - Dinar [TND]')),
    ('TOP', _('Tonga - Pa\'anga [TOP]')),
    ('TRY', _('Turkey - Lira [TRY]')),
    ('TTD', _('Trinidad & Tobago - Dollar [TTD]')),
    ('TVD', _('Tuvalu - Dollar [TVD]')),
    ('TWD', _('Taiwan - Dollar [TWD]')),
    ('TZS', _('Tanzania - Schilling [TZS]')),
    ('UAH', _('Ukraine - Hryvnia [UAH]')),
    ('UGX', _('Uganda - Shilling [UGX]')),
    ('USD', _('United States - Dollar [USD]')),
    ('UYU', _('Uruguay - Peso [UYU]')),
    ('UZS', _('Uzbekistan - Som [UZS]')),
    ('VEF', _('Venezuela - Bolivar Fuerte [VEF]')),
    ('VND', _('Viet Nam - Dong [VND]')),
    ('VUV', _('Vanuatu - Vatu [VUV]')),
    ('WST', _('Samoa - Tala [WST]')),
    ('XAF', _('Financial Cooperation in Central Africa - Franc [XAF]')),
    ('XOF', _('Financial Community of Africa - Franc [XOF]')),
    ('YER', _('Yemen - Rial [YER]')),
    ('ZAR', _('South Africa - Rand [ZAR]')),
    ('ZMK', _('Zambia - Kwacha [ZMK]')),
    ('ZRN', _('Zaire - New Zaire [ZRN]')),
    ('ZWD', _('Zimbabwe - Dollar [ZWD]')),
]

# sort by country of currency, not iso
CURRENCIES = sorted(ALL_CURRENCIES, key=lambda currency: currency[1])
CURRENCIES = PRIORITY_CURRENCIES + CURRENCIES
SORTED_CURRENCIES = CURRENCIES

def isValidCurrency(field_data, all_data):
    if not field_data in [cur[0] for cur in CURRENCIES]:
        raise ValidationError, ugettext("Unsupported or invalid currency")

class CurrencyField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', CURRENCIES)
        super(CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


class Converter(object):
    """ A currency converter class """
    
    PROVIDERS = []

    def __init__(self, from_cur, to_cur):
        self.from_cur = from_cur
        self.to_cur = to_cur
        self.PROVIDERS = [
            ('Github', self.get_from_github),
            ('Google', self.get_from_google),
            ('Yahoo', self.get_from_yahoo),
        ]

    # try few time to get the rate. 
    # reason: some provider don't have all currencies, or there could be network or parsing error
    def get(self):
        tries = 0
        rate = 0
        provider = None
        while True:
            provider = self.get_next_provider(provider)
            rate = provider[1]()
            if rate:
                break;
            else:
                tries += 1
                if tries > len(self.PROVIDERS)+1:
                    break;
        return float(rate)
    
    # get a random provider from the list, try to avoid returning the previous provider
    def get_next_provider(self, prev):
        if len(self.PROVIDERS) > 1 and prev:
            while True:
                rand = random.randint(1, len(self.PROVIDERS))
                provider = self.PROVIDERS[rand-1]
                if provider != prev:
                    break;
        else:
            rand = random.randint(1, len(self.PROVIDERS))
            provider = self.PROVIDERS[rand-1]

        # print provider[0]
        return provider

    # get the exchange rate from google
    def get_from_google(self):
        rate = 0
        if self.from_cur != self.to_cur:
            fromto = "%s-%s" % (self.from_cur, self.to_cur)
            query = {
                'amount':   1, 
                'from':     self.from_cur,
                'to':       self.to_cur,
                'eq':       '%3D%3F' # the %3D%3F is equivalent to ?=
            }
            url = "http://www.google.com/ig/calculator?hl=en&q=%(amount)s%(from)s%(eq)s%(to)s" % query
            try:
                resp = urllib2.urlopen(url, timeout=4)
            except urllib2.URLError, e:
                pass
            else:
                try:
                    raw_data = resp.read()
                    raw_data = raw_data.replace('\xa0','')
                    j = self.sanitize_json(raw_data)
                    data = json.loads(j)
                    rate = Decimal(str(data['rhs'].split(" ")[0]))
                    if not rate:
                        rate = 0
                except:
                    pass
        
        return rate

    # get the exchange rate from yahoo
    def get_from_yahoo(self):
        rate = 0
        if self.from_cur != self.to_cur:
            fromto = "%s-%s" % (self.from_cur, self.to_cur)
            query = {
                'from': self.from_cur,
                'to':   self.to_cur,
            }
            url = "http://finance.yahoo.com/d/quotes.csv" + "?s=%(from)s%(to)s=X&f=sl1d1t1ba&e=.csv" % query
            try:
                resp = urllib2.urlopen(url, timeout=4)
            except urllib2.URLError, e:
                pass
            else:
                try:
                    raw_data = resp.read()
                    rate = Decimal(str(raw_data.split(',')[1]))
                    if not rate:
                        rate = 0
                except:
                    pass

        return rate

    # get the exchange rate from github
    def get_from_github(self):
        rate = 0
        if self.from_cur == self.to_cur:
            rate = 1
            return rate
        
        gitkey = 'key-github-rate-file'
        data = cache.get(gitkey)
        if not data:
            url = "https://raw.github.com/currencybot/open-exchange-rates/master/latest.json"
            try:
                resp = urllib2.urlopen(url, timeout=4)
            except urllib2.URLError, e:
                pass
            else:
                data = json.loads(resp.read())
                cache.set(gitkey, data, 24*60*60) # cache for a day

        if data:
            try:
                from2usd = data['rates'][self.from_cur]
                to2usd = data['rates'][self.to_cur]
                rate = Decimal(str(to2usd)) / Decimal (str(from2usd))
                if not rate:
                    rate = 0
            except:
                pass

        return rate

    def sanitize_json(self, raw_data):
        """ cleans up json that doesn't use double quotes for its keys """
        j = raw_data
        j = re.sub(r"{\s*(\w)", r'{"\1', j)
        j = re.sub(r",\s*(\w)", r',"\1', j)
        j = re.sub(r"(\w):", r'\1":', j)
        return j

# converts an amount in a given currency to it's USD then return a text like:
#  if xchange is success: "1569 [USD] ≈ 1000 [GBP]", else: "? [USD] ≈ 1000 [GBP]"
def get_to_usd_text(amount, from_cur):
    to_cur = "USD"
    if not amount:
        amount = 0
    if to_cur == from_cur:
        text = '%d [%s]' % (amount, from_cur)
    else:
        almost_sign = ' ≈ '.decode("utf-8")
        usd = get_currency_exchange(amount, from_cur, to_cur)
        if usd > 0:
            text = '%d [%s] %s %d [%s]' % (amount, from_cur, almost_sign, usd, to_cur)
        else:
            text = '%d [%s] %s ? [%s]' % (amount, from_cur, almost_sign, to_cur)
    return text

# converts an amount in a given currency to an amount in a desired curency
def get_currency_exchange(amount, from_cur, to_cur):
    # import pdb;pdb.set_trace()
    exchange = 0
    if not amount: 
        amount = 0
    if amount > 0:
        key = 'currency-1-%s-rate' % from_cur
        rate = cache.get(key)
        if not rate:
            rate = Converter(from_cur,to_cur).get()
            cache.set(key, rate, 24*60*60) # cache for a day
        exchange = amount * rate
        if exchange > 0 and exchange < 1:
            exchange = 1
        else:
            exchange = round(amount * rate, 0)
    return exchange
    


