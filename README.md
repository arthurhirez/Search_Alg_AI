The repository showcases the results of a study comparing different search algorithms (informed and uninformed) in the context of an application that suggests the best path to be taken in the subway network of the city of São Paulo - SP, Brazil.

# METHODOLOGY

In the first step, the authors implement the informed search algorithms A* and Best-First, as well as the uninformed Depth First Search. Additionally, data preprocessing is performed to model the problem as a graph using the data structure implemented in the NetworkX library.

The paper presents two distinct studies. The first study aims to draw conclusions about the efficiency of different variations of search algorithms. The implemented algorithms, as well as the Dijkstra algorithm from the NetworkX library, are used for comparison. Two types of heuristics for the A* algorithm are also compared: straight-line distance and Haversine distance, which considers the curvature of the earth based on latitude and longitude.

The second study is related to the analysis of the execution time and properties of the paths found by the implemented search algorithms, specifically Depth First Search (uninformed) and A* (informed) with the Haversine distance heuristic.

To conduct the mentioned studies, an experiment generates 2500 random origin/destination points. For each algorithm, a path between nodes is sought, with the variables of interest being the path's size, total distance, and execution time. To minimize hardware and software interference in time measurements, each execution time is measured five times, and the results are presented as the average of these times.

# RESULTS AND DISCUSSIONS

Firstly, the study of search algorithms is presented, providing a brief description of the implemented search algorithms, whose execution times, and path properties are analyzed.

Then, a comparative study between informed and uninformed search is conducted, with a brief description of the nuances of each case. Additionally, the Mann-Whitney test is used to determine if there is statistical difference between the obtained results.

As mentioned, the time measurement results are presented as the average of five time measurements for both cases.

## 3.1 STUDY OF SEARCH ALGORITHMS

This section compiles comparative results between informed and uninformed search and comparative results of different algorithms for each type of search.

In Figure 1, multiple search algorithms, both informed and uninformed, are compared, including implementations by the authors, except for the Dijkstra algorithm.

![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/b99ca385-a724-4196-a4f5-2a4b149f5203)

In the first case analyzed, it is evident that informed search algorithms (A* and Best-First) behave similarly regarding path properties (number of nodes and total distance). However, as expected, the A* algorithm always finds optimal paths, presenting lower values for the number of nodes and total distance.

Regarding execution time, the A* algorithm showed the worst results, which can be partially attributed to the lack of optimization in the implementation. Nevertheless, this is an expected result since finding an optimal solution comes with an associated cost.

Finally, the Depth-First search algorithm returned paths with greater distances and number of nodes but with low execution time compared to informed search cases.

The comparison between the two uninformed search algorithms (Depth-First and Dijkstra) is performed in Figure 2. It shows that the Dijkstra algorithm demonstrates better results in finding shorter paths, with cases where the difference reaches almost 60 nodes between paths found by each algorithm.

![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/264a64a4-97d7-4183-894c-0784a0e1e08c)

In terms of distance, Depth-First search had paths with a median distance close to 60 km, compared to a median of approximately 25 km for Dijkstra search cases. For both cases, the execution time was similar, making the Dijkstra algorithm the better choice.

In the comparison between the informed search algorithms (Figure 3), A* and Best-First are considered. For A*, two heuristics are compared: the first (Heur0) uses the Haversine distance, considering the curvature of the earth based on latitude and longitude, and the second (Heur1) uses straight-line distance between stations.

![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/71cfd8c9-7a30-43ef-87ce-943130d1f4f4)

It is evident that, in terms of path size and total distance, the results are similar for the two chosen heuristics and between algorithms. Observing the execution times, the heuristic using Haversine distance achieved better results when compared to the Euclidean distance heuristic.

Therefore, the choice of a suitable heuristic, in addition to facilitating the convergence of the optimal path solution more quickly, also has a considerable influence on the algorithm's execution time.

Comparing A* and Best-First algorithms, it is noted that the latter had a shorter execution time, but it should be emphasized that it did not always present the optimal path, as evidenced by observing larger path sizes and distances compared to those obtained using the A* algorithm.

## 3.2 COMPARISON BETWEEN INFORMED AND UNINFORMED SEARCH

In this section, a comparison is made between the two types of search, using the informed search algorithm A* and the uninformed Depth-First search algorithm.

The size and distance of paths, as well as the execution time, are analyzed. For each analysis, the p-value of the Mann-Whitney test is calculated, indicating whether there is statistical difference between the results. The null hypothesis is that the results are derived from the same distribution.

The distributions of observations are shown in the leftmost plot in the analyses below. The middle and right images are derived from subtracting the results obtained by the Depth-First search algorithm from those obtained by the A* algorithm.


In Figure 4, results related to path sizes are presented. The calculated p-value is rounded to 0, indicating strong evidence of statistical difference between the results. The majority of cases show that A* led to smaller paths, as confirmed by the image on the right, which shows that the majority of the difference between paths is negative.

![distribuiçãoVAR_0](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/d0b253d1-9dd6-4d9b-bdc1-bec25428c260)


A similar analysis is conducted for the total distance of paths, with the results shown in Figure 5. The calculated p-value is again approximated as 0, showing a difference between the results obtained by the two types of search.

