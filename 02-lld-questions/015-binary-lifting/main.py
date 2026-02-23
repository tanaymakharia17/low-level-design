"""



import math
n = 10
upper_limit = math.ceil(math.log2(n)) + 2
lifting_matrix = [[0] * upper_limit for _ in range(n)]
parents = [-1, 0, 0, 0, 1, 1, 3, 4, 6, 6] # [0, 0, 1, 2, 3, 4, 5, 6, 7, 8]
for i in range(n):
    lifting_matrix[i][0] = i
    lifting_matrix[i][1] = parents[i]

print(lifting_matrix)

for i in range(2, upper_limit):
    for node in range(n):
        lifting_matrix[node][i] = lifting_matrix[lifting_matrix[node][i-1]][i-1]

print(lifting_matrix)

"""

import math
from typing import List

class BinaryLifting:
    def __init__(self, n: int, parents: List[int]):
        self.n = n
        self.parents = parents
        self.LOG = math.ceil(math.log2(n)) + 1
        self.lift = [[-1] * self.LOG for _ in range(n)]
        self.depth = [0] * n  # for LCA
        self._build()

    def _build(self):
        # Initialize parent and self-reference
        for i in range(self.n):
            self.lift[i][0] = self.parents[i]
        
        # Precompute depth
        def dfs(node, par):
            for child in range(self.n):
                if self.parents[child] == node and child != par:
                    self.depth[child] = self.depth[node] + 1
                    dfs(child, node)
        dfs(0, -1)  # assuming 0 is the root

        # Build full lifting table
        for j in range(1, self.LOG):
            for i in range(self.n):
                prev = self.lift[i][j - 1]
                if prev != -1:
                    self.lift[i][j] = self.lift[prev][j - 1]

    def get_kth_ancestor(self, node: int, k: int) -> int:
        for i in range(self.LOG):
            if k & (1 << i):
                node = self.lift[node][i]
                if node == -1:
                    break
        return node

    def lowest_common_ancestor(self, u: int, v: int) -> int:
        # Bring both to the same depth
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        u = self.get_kth_ancestor(u, diff)

        if u == v:
            return u

        for i in reversed(range(self.LOG)):
            if self.lift[u][i] != -1 and self.lift[u][i] != self.lift[v][i]:
                u = self.lift[u][i]
                v = self.lift[v][i]

        return self.lift[u][0]
    

import datetime
if __name__ == "__main__":
    start_time = datetime.datetime.now()
    n = 10
    parents = [-1, 0, 0, 0, 1, 1, 3, 4, 6, 6]
    bl = BinaryLifting(n, parents)

    print("k-th Ancestors:")
    print("3rd ancestor of 7:", bl.get_kth_ancestor(7, 3))  # Expected: 0
    print("2nd ancestor of 8:", bl.get_kth_ancestor(8, 2))  # Expected: 3

    for i in range(10000):
        print("\nLowest Common Ancestors:")
        print("LCA of 7 and 5:", bl.lowest_common_ancestor(7, 5))  # Expected: 1
        print("LCA of 8 and 9:", bl.lowest_common_ancestor(8, 9))  # Expected: 6
        print("LCA of 4 and 9:", bl.lowest_common_ancestor(4, 9))  # Expected: 0
    
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print("Total time:", elapsed_time.total_seconds())

