'''
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

Solution Notes:
For each vertex, generate and store all Hamming distances that are 0, 1 and 2 units apart. There
is only 1 code point that is 0 units apart (which is the same code as the vertex), 24C1 = 24
possible code points that are 1 unit apart and there are 24C2 = 276 possible code points that are
2 units apart for each vertex.

Now, put all vertexes along with their assigned code into a hash table. Use the code as the hash
table key, with the vertex number as the value - note that some codes are not unique (i.e. more
than one vertex can be associated with the same code), so each key in the hash table will have to
potentially hold more than one vertex - we will use this hash table later to look up the vertex
number(s) given the corresponding Hamming code in O(1) time.

Execute the following:
For each vertex (200K iterations):
  For each code that is 0 units apart from
  this vertex: (1 iteration - there is only one such code
  which is the same code as that of the vertex itself)
    - Use the code to index into the hash table and
      get the corresponding vertexes if they exist.
    - Add these 2 vertexes to a cluster.

For each vertex (200K iterations):
  For each code that is 1 unit apart from
  this vertex: (24 iterations)
    - Use the code to index into the hash table and
      get the corresponding vertexes if they exist.
    - Add these 2 vertexes to a cluster.

For each vertex (200K iterations):
  For each code that is 2 units apart from
  this vertex: (276 iterations)
    - Use the code to index into the hash table and
      get the corresponding vertexes if they exist.
    - Add these 2 vertexes to a cluster.

We are now left with clusters that are at least 3 units apart.
'''
import time


# Union-Find array data structure
class Union_Find(object):
    def __init__(self, n):
        self._parents = list(range(1, n + 1))
        self._cluster_sizes = [1] * n
        self._num_clusters = n

    def root(self, node):
        p = node
        while p != self._parents[p - 1]:
            p = self._parents[p - 1]
        return p

    # input: old root, new root, new cluster size
    # output: number of root updates
    def _combine(self, old_root, new_root, new_cluster_size):
        self._num_clusters -= 1
        for node_i, parent in enumerate(self._parents):
            if parent == old_root:
                self._parents[node_i] = new_root
            if parent == old_root or parent == new_root:
                self._cluster_sizes[node_i] = new_cluster_size

    def union(self, u, v):
        u_root = self.root(u)
        v_root = self.root(v)
        if u_root == v_root:
            return

        u_cluster_size = self._cluster_sizes[u - 1]
        v_cluster_size = self._cluster_sizes[v - 1]
        new_cluster_size = u_cluster_size + v_cluster_size

        if u_cluster_size >= v_cluster_size:
            self._combine(v_root, u_root, new_cluster_size)
        else:
            self._combine(u_root, v_root, new_cluster_size)

    def get_num_clusters(self):
        return self._num_clusters


# input: code (string) with n length
# output: an array containing "n choose 1" codes (strings) 1 unit away from input code
def generate_codes_1_unit_away(code):
    codes_1_unit_away = {}
    for i, num in enumerate(code):
        a = list(code)
        a[i] = '0' if num == '1' else '1'
        gen_code = ''.join(a)
        codes_1_unit_away[gen_code] = 1
    return list(codes_1_unit_away.keys())


# input: code (string) with n length
# output: an array containing "n choose 2" codes (strings) 2 units away from input code
def generate_codes_2_units_away(code):
    codes_2_units_away = {}
    for i, num in enumerate(code):
        a = list(code)
        a[i] = '0' if num == '1' else '1'
        changed_i = i
        mod_code = ''.join(a)
        for j, second_num in enumerate(mod_code):
            b = list(mod_code)
            if j != changed_i:
                b[j] = '0' if second_num == '1' else '1'
                gen_code = ''.join(b)
                codes_2_units_away[gen_code] = 1
    return list(codes_2_units_away.keys())


# input: filename
# output: hash with codes as keys and an array of vertices with that code as values
def populate_code_v_hash(filename):
    code_v_hash = {}
    with open(filename) as f_handle:
        f_handle.readline()
        for i, line in enumerate(f_handle):
            code = line.replace(' ', '').strip()
            code_v_hash.setdefault(code, []).append(i + 1)
    return code_v_hash


# input: filename, min_spacing "permissibl"e" for k clustering (as we have better, more defined
# clusters when spacing is maximized)
# output: max num of clusters possible to get at least desired min_spacing provided, i.e. so that
# all pairs of nodes with <=min_spacing-1 different bits fall into the same clusters
def max_k_clusters_for_min_spacing(filename, min_spacing):
    code_v_hash = populate_code_v_hash(filename)
    with open(filename) as f_handle:
        num_nodes = int(f_handle.readline().split()[0])

        union_find = Union_Find(num_nodes)
        hamming_distances = []
        for i, line in enumerate(f_handle):
            current_v = i + 1
            code = line.replace(' ', '').strip()
            codes_1_unit_away = generate_codes_1_unit_away(code)
            codes_2_units_away = generate_codes_2_units_away(code)
            hamming_distances = [code] + codes_1_unit_away + codes_2_units_away
            for h_code in hamming_distances:
                vertices_with_h_code = code_v_hash[h_code] if h_code in code_v_hash else []
                for v in vertices_with_h_code:
                    if v != current_v:
                        union_find.union(current_v, v)

    return union_find.get_num_clusters()


def main():
    start = time.time()
    # expected example result: 2
    result = max_k_clusters_for_min_spacing('max_k_clusters_for_min_spacing.txt', 3)
    print('result: ', result)
    print('elapsed time: ', time.time() - start)


main()
