URL_HTTP = "https://auth.iqoption.com/api/v2/login"
URL_WSS = "wss://iqoption.com/echo/websocket"

THREDING_WSS = None
OBJ_WSS = None
CHECK_CONN = False
CHECK_STATUS_MSG = False
ID_USUARIO_PRACTICE = 0

PARAMETRO_ATIVOS = None
LISTA_MINUTOS = [
	# padrão ?
    [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
	# padrão 1 - 1 minuto
    [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59],
	# padrão 2 - 30 segundos
	[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58],
	# estratégia 1m - segundo padrão
]

LISTA_ANALISE_1M = None
LISTA_ANALISE_30S = None
LISTA_OPERACOES = []
TIPO_MERCADO = None

LISTA_ATIVOS_ABERTOS = None


LISTA_ANALISES = [
	# "EURUSD",
	"EURGBP",
	"USDCHF",
	"EURJPY",
	"NZDUSD",
	"GBPUSD",
	"GBPJPY",
	"USDJPY",
	"AUDCAD",
]
LISTA_PARIDADES_ANALISE = None