"""Example usage for Branch and Bound MILP Solver Skill."""
from client import BranchAndBoundMILP

def main():
    print("Executing Branch and Bound MILP Solver...")
    # Maximize 5x1 + 4x2
    # s.t.
    #  x1 + x2 <= 5
    #  10x1 + 6x2 <= 45
    #  x1, x2 in Z+
    c = [5.0, 4.0]
    A = [[1.0, 1.0], [10.0, 6.0]]
    b = [5.0, 45.0]
    bb = BranchAndBoundMILP(c=c, A=A, b=b, integer_indices=[0, 1], maximize=True)
    res = bb.solve()
    print("Result:", res)
    assert res["status"] == "optimal", "MILP solver failed"
    assert abs(res["optimal_value"] - 23.0) < 1e-4, f"Unexpected opt val {res['optimal_value']}"
    assert res["solution"] == [3.0, 2.0]
    print("Branch and Bound MILP Solver verified successfully!")

if __name__ == "__main__":
    main()
