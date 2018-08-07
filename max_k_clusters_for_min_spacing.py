'''
Here we have a greedy clustering algorithm for computing a max-spacing k-clustering. The
accompanying file describes a distance function (equivalently, a complete graph with edge costs).
It has the following format:

[number_of_nodes]
[edge 1 node 1] [edge 1 node 2] [edge 1 cost]
[edge 2 node 1] [edge 2 node 2] [edge 2 cost]
...

There is one edge (i,j) for each choice of 1 <= i < j <= n, where n is the number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance between nodes
1 and 3 (equivalently, the cost of the edge (1,3)) is 5250. We can assume that distances are
positive but should NOT assume that they are distinct.

We'll run the clustering algorithm on this data set, where the target number k of clusters is set
to 4. What is the maximum spacing of a 4-clustering?
'''
import time


# input: filename, min_spacing permissible for k clustering (as we have more defined clusters
# when spacing is maximized)
# output: max num of clusters needed to get at least desired min_spacing provided, i.e. so that all
# two nodes with <=(min_spacing - 1) different bits fall into the same clusters
def max_k_clusters_for_min_spacing(filename, min_spacing):
    return None


def main():
    start = time.time()
    result = max_k_clusters_for_min_spacing('max_k_clusters_for_min_spacing.txt', 3)
    print('result: ', result)
    print('elapsed time: ', time.time() - start)


main()
