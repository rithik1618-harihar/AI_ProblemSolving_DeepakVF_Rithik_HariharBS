"""
Smart Navigation System — Flask Web Application
Problem 8: AI Problem Solving Assignment
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from algorithms import Graph, compare_algorithms

app = Flask(__name__, template_folder="../templates", static_folder="../static")


# ─── Routes ───────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    """
    POST /api/search
    Body: { "edges": [["A","B"], ...], "start": "A", "goal": "G" }
    """
    data = request.get_json()

    edges = data.get("edges", [])
    start = data.get("start", "").strip().upper()
    goal = data.get("goal", "").strip().upper()

    if not start or not goal:
        return jsonify({"error": "Start and goal nodes are required"}), 400

    g = Graph()
    for edge in edges:
        if len(edge) == 2:
            g.add_edge(str(edge[0]).upper(), str(edge[1]).upper())

    if start not in g.adjacency_list:
        return jsonify({"error": f"Start node '{start}' not found in graph"}), 400
    if goal not in g.adjacency_list:
        return jsonify({"error": f"Goal node '{goal}' not found in graph"}), 400

    result = compare_algorithms(g, start, goal)
    result["nodes"] = g.get_nodes()
    result["edges"] = g.get_edges()
    return jsonify(result)


@app.route("/api/example", methods=["GET"])
def example():
    """Return a pre-built example graph."""
    g = Graph()
    example_edges = [
        ["A", "B"], ["A", "C"], ["B", "D"],
        ["B", "E"], ["C", "F"], ["D", "G"],
        ["E", "G"], ["F", "G"],
    ]
    for e in example_edges:
        g.add_edge(e[0], e[1])

    result = compare_algorithms(g, "A", "G")
    result["nodes"] = g.get_nodes()
    result["edges"] = g.get_edges()
    result["start"] = "A"
    result["goal"] = "G"
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
