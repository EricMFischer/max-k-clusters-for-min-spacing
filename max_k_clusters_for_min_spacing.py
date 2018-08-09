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


# Vertex class for undirected graphs
class Vertex():
    def __init__(self, key):
        self._key = key
        self._nbrs = {}

    def __str__(self):
        return '{' + "'key': {}, 'nbrs': {}".format(
            self._key,
            self._nbrs
        ) + '}'

    def add_nbr(self, nbr_key, weight=1):
        if (nbr_key):
            self._nbrs[nbr_key] = weight

    def has_nbr(self, nbr_key):
        return nbr_key in self._nbrs

    def get_nbr_keys(self):
        return self._nbrs.keys()

    def get_nbr_values(self):
        return self._nbrs.values()

    def remove_nbr(self, nbr_key):
        if nbr_key in self._nbrs:
            del self._nbrs[nbr_key]

    def get_e(self, nbr_key):
        if nbr_key in self._nbrs:
            return self._nbrs[nbr_key]


# Undirected graph class
class Graph():
    def __init__(self):
        self._vertices = {}

    # 'x in graph' will use this containment logic
    def __contains__(self, key):
        return key in self._vertices

    # 'for x in graph' will use this iter() definition, where x is a vertex in an array
    def __iter__(self):
        return iter(self._vertices.values())

    def __str__(self):
        output = '\n{\n'
        vertices = self._vertices.values()
        for v in vertices:
            graph_key = "{}".format(v._key)
            v_str = "\n   'key': {}, \n   'nbrs': {}".format(
                v._key,
                v._nbrs
            )
            output += ' ' + graph_key + ': {' + v_str + '\n },\n'
        return output + '}'

    def add_v(self, v):
        if v:
            self._vertices[v._key] = v
        return self

    def get_v(self, key):
        try:
            return self._vertices[key]
        except KeyError:
            return None

    def get_v_keys(self):
        return list(self._vertices.keys())

    # removes vertex as neighbor from all its neighbors, then deletes vertex
    def remove_v(self, key):
        if key in self._vertices:
            nbr_keys = self._vertices[key].get_nbr_keys()
            for nbr_key in nbr_keys:
                self.remove_e(nbr_key, key)
            del self._vertices[key]

    def add_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        self._vertices[from_key].add_nbr(to_key, weight)
        self._vertices[to_key].add_nbr(from_key, weight)

    def get_e(self, from_key, to_key):
        if from_key and to_key in self._vertices:
            return self.get_v(from_key).get_e(to_key)

    # adds the weight for an edge if it exists already, with a default of 1
    def increase_e(self, from_key, to_key, weight=1):
        if from_key not in self._vertices:
            self.add_v(Vertex(from_key))
        if to_key not in self._vertices:
            self.add_v(Vertex(to_key))

        weight_u_v = self.get_v(from_key).get_e(to_key)
        new_weight_u_v = weight_u_v + weight if weight_u_v else weight

        weight_v_u = self.get_v(to_key).get_e(from_key)
        new_weight_v_u = weight_v_u + weight if weight_v_u else weight

        self._vertices[from_key].add_nbr(to_key, new_weight_u_v)
        self._vertices[to_key].add_nbr(from_key, new_weight_v_u)

    def has_e(self, from_key, to_key):
        if from_key in self._vertices:
            return self._vertices[from_key].has_nbr(to_key)

    def remove_e(self, from_key, to_key):
        if from_key in self._vertices:
            self._vertices[from_key].remove_nbr(to_key)
        if to_key in self._vertices:
            self._vertices[to_key].remove_nbr(from_key)

    def for_each_v(self, cb):
        for v in self._vertices:
            cb(v)


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
    codes_1_unit_away = []
    for i, num in enumerate(code):
        array = list(code)
        array[i] = '0' if num == '1' else '1'
        gen_code = ''.join(array)
        codes_1_unit_away.append(gen_code)
    return codes_1_unit_away


# input: code (string) with n length
# output: an array containing "n choose 2" codes (strings) 2 units away from input code
def generate_codes_2_units_away(code):
    codes_2_units_away = []
    for i, num in enumerate(code):
        array = list(code)
        # array[i] = '0' if num == '1' else '1'
        gen_code = ''.join(array)
        codes_2_units_away.append(gen_code)
    return codes_2_units_away


# input: filename, min_spacing "permissibl"e" for k clustering (as we have better, more defined
# clusters when spacing is maximized)
# output: max num of clusters possible to get at least desired min_spacing provided, i.e. so that
# all pairs of nodes with <=min_spacing-1 different bits fall into the same clusters
def max_k_clusters_for_min_spacing(filename, min_spacing):
    with open(filename) as f_handle:
        info = f_handle.readline().split()
        num_nodes = int(info[0])
        bits_per_node = int(info[1])
        print('num of nodes, bits per node: ', num_nodes, bits_per_node)

        code_v_hash = {}
        union_find = Union_Find(num_nodes)
        T = Graph()
        for index, line in enumerate(f_handle):
            code = line.replace(' ', '').strip()
            code_v_hash[code] = index + 1

            codes_1_unit_away = generate_codes_1_unit_away(code)
            for nbr_code in codes_1_unit_away:
                T.add_e(code, nbr_code)
                union_find.union(code, nbr_code)

            codes_2_units_away = generate_codes_2_units_away(code)
            for nbr_2_code in codes_2_units_away:
                T.add_e(code, nbr_2_code)
                union_find.union(code, nbr_2_code)

        print('code_v_hash: ', code_v_hash)
    return None


def main():
    start = time.time()
    # expected example result: 2
    result = max_k_clusters_for_min_spacing('max_k_clusters_for_min_spacing_ex.txt', 3)
    print('result: ', result)
    print('elapsed time: ', time.time() - start)


main()
