import funcoes_busca as busca

import pandas as pd
import networkx as nx

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats as st

import time
import math
from haversine import haversine

class NewExperiment():
    def __init__(self, Graph, Dataframe):
        self.df_result = pd.DataFrame(columns=['path_AStar', 'len_AStar', 'dist_AStar', 'time_AStar',
                                               'path_dfs', 'len_dfs', 'dist_dfs', 'time_dfs',
                                               'path_djk', 'len_djk', 'dist_djk', 'time_djk',
                                               'path_hrt', 'len_hrt', 'dist_hrt', 'time_hrt',
                                               'path_gbf', 'len_gbf', 'dist_gbf', 'time_gbf'
                                               ])
        self.G = Graph
        self.df = Dataframe

    def heuristica(self, node_A, node_B, euclidiana=True):

        coord_a = (0, 0)
        coord_b = (0, 0)
        flag = 0

        try:
            ca_X = self.df.loc[(self.df['label_source'] == node_A)]['pos_X'].iloc[0]
            ca_Y = self.df.loc[(self.df['label_source'] == node_A)]['pos_Y'].iloc[0]
            coord_a = (ca_X, ca_Y)
        except IndexError:
            flag = 1

        try:
            cb_X = self.df.loc[(self.df['label_source'] == node_B)]['pos_X'].iloc[0]
            cb_Y = self.df.loc[(self.df['label_source'] == node_B)]['pos_Y'].iloc[0]
            coord_b = (cb_X, cb_Y)
        except IndexError:
            flag = -1

        if flag == 1: coord_a = coord_b
        if flag == -1: coord_b = coord_a

        if euclidiana:
            return math.dist(coord_a, coord_b)
        else:
            return haversine(coord_a, coord_b)

    def elapsed_time(self, n_rep=10):
        # Define source/target
        idx_s = np.random.randint(0, len(self.df))
        source = self.df.iloc[idx_s]['label_source']

        idx_t = np.random.randint(0, len(self.df))
        while (idx_s == idx_t): idx_t = np.random.randint(0, len(self.df))
        target = self.df.iloc[idx_t]['label_target']

        # A* time measure
        a_time = []
        for i in range(n_rep):
            start_time = time.perf_counter()
            path_AStar = list(busca.a_estrela(self.G, source, target, self.df))
            dist_AStar = busca.a_estrela_distancia(self.G, source, target, self.df)
            end_time = time.perf_counter()
            time_AStar = end_time - start_time
            a_time.append(time_AStar)

        # DFS time measure
        dfs_time = []
        for i in range(n_rep):
            start_time = time.perf_counter()
            path_dfs = list(busca.dfs_path(self.G, source, target))
            dist_dfs = busca.dfs_distancia(self.G, source, target)
            end_time = time.perf_counter()
            time_dfs = end_time - start_time
            dfs_time.append(time_dfs)

        # Heuristic time measure
        hrt_time = []
        for i in range(n_rep):
            start_time = time.perf_counter()
            path_hrt = list(nx.astar_path(self.G, source, target, heuristic=self.heuristica))
            dist_hrt = nx.astar_path_length(self.G, source, target, heuristic=self.heuristica)
            end_time = time.perf_counter()
            time_hrt = end_time - start_time
            hrt_time.append(time_hrt)

        # Dijkstra time measure
        djk_time = []
        for i in range(n_rep):
            start_time = time.perf_counter()
            path_djk = list(nx.dijkstra_path(self.G, source, target))
            dist_djk = nx.dijkstra_path_length(self.G, source, target)
            end_time = time.perf_counter()
            time_djk = end_time - start_time
            djk_time.append(time_djk)

        # Greedy Best first time measure
        gbf_time = []
        for i in range(n_rep):
            start_time = time.perf_counter()
            path_gbf = list(busca.best_first(self.G, source, target, self.df))
            dist_gbf = busca.best_first_distancia(self.G, source, target, self.df)
            end_time = time.perf_counter()
            time_gbf = end_time - start_time
            gbf_time.append(time_gbf)

        def avg(lista):
            return sum(lista) / len(lista)

        return [path_AStar, len(path_AStar), dist_AStar, avg(a_time),
                path_dfs, len(path_dfs), dist_dfs, avg(dfs_time),
                path_djk, len(path_djk), dist_djk, avg(djk_time),
                path_hrt, len(path_hrt), dist_hrt, avg(hrt_time),
                path_gbf, len(path_gbf), dist_gbf, avg(gbf_time),
                ]

    def run_experiment(self, n_exp, n_rep):
        start_time = time.time()
        for exp in range(n_exp):
            experiment = self.elapsed_time(n_rep)
            self.df_result.loc[len(self.df_result)] = experiment
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tempo total do experimento: {elapsed_time}s")
        self.df_result['delta_time'] = self.df_result['time_AStar'] - self.df_result['time_dfs']
        self.df_result['delta_len'] = self.df_result['len_AStar'] - self.df_result['len_dfs']
        self.df_result['delta_dist'] = self.df_result['dist_AStar'] - self.df_result['dist_dfs']

        self.df_result['delta_timeHeur'] = self.df_result['time_AStar'] - self.df_result['time_hrt']
        self.df_result['delta_lenHeur'] = self.df_result['len_AStar'] - self.df_result['len_hrt']
        self.df_result['delta_distHeur'] = self.df_result['dist_AStar'] - self.df_result['dist_hrt']

        self.df_result['delta_timeInfo'] = self.df_result['time_AStar'] - self.df_result['time_gbf']
        self.df_result['delta_lenInfo'] = self.df_result['len_AStar'] - self.df_result['len_gbf']
        self.df_result['delta_distInfo'] = self.df_result['dist_AStar'] - self.df_result['dist_gbf']

        self.df_result['delta_timeNao'] = self.df_result['time_dfs'] - self.df_result['time_djk']
        self.df_result['delta_lenNao'] = self.df_result['len_dfs'] - self.df_result['len_djk']
        self.df_result['delta_distNao'] = self.df_result['dist_dfs'] - self.df_result['dist_djk']


