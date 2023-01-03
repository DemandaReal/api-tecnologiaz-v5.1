import pandas as pd
from api_versao_5.database.query_painel.update_rank import query_rank_painel, update_rankings


def atualizar_rank_paridades(conexao, cursor_db):
    query = query_rank_painel(conexao=conexao, cursor_db=cursor_db)
    tt_registros = len(query)
    lista_df_final = []
    
    if tt_registros >= 1:
        lista_rank_temp = [
            [], # ativo
            [], # operacao
            [], # resultado
            [], # padrao
        ]
        for i in range(tt_registros):
            lista_rank_temp[0].append(query[i][7])
            lista_rank_temp[1].append(query[i][6])
            lista_rank_temp[2].append(query[i][9])
            lista_rank_temp[3].append(query[i][8])
        
        df_rank_tmp = pd.DataFrame(list(zip(
            lista_rank_temp[0],
            lista_rank_temp[1],
            lista_rank_temp[2],
            lista_rank_temp[3],
        )), columns=["ativo", "operacao", "resultado", "padrao"])

        padroes = df_rank_tmp["padrao"].drop_duplicates(keep='last').values
        ativos = df_rank_tmp["ativo"].drop_duplicates(keep='last').values
        print(padroes, ativos)
        
        lista_df_temp = []
        for i in range(len(padroes)):
            df = df_rank_tmp[df_rank_tmp["padrao"]==padroes[i]]
            lista_df_temp.append(df)

            print(f"********************* Padrão: {padroes[i]}")
            print(df)

        try:
            for i in range(len(lista_df_temp)):
                dfT = lista_df_temp[i]
                listaDF = [[], [], [], [], [], [], []]
                for j in range(len(ativos)):

                    dfT2 = dfT[dfT["ativo"]==ativos[j]].tail(5)
                    tt_win  = len(dfT2[ dfT2["resultado"]== 2 ])
                    tt_loss = len(dfT2[ dfT2["resultado"]== 3 ])
                    tt_analisado = tt_win + tt_loss
                    perc_win = 0.0
                    perc_loss = 0.0
                    if tt_analisado >= 1:
                        if tt_win >= 1:
                            perc_win = tt_win / tt_analisado
                        if tt_loss >= 1:
                            perc_loss = tt_loss / tt_analisado

            
                    print(f">>>>>> win: {tt_win} | loss: {tt_loss} | tt: {tt_analisado} | ativo: {ativos[j]} | padrão: {padroes[i]}")
                    print(f">>>> perc_win: {perc_win} | perc_loss: {perc_loss}")
                    listaDF[0].append(ativos[j])
                    listaDF[1].append(tt_analisado)
                    listaDF[2].append(tt_win)
                    listaDF[3].append(tt_loss)
                    listaDF[4].append(perc_win)
                    listaDF[5].append(perc_loss)
                    listaDF[6].append(padroes[i])
                
                df = pd.DataFrame(list(zip(
                    listaDF[0],
                    listaDF[1],
                    listaDF[2],
                    listaDF[3],
                    listaDF[4],
                    listaDF[5],
                    listaDF[6],
                )), columns=["ativo", "tt analisado", "tt win", "tt loss", "perc win", "perc loss", "padrao"])
                lista_df_final.append(df)

            lista_final_ranking_ordenado = []
            for i in range(len(lista_df_final)):
                print("------------------------------------------------------------------------------")
                lista_final_ranking_ordenado.append(
                    lista_df_final[i].sort_values(
                        ["tt win", "perc win"],
                        ascending=False).head(3))
            
            update_rankings(lista_rankings=lista_final_ranking_ordenado, conexao=conexao, cursor_db=cursor_db)
        
        except Exception as e:
            print(e)

