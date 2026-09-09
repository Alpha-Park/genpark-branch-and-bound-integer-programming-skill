"""
Autonomous Agent Branch and Bound Mixed-Integer Linear Programming (MILP) Solver Skill
Pure Python Standard Library implementation.
"""
import math
from typing import List, Dict, Any, Set
from client_simplex import SimplexSolver

class BranchAndBoundMILP:
    """
    Branch and Bound solver for Mixed Integer Linear Programming (MILP).
    Solves: Maximize c^T x s.t. A x <= b, x >= 0, x_j in Z for j in integer_indices.
    """
    def __init__(self, c: List[float], A: List[List[float]], b: List[float], 
                 integer_indices: List[int], maximize: bool = True):
        self.c = [float(x) for x in c]
        self.A = [[float(v) for v in r] for r in A]
        self.b = [float(x) for x in b]
        self.integer_indices = set(integer_indices)
        self.maximize = maximize
        self.best_obj = float("-inf") if maximize else float("inf")
        self.best_sol = None
        self.nodes_explored = 0

    def solve(self, max_nodes: int = 1000) -> Dict[str, Any]:
        init_types = ["<="] * len(self.b)
        stack = [(self.A, self.b, init_types)]

        while stack and self.nodes_explored < max_nodes:
            self.nodes_explored += 1
            A_k, b_k, types_k = stack.pop()

            lp = SimplexSolver(self.c, A_k, b_k, types_k, maximize=self.maximize)
            res = lp.solve()

            if res["status"] != "optimal":
                continue

            obj_val = res["optimal_value"]
            sol = res["solution"]

            if self.maximize and obj_val <= self.best_obj + 1e-6:
                continue
            if not self.maximize and obj_val >= self.best_obj - 1e-6:
                continue

            fractional_var = None
            max_frac_dist = 0.0

            for j in self.integer_indices:
                val = sol[j]
                nearest = round(val)
                dist = abs(val - nearest)
                if dist > 1e-5:
                    if dist > max_frac_dist:
                        max_frac_dist = dist
                        fractional_var = (j, val)

            if fractional_var is None:
                self.best_obj = obj_val
                self.best_sol = sol
            else:
                j, val = fractional_var
                floor_val = math.floor(val)
                ceil_val = math.ceil(val)

                new_row1 = [0.0] * len(self.c)
                new_row1[j] = 1.0
                branch1_A = [list(r) for r in A_k] + [new_row1]
                branch1_b = list(b_k) + [float(floor_val)]
                branch1_types = list(types_k) + ["<="]

                new_row2 = [0.0] * len(self.c)
                new_row2[j] = 1.0
                branch2_A = [list(r) for r in A_k] + [new_row2]
                branch2_b = list(b_k) + [float(ceil_val)]
                branch2_types = list(types_k) + [">="]

                stack.append((branch2_A, branch2_b, branch2_types))
                stack.append((branch1_A, branch1_b, branch1_types))

        return {
            "status": "optimal" if self.best_sol is not None else "infeasible",
            "optimal_value": round(self.best_obj, 6) if self.best_sol else None,
            "solution": [round(x, 6) for x in self.best_sol] if self.best_sol else None,
            "nodes_explored": self.nodes_explored
        }