def plot_distrib(df, astar, depth, idx):
    x_label = ['Tamanho dos caminhos', 'Distância dos caminhos', 'Tempo de execução']
    title = ['Distribuição do tamanho dos caminhos', 'Distribuição da extensão dos caminhos',
             'Distribuição dos tempos de execução']
    delta = ['delta_len', 'delta_dist', 'delta_time']

    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    param_bins = 1
    ax = axes[0]
    ax.set_xlabel(x_label[idx])

    log_bool = False
    if (idx == 2):
        log_bool = True
        ax.set_xlabel(x_label[idx] + " (Escala log)")
        param_bins = 0.1

    sns.histplot(data=df, x=astar, binwidth=param_bins, color='red', label='A*', alpha=0.30, ax=ax, kde=True,
                 log_scale=log_bool)
    sns.histplot(data=df, x=depth, binwidth=param_bins, color='blue', label='Depth', alpha=0.85, ax=ax, kde=True,
                 log_scale=log_bool)

    ax.set_ylabel('Número de caminhos')
    ax.set_title(title[idx])

    _, p_value = st.mannwhitneyu(x=df[astar], y=df[depth])
    ax.bar([], [], label=f'p-value = {p_value:.2f}', fill=False)
    ax.legend()

    ax = axes[1]
    ax.hist(df[delta[idx]], bins=50)
    ax.set_xlabel('Diferença de ' + x_label[idx] + ' (A* $vs.$ Depth)')
    ax.set_ylabel('Número de caminhos')
    ax.set_title(f'Distribuição da Diferença de ' + x_label[idx])

    ax = axes[2]
    df_ord = df.sort_values(by=delta[idx]).reset_index().copy()
    ax.bar(df_ord.index, df_ord[delta[idx]], fill=False, ec='slategray')
    ax.set_xlabel(r'Elemento $X_i$')
    ax.set_ylabel('Diferença de ' + x_label[idx] + r' de $X_i$')
    ax.set_title(f'Distribuição da Diferença de ' + x_label[idx])

    plt.tight_layout()

    plt.show()

def plot_boxplots(df):
    variable_plot = [["len_AStar", "len_gbf", "len_djk", "len_dfs"],
                     ["dist_AStar", "dist_gbf", "dist_djk", "dist_dfs"],
                     ["time_AStar", "time_gbf", "time_djk", "time_dfs"]]
    labels1 = ["A*", "Best first", "Dijkstra", "Depth"]

    var_nao_inform = [["len_djk", "len_dfs", "delta_lenNao"],
                      ["dist_djk", "dist_dfs", "delta_distNao"],
                      ["time_djk", "time_dfs", "delta_timeNao"]]
    labels2 = ["Dijkstra", "Depth", r"${\Delta}$"]

    var_inform = [["len_AStar", "len_hrt", "len_gbf", "delta_lenHeur", "delta_lenInfo"],
                  ["dist_AStar", "dist_hrt", "dist_gbf", "delta_distHeur", "delta_distInfo"],
                  ["time_AStar", "time_hrt", "time_gbf", "delta_timeHeur", "delta_timeInfo"]]
    labels3 = ["A* Heur0", "A* Heur1", "Best first", r"${\Delta} Heurística $", r"${\Delta} A* GBF$"]

    var_comp = [["len_AStar", "len_dfs", "delta_len"],
                ["dist_AStar", "dist_dfs", "delta_dist"],
                ["time_AStar", "time_dfs", "delta_time"]]
    labels4 = ["A*", "Best Depth", r"${\Delta}$"]

    var_plot = [(variable_plot, labels1),
                (var_nao_inform, labels2),
                (var_inform, labels3),
                (var_comp, labels4)
                ]

    titles = ["Número de nós", "Distância (km)", "Tempo execução"]

    tick_fontsize = 17.5

    for i, plot in enumerate(var_plot):
        fig, axs = plt.subplots(1, 3, figsize=(30, 12))
        for var in range(3):
            ax = axs[var]
            sns.boxplot(data=df[var_plot[i][0][var]], orient='horizontal', ax=ax)
            ax.set_yticklabels(var_plot[i][1])

            ax.tick_params(axis='y', labelsize=tick_fontsize)
            ax.tick_params(axis='x', labelsize=tick_fontsize)
            ax.set_title(titles[var], fontsize=20)
            ax.grid(which='major', axis='y', linestyle='--', alpha=0.7)

        plt.show()