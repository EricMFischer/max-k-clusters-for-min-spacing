## Synopsis
In this question the task is again to run the clustering algorithm from lecture, but on a MUCH
bigger graph. So big, in fact, that the distances (i.e., edge costs) are only defined implicitly,
rather than being provided as an explicit list.

The format is:
[# of nodes] [# of bits for each node's label]

[first bit of node 1] ... [last bit of node 1]

[first bit of node 2] ... [last bit of node 2]

...

For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes
the 24 bits associated with node #2.

The distance between two nodes uu and vv in this problem is defined as the Hamming distance--- the
number of differing bits --- between the two nodes' labels. For example, the Hamming distance
between the 24-bit label of node #2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0
1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a k-clustering with spacing
at least 3? That is, how many clusters are needed to ensure that no pair of nodes with all but 2
bits in common get split into different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably can't write it out
explicitly, let alone sort the edges by cost. So you will have to be a little creative to complete
this part of the question. For example, is there some way you can identify the smallest distances
without explicitly looking at every pair of nodes?

## Motivation

This algorithm further builds one's intuition on k clusters and spacing. Here, we are trying to find the maximum number of k clusters given a desired minimum spacing between the nodes. For example, we might want the maximum number of k clusters possible given that we maintain a desired minimum spacing of 3 between the nodes (i.e. all pairs of nodes with spacing 2 or less fall within the same clusters). This problem is practical, as we always want to maximize spacing between nodes in different clusters, as we'd define our algorithm as performing poorly if two relatively similar nodes with a small spacing ended up in different clusters, or categorizations of our dataset. 
## Acknowledgements

This algorithm is part of the Stanford University Algorithms 4-Course Specialization on Coursera, instructed by Tim Roughgarden.
