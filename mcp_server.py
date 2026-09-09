"""MCP Server for Branch and Bound MILP Solver Skill."""
import json
import sys
from client import BranchAndBoundMILP

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "solve_milp",
                            "description": "Solve Mixed-Integer Linear Program via Branch and Bound",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "c": {"type": "array", "items": {"type": "number"}},
                                    "A": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                                    "b": {"type": "array", "items": {"type": "number"}},
                                    "integer_indices": {"type": "array", "items": {"type": "integer"}},
                                    "maximize": {"type": "boolean"}
                                },
                                "required": ["c", "A", "b", "integer_indices"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                solver = BranchAndBoundMILP(
                    c=args["c"],
                    A=args["A"],
                    b=args["b"],
                    integer_indices=args["integer_indices"],
                    maximize=args.get("maximize", True)
                )
                output = solver.solve()
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(output)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
