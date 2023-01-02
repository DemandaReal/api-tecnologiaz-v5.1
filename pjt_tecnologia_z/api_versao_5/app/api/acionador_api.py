import threading
from api_versao_5.valores_globais import var_globais
from api_versao_5.app.servidor_iq.client import ClientWSS
from api_versao_5.mensageria.canais import Mensageria
from api_versao_5.autenticacao.plataformaIQ.autenticar_iq import valida_credenciais

class AcionadoresAPI:
    def autenticacao_iqoption_api(username, password):
        auth = valida_credenciais(username, password)
        return auth

    def conectar_wss(ssid):
        if var_globais.CHECK_CONN == True:
            print("### Cliente já autenticado no websocket ###")
        else:
            var_globais.OBJ_WSS = ClientWSS(var_globais.URL_WSS)
            var_globais.THREDING_WSS = threading.Thread(target=var_globais.OBJ_WSS.wss.run_forever).start()
            while True:
                if var_globais.CHECK_CONN == True:
                    break
            Mensageria.enviar_ssid(ssid=ssid)
            while True:
                if var_globais.CHECK_STATUS_MSG == True and var_globais.ID_USUARIO_PRACTICE != 0:
                    break
            
            print(f"--> status conexão Websocket: {var_globais.CHECK_CONN}")
            print(f"--> status mensageria Websocket: {var_globais.CHECK_STATUS_MSG}")
            Mensageria.enviar_msg_config_usuario()
            return
   
    