![distribuiçãoVAR_1](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/8109cd77-18bd-4d39-b271-ec3644854cfc)

Observing the central and right figures, it is evident that paths obtained by the A* algorithm are always optimal, as there was not a single case where the uninformed search returned a shorter path. It is noteworthy that the shortest path is not always the one with fewer nodes, so these results do not invalidate the results of the total path size comparison.

Results related to execution time are presented in Figure 6, where a logarithmic scale is used for the x-axis. Similar to previous cases, the Mann-Whitney test results indicate strong evidence of statistical difference between informed and uninformed search cases.

![distribuiçãoVAR_2](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/dab56584-84b8-41f9-b2a9-bc0a89ab615c)

Observing the central and right figures, it is clear that the cost of finding an optimal path is always reflected in the execution time, with the A* algorithm being consistently more costly—differing by 2 orders of magnitude, as shown in the leftmost image.

In Table 1, the results of the comparison between the two types of search are compiled. Considering the proportions (A* / Depth) of the values found, paths between two nodes found by A* resulted in values around 68% and 60% smaller than the values obtained from Depth-First search for the number of nodes and distance, respectively, but with an average execution time 242 times longer.

Table 1: Comparative Results – Informed vs Uninformed Search

|             | Tamanho | Distância | Proporções (A* / Depth) |
|-------------|---------|-----------|--------------------------|
| **Média**   | 0.678   | 0.603     | 242.572                  |
| **Mínimo**  | 0.052   | 0.016     | 0.885                    |
| **Máximo**  | 1.800   | 1.000     | 1878.485                 |
| **Desvio Padrão** | 0.295 | 0.290 | 228.103                  |

| **Diferenças em valores absolutos (A* - Depth)** | Média | Máxima   |
|--------------------------------------------------|-------|----------|
| **Tamanho**                                      | 12.321| 59.000   |
| **Distância**                                    | 17.813| 121.971  |
| **Proporção**                                    | 0.066 | 0.304    |


In the extreme case, the A* algorithm obtained a path of the same distance as the Depth-First search algorithm, presenting cases with up to 1.8 times the number of nodes found by the Depth-First search. This result illustrates that the best path is not always the one that passes through the fewest nodes. Regarding execution time, in the worst case, A* took 1878 times longer than the Depth-First search algorithm.


![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/9fd3306e-9d17-4279-8de8-0e8ddc944971)

In terms of the proportion of execution time, depicted in the rightmost image, it is observed that 75% of cases using A* take up to 375 times more time than Depth-First search, with 50% of the results taking up to 171 times more time, and an average time spent 242 times higher.


# 3.3 Subway Route Implementation

After completing the study on search algorithms, the program for route calculation is implemented. The graph structure implemented in the NetworkX library is utilized, with the A* search. The results of the obtained route are displayed to the user in Figure 8, and the detailed itinerary is shown to the user in Figure 9.

![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/5d1d24c2-2e44-499e-afff-3e56936d8397)

Validation was conducted by comparing the program's results with those obtained using the route calculated by Google Maps. In a significant portion of the results, a very similar travel time was returned, and in almost all checks, the same route was obtained.

![image](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/9546a154-dd85-4305-a99e-fe826e157579)

![malha_full](https://github.com/arthurhirez/BUSCA_IA/assets/109704516/d12fb295-6226-4644-b8d1-f62ba477be27)



# Conclusions

With widespread applications, the task of search is present in almost any computational implementation, emphasizing the importance of studying and understanding the topic. Thus, this study aims to evaluate variations in search implementation, using both informed and uninformed search variations, as well as to elucidate the impact of adopting different heuristics in the case of the A* algorithm.

In both presented studies, the results are derived from an experiment with 2500 random paths, with timing measured 5 times, using the average of the measurements to provide robustness to the study.

## Study 1 - Comparison of Various Algorithms

- **Informed Search:** Informed search algorithms obtain shorter paths, resulting in optimal solutions. However, the average execution times reflect the cost of finding an optimal solution.

- **Uninformed Search:** The algorithm implemented in the NetworkX library returns shorter paths compared to the authors' depth-first search implementation. This could be due to implementation optimization and the intrinsic characteristic of depth-first search not always finding the shortest path.

- **Informed Search Heuristics:** The study compares two distance calculation heuristics, Haversine and Euclidean, with diverging results only in execution time. The appropriate choice of the heuristic leads to optimized convergence of the optimal solution. The Best-First algorithm shows positive results with lower execution times than A* implementations but does not always return optimal solutions.

## Study 2 - A* vs. Depth-First Search Comparison

- **Informed vs. Uninformed:** Informed search leads to optimal results with paths as or more efficient in all cases. However, the execution time difference of up to two orders of magnitude indicates that the pursuit of optimal solutions in complex problems can be impractical, making knowledge of alternatives, like uninformed searches, extremely relevant.

- **A* Performance:** Paths found by A* are always optimal, even when passing through more nodes, resulting in shorter distances. While the execution time is significantly higher in A*, this difference is not noticeable to the user, justifying the adoption of this algorithm as the search engine.
