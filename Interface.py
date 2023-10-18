import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from datetime import timedelta
from haversine import haversine

import funcoes_busca as busca

# Funções interface usuário
class UserInterface():
    def __init__(self):
        # Dicionário de cores para plotagem
        self.colour_dict = {'VERMELHA': '#FF0F00',
                       'VERDE': '#2EFF00',
                       'TURQUESA': '#00E0FF',
                       'SAFIRA': '#385f8f',
                       'RUBI': '#aa443f',
                       'PRATA': '#c0c0c0',
                       'LILAS': '#c8a2c8',
                       'JADE': '#00A86B',
                       'ESMERALDA': '#50c878',
                       'DIAMANTE': '#b9f2ff',
                       'CORAL': '#ff7f50',
                       'AZUL': '#4169e1',
                       'AMARELA': '#ffff00',
                       }

        # Variável -> velocidade média do metrô
        self.train_speed = 40

        self.linhas_id = []
        self.position_map = {}

        self.df_raw  = self.import_data()
        self.df_dict = self.position_df()

        self.G, self.df = self.create_graph()

    def get_input(self) -> list:
        input_user = []
        str_input = ''
        flag = 0
        msg = 'Insira a estação de origem:\nNão utilize acentos/caracteres especiais!\nInsira "Q" para sair do programa.'
        while flag == 0:
            str_input = input(msg).upper()
            flag = len(self.df.loc[self.df['source'] == str_input])
            if (flag == 0):
                msg = 'Estação inválida!\nInsira a estação de origem:\nNão utilize acentos/caracteres especiais!\nInsira "Q" para sair do programa.'

            if(str_input == "Q"):
                return None
        input_user.append(str_input)



        str_input = ''
        flag = 0
        msg = 'Insira a estação de destino:\nNão utilize acentos/caracteres especiais!\nInsira "Q" para sair do programa.'
        while flag == 0:
            str_input = input(msg).upper()
            # utilizada busca na coluna 'source' pois ela abrange todos os casos
            # ao contrário da coluna 'target'
            flag = len(self.df.loc[self.df['source'] == str_input])
            if (flag == 0):
                msg = 'Estação inválida!\nInsira a estação de destino:\nNão utilize acentos/caracteres especiais!\nInsira "Q" para sair do programa.'

            if (str_input == "Q"):
                return None
        input_user.append(str_input)


        return input_user




    def get_time(self, time):
        td_str = str(timedelta(seconds=time))
        x = td_str.split(':')
        print('\nDuração aproximada do trajeto', x[0], 'horas', x[1], 'minutos', x[2], 'segundos')


    def best_path(self, origin: str, destination: str, **kwargs):
        path_nodes = busca.a_estrela(grafo=self.G, no_origem = origin, no_destino= destination, df= self.df, peso="weight")
        path_lenght = busca.a_estrela_distancia(grafo=self.G, no_origem = origin, no_destino= destination, df= self.df, peso="weight")
        aux_troca = 0
        aux_index = 0

        est0 = path_nodes[0].split('-')
        est1 = path_nodes[1].split('-')

        if (est0[0] == est1[0]):
            aux_troca = -1
            aux_index = 1

        key_list = []
        for i in range(len(path_nodes) - 1):
            key = list(self.G.get_edge_data(path_nodes[i], path_nodes[i + 1]))
            key_list.append(key[0])

        aux_key = key_list[0]
        aux_flag = 0

        print('\n\nItinerário resumido:')
        print(f"{'Embarque na linha:': <25} {key_list[aux_index]: <20} {'Estação:': <10} {path_nodes[aux_index].split('-')[0] : <25}")

        for aux_index in range(len(path_nodes) - 1):
            if (aux_flag == 0) and (aux_key != key_list[aux_index]):
                print(f"{'Baldeação para linha:': <25} {key_list[aux_index]: <20} {'Estação:': <10} {path_nodes[aux_index].split('-')[0] : <25}")
                aux_flag = 1

            aux_key = key_list[aux_index]
            aux_flag = 0

        print(f"{'Desembarque na linha:': <25} {key_list[-1]: <20} {'Estação:': <10} {path_nodes[-1].split('-')[0] : <25}")

        # 30 segundos por parada (metro)
        # 3 minutos baldeação
        # 40km/h velocidade média metro

        eta_seconds = ((path_lenght * 3600) / self.train_speed) + ((len(path_nodes) - 1) * 30) + (aux_troca * 180)

        print(f"Distância estimada do trajeto: {path_lenght:.2f}km")
        self.get_time(int(eta_seconds))

        print("\nItinerário descriminado:")
        for bkp_index in range(len(path_nodes) - 1):
            if (path_nodes[bkp_index].split('-')[0] != path_nodes[bkp_index + 1].split('-')[0]):
                print(f"{'Linha:   ' + key_list[bkp_index]: <30} {'Estação:   ' + path_nodes[bkp_index].split('-')[0] : <40} -> {'Estação:   ' + path_nodes[bkp_index + 1].split('-')[0] : <30} ")
            else:
                print(f"\n{'MUDANÇA DE LINHAS NA ESTAÇÃO:   ' + path_nodes[bkp_index].split('-')[0] : <45} {'Linha de origem: ' + key_list[bkp_index - 1]: <25} ---> {'Linha destino: ' + key_list[bkp_index + 1]: <30}")

        key_unique = []
        for key in key_list:
            if key not in key_unique:
                key_unique.append(key)

        nodes_list = []
        for node in path_nodes:
            aux_str = node.split('-')[0]
            if aux_str not in nodes_list:
                nodes_list.append(aux_str)

        plt.figure(figsize=(kwargs.get('figsize', (15,10))))
        for elem in key_unique:
            key = elem.split('-')[-1]
            df_edges_aux = self.df_dict[key][["source", "target", "weight", "label_edge"]]
            df_edges = df_edges_aux.loc[
                (df_edges_aux['source'].isin(nodes_list)) & (df_edges_aux['target'].isin(nodes_list))]

            g_col = nx.from_pandas_edgelist(df_edges, source='source', target='target', edge_attr='weight')

            nx.draw_networkx(g_col,
                             pos=self.position_map,
                             with_labels=True,
                             node_size=kwargs.get('node_size', 500),
                             node_shape='8',
                             node_color=self.colour_dict.get(key),
                             style='dashed',
                             font_size=kwargs.get('font_size', 10))
        plt.savefig("itinerario.png")

    def menu_user(self, **kwargs):
        input_menu = self.get_input()
        if(input_menu == None):
            print("Programa abortado!")
            return None
        orig_input = self.df['label_source'].loc[self.df['source'] == input_menu[0]].iloc[0]
        dest_input = self.df['label_source'].loc[self.df['source'] == input_menu[1]].iloc[0]
        self.best_path(origin = orig_input, destination= dest_input, **kwargs)

    def _apply_haversine(self, data):
        df = data.copy()

        for i in range(len(df) - 1):
            coord_a = (df.pos_X[i], df.pos_Y[i])
            coord_b = (df.pos_X[i + 1], df.pos_Y[i + 1])
            df.loc[[i], ['weight']] = haversine(coord_a, coord_b)

        return df

    def import_data(self):
        # Tratamento inicial dos dados
        ## importar e fazer bkp dados
        df_raw = pd.read_csv('metroetrem_sp_comlinks.csv')

        ## Renomear colunas
        df_raw.rename(columns={"estacao_upp": "source", "link": "target", "nome_lin" : "name", "long" : "pos_X", "lat" : "pos_Y"}, inplace = True)

        ## Criar coluna de peso das arestas
        df_raw['weight'] = 0
        df_raw = self._apply_haversine(df_raw)

        ## Aplicar mapa de cores
        df_raw['colour'] = df_raw['name'].map(self.colour_dict)

        ## Inserir dados faltantes/Corrigir inconsistências
        df_raw.loc[len(df_raw.index)] = [4, 'AMARELA', -46.662161, -23.555044, 'PAULISTA', 'CONSOLACAO', 0.5, '#ffff00']
        df_raw.loc[len(df_raw.index)] = [2, 'VERDE', -46.660974, -23.557372, 'CONSOLACAO', 'PAULISTA', 0.5, '##2EFF00']
        df_raw.loc[df_raw['source'] == 'PALMEIRAS BARRA FUNDA', 'source'] = 'BARRA FUNDA'

        ## Criar labels para os nós
        ### Colunas 'Labels' são utilizadas no cálculo do trajeto
        ### Colunas 'source & target' são utilizadas na plotagem do trajeto
        df_raw['num_lin'] = df_raw['num_lin'].astype('str')
        df_raw['label_edge'] = df_raw['num_lin'] + '-' + df_raw['name']
        df_raw['label_source'] = df_raw['source'] + '-' + df_raw['num_lin']
        df_raw['label_target'] = df_raw['target'] + '-' + df_raw['num_lin']

        return df_raw

    def position_df(self):
        df_map = self.df_raw.copy()
        df_map.dropna(inplace=True)
        df_map.drop(df_map.loc[df_map['weight'] == 0].index, inplace=True)

        ## Criar dict de posição dos nodes
        aux_pos = df_map[["source", "pos_X", "pos_Y"]].copy()
        aux_pos.drop_duplicates(subset=['source'], keep='first', inplace=True)
        self.position_map = aux_pos.set_index('source').T.to_dict('list')

        ## Remover estações duplicadas
        df_map.drop(df_map.loc[df_map['source'] == df_map['target']].index, inplace=True)

        ## Criar dicionário que cada chave contenha os dados das estações de dada linha
        ## -> linha : dataframe da linha
        self.linhas_id = df_map.name.unique()
        dict_linhas = {elem: pd.DataFrame() for elem in self.linhas_id}

        ## Laço para plotar cada linha
        for key in dict_linhas.keys():
            dict_linhas[key] = df_map[:][df_map.name == key]

        self.df_map = df_map

        return dict_linhas


    def plot_network(self, plot_Whole = False, plot_line = None):
        # Manipulação dos dados para plotagem de cada linha separadamente

        if (plot_line in self.linhas_id):
            plt.figure(figsize = (20,5))
            title = 'Linha ' + self.df_map['num_lin'].loc[self.df_map['name'] == plot_line].iloc[0] + '-' + plot_line.capitalize()
            plt.title(title)
            df_edges = self.df_dict[plot_line][["source", "target", "weight"]]

            g_key = nx.from_pandas_edgelist(df_edges, source = 'source', target = 'target', edge_attr = 'weight')

            nx.draw_networkx(g_key,
                             pos = self.position_map,
                             with_labels = True,
                             node_size=75,
                             node_shape = '8',
                             node_color = self.colour_dict.get(plot_line),
                             style = 'dashed',
                             font_size = 7)

        if (plot_Whole and (plot_line not in self.linhas_id)):
            # Plotagem de malha inteira

            plt.figure(figsize=(30, 30))
            for key in self.df_dict:
                df_edges = self.df_dict[key][["source", "target", "weight"]]

                g_full = nx.from_pandas_edgelist(df_edges, source='source', target='target', edge_attr='weight')
                nx.draw_networkx(g_full,
                                 pos=self.position_map,
                                 with_labels=True,
                                 node_size=500,
                                 node_shape='8',
                                 node_color=self.colour_dict.get(key),
                                 style='dashed',
                                 font_size=10)

            plt.savefig("malha_full.png")

    def create_graph(self):
        ## Adicionar estações que fazem conexão com mais de uma linha (baldeação)

        ## Criar dataframe que recebe estações que tem baldeação
        columns_list = self.df_raw.columns.values.tolist()
        df_baldea = pd.DataFrame(columns=columns_list)

        ## Copiar as estações que são 'source'/origem de mais de um trajeto
        df_aux = self.df_raw[self.df_raw.duplicated('source')].sort_values('source')
        bald_list = df_aux['source'].unique()

        ## Preencher o dataframe com conexões entre a mesma estação mas entre diferentes linhas (e.g. Luz-Azul -> Luz-Coral)
        for elem in bald_list:
            slice_bald = self.df_raw.loc[self.df_raw['source'] == elem]
            for i in range(len(slice_bald)):
                for j in range(i + 1, len(slice_bald)):
                    df_baldea.loc[len(df_baldea.index)] = [slice_bald.iloc[i][0],
                                                           slice_bald.iloc[i][1],
                                                           slice_bald.iloc[i][2],
                                                           slice_bald.iloc[i][3],
                                                           slice_bald.iloc[i][4],
                                                           slice_bald.iloc[i][4],
                                                           (self.train_speed / 12),
                                                           slice_bald.iloc[i][7],
                                                           slice_bald.iloc[i][8],
                                                           slice_bald.iloc[i][9],
                                                           slice_bald.iloc[j][9]]

        ## Concatenar o dataframe original com o que contem as baldeações
        # display(df_baldea)
        df = pd.concat([self.df_raw, df_baldea]).sort_values('num_lin').reset_index(drop=True)
        df = df.reindex(index=df.index[::-1])

        df.dropna(inplace=True)
        df.drop(df.loc[df['weight'] == 0].index, inplace=True)

        # ## Criar um dict de posição dos nodes (source e target)
        # aux_pos_source = df[["label_source", "pos_X", "pos_Y"]].copy()
        # aux_pos_target = df[["label_target", "pos_X", "pos_Y"]].copy()
        #
        # aux_pos_source = aux_pos_source.drop_duplicates()
        # aux_pos_target = aux_pos_target.drop_duplicates()
        #
        # position_source = aux_pos_source.set_index('label_source').T.to_dict('list')
        # position_target = aux_pos_target.set_index('label_target').T.to_dict('list')
        #
        # position = position_source.copy()
        # position.update(position_target)

        ## Criar o grafo utilizado para cálculo de trajeto
        G_calc = nx.from_pandas_edgelist(df, source='label_source', target='label_target', edge_attr='weight',
                                         create_using=nx.MultiGraph, edge_key='label_edge')

        return G_calc, df