"""
Autonomous Agent Two-Phase Simplex Linear Programming Solver Skill
Pure Python Standard Library implementation.
"""
from typing import List, Dict, Any, Optional

class SimplexSolver:
    """
    Two-Phase Simplex Algorithm for Linear Programming.
    Solves: Maximize c^T x subject to A x (<=, >=, ==) b and x >= 0.
    """
    def __init__(self, c: List[float], A: List[List[float]], b: List[float], 
                 constraints_types: Optional[List[str]] = None, maximize: bool = True):
        self.c = [float(x) for x in c]
        self.A = [[float(v) for v in row] for row in A]
        self.b = [float(x) for x in b]
        self.constraints_types = constraints_types or ["<="] * len(b)
        self.maximize = maximize
        self.m = len(b)
        self.n = len(c)

    def solve(self) -> Dict[str, Any]:
        m, n = self.m, self.n
        A_norm = [list(r) for r in self.A]
        b_norm = list(self.b)
        c_norm = [x if self.maximize else -x for x in self.c]
        types_norm = list(self.constraints_types)

        for i in range(m):
            if b_norm[i] < -1e-9:
                b_norm[i] = -b_norm[i]
                A_norm[i] = [-val for val in A_norm[i]]
                if types_norm[i] == "<=":
                    types_norm[i] = ">="
                elif types_norm[i] == ">=":
                    types_norm[i] = "<="

        slack_surplus = []
        artificial = []
        for i, t in enumerate(types_norm):
            if t == "<=":
                slack_surplus.append((i, 1.0))
            elif t == ">=":
                slack_surplus.append((i, -1.0))
                artificial.append(i)
            elif t == "==":
                artificial.append(i)
            else:
                raise ValueError(f"Unknown constraint type: {t}")

        num_slack = len(slack_surplus)
        num_art = len(artificial)
        total_vars = n + num_slack + num_art

        tab = [[0.0] * (total_vars + 1) for _ in range(m + 2)]
        basis = [-1] * m

        for i in range(m):
            for j in range(n):
                tab[i + 2][j] = A_norm[i][j]
            tab[i + 2][-1] = b_norm[i]

        for s_idx, (r, sign) in enumerate(slack_surplus):
            col = n + s_idx
            tab[r + 2][col] = sign
            if sign == 1.0:
                basis[r] = col

        for a_idx, r in enumerate(artificial):
            col = n + num_slack + a_idx
            tab[r + 2][col] = 1.0
            basis[r] = col

        for j in range(n):
            tab[1][j] = -c_norm[j]

        if num_art > 0:
            for a_idx, r in enumerate(artificial):
                col = n + num_slack + a_idx
                tab[0][col] = 1.0
            for a_idx, r in enumerate(artificial):
                for c_col in range(total_vars + 1):
                    tab[0][c_col] -= tab[r + 2][c_col]

            status = self._pivot_phase(tab, basis, obj_row=0, active_cols=total_vars)
            if status != "optimal" or abs(tab[0][-1]) > 1e-6:
                return {"status": "infeasible", "optimal_value": None, "solution": None}

        for i in range(m):
            basic_col = basis[i]
            coeff = tab[1][basic_col]
            if abs(coeff) > 1e-9:
                for c_col in range(total_vars + 1):
                    tab[1][c_col] -= coeff * tab[i + 2][c_col]

        allowed_cols = n + num_slack
        status = self._pivot_phase(tab, basis, obj_row=1, active_cols=allowed_cols)
        if status == "unbounded":
            return {"status": "unbounded", "optimal_value": None, "solution": None}

        sol = [0.0] * n
        for i in range(m):
            if basis[i] < n:
                sol[basis[i]] = tab[i + 2][-1]

        opt_val = tab[1][-1]
        if not self.maximize:
            opt_val = -opt_val

        shadow_prices = []
        for s_idx, (r, sign) in enumerate(slack_surplus):
            col = n + s_idx
            shadow_prices.append(tab[1][col] * sign)

        return {
            "status": "optimal",
            "optimal_value": round(opt_val, 6),
            "solution": [round(x, 6) for x in sol],
            "basis": basis,
            "shadow_prices": [round(p, 6) for p in shadow_prices[:m]]
        }

    def _pivot_phase(self, tab: List[List[float]], basis: List[int], obj_row: int, active_cols: int) -> str:
        m = self.m
        max_iters = 500
        for _ in range(max_iters):
            entering_col = -1
            min_val = -1e-9
            for j in range(active_cols):
                if tab[obj_row][j] < min_val:
                    min_val = tab[obj_row][j]
                    entering_col = j

            if entering_col == -1:
                return "optimal"

            leaving_row = -1
            min_ratio = float("inf")
            for i in range(m):
                a_ij = tab[i + 2][entering_col]
                if a_ij > 1e-9:
                    ratio = tab[i + 2][-1] / a_ij
                    if ratio < min_ratio - 1e-9:
                        min_ratio = ratio
                        leaving_row = i

            if leaving_row == -1:
                return "unbounded"

            p_row = leaving_row + 2
            pivot_val = tab[p_row][entering_col]
            for j in range(len(tab[0])):
                tab[p_row][j] /= pivot_val

            for r in range(len(tab)):
                if r != p_row:
                    factor = tab[r][entering_col]
                    if abs(factor) > 1e-12:
                        for j in range(len(tab[0])):
                            tab[r][j] -= factor * tab[p_row][j]

            basis[leaving_row] = entering_col

        return "optimal"
