## Plotting trajectories as a directed graph

### General idea: represent KTH campus mobility data as a directed graph and privatize queries related to graph statistics such as edge and node count. For that, test node differential privacy code developed by Github user anusii (https://github.com/anusii/graph-dp).

1. Library used for plotting and graph making -> networkx (https://networkx.org/) and matplotlib (https://matplotlib.org/)
2. Nodes: AP names
3. Edges: 1 edge represents 1 user going who has traveled once between the nodes (direction counts in representation, but has to be erased for node_dp code)
4. One graph represents data between midnight and noon of one day in KTH dataset
5. Feed undirected KTH graph into node dp code 
6. Tried different number of clients (trajectories) privatized: 20, 100, 240. The results are in results jupyter notebook. 
7. The code privatizing the full number of trajectories takes a challenging amount of time to run.

**Further work**: reconstructing data based on privatized query answers for release.

### Utilizing graph representation for ngram efficiency analysis

1. APs are represented by integer indeces
2. Each trajectory is a sequence of integers (indeces)
3. Two directed graphs are plotted: one for original KTH morning dataset and one for the noisy dataset processed by the ngram approach code.
4. Each trajectory has a different color edges.
5. Differences between original and noisy trajectories can be seen clearly. 

Notebooks:
  * ***graph_repr.ipynb***: networkx representation of different segments of KTH data
  * ***node_dp_efforts.ipynb***: usage of node dp algorithm to process KTH data represented as undirected graphs
  * ***node_dp_results.md***: a table of results of node dp algorithm in correlation to data sample size (20, 100, and 240 trajectories)
  * ***ngram_visualize.ipynb***: visualization of ngram algorithm results as directed trajectory graph 
