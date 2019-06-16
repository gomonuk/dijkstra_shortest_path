infinity = float("inf")

vertex = {
    "v1": {"score": infinity, "path": "", "neighbors": set()},
    "v2": {"score": infinity, "path": "", "neighbors": set()},
    "v3": {"score": infinity, "path": "", "neighbors": set()},
    "v4": {"score": infinity, "path": "", "neighbors": set()},
    "v5": {"score": infinity, "path": "", "neighbors": set()},
    "v6": {"score": infinity, "path": "", "neighbors": set()},
    "v7": {"score": 0,        "path": "v7", "neighbors": set()},
    "v8": {"score": infinity, "path": "", "neighbors": set()}
}

# v7 - v8

edges = {
    ("v1", "v4"): 24,
    ("v2", "v6"): 8,
    ("v5", "v6"): 3,

    ("v1", "v6"): 33,
    ("v3", "v5"): 26,
    ("v5", "v7"): 15,

    ("v1", "v8"): 27,
    ("v3", "v7"): 23,
    ("v5", "v8"): 11,

    ("v2", "v3"): 21,
    ("v4", "v5"): 25,
    ("v6", "v8"): 14,

    ("v2", "v4"): 12,
    ("v4", "v6"): 2

}

for edge in edges:
    for v in edge:
        vertex[v]["neighbors"].update(set(edge))

min_vertex = "v1"
ber = list(vertex.keys())

for i in vertex:
    vertex_data = vertex[min_vertex]
    vertex_data["neighbors"].remove(min_vertex)
    for neighbor in vertex_data["neighbors"]:
        p = edges.get((min_vertex, neighbor)) or edges.get((neighbor, min_vertex))  # не проверяется направленность
        a = vertex[min_vertex]["score"] + p

        if a < vertex[neighbor]["score"]:
            vertex[neighbor]["path"] = vertex[min_vertex]["path"] + "->" + neighbor
            vertex[neighbor]["score"] = vertex[min_vertex]["score"] + p

        # vertex[neighbor]["score"] = a if a < vertex[neighbor]["score"] else vertex[neighbor]["score"]

    ber.remove(min_vertex)

    mn = float("inf")
    for v in ber:
        if vertex[v]["score"] < mn:
            min_vertex = v
            mn = vertex[v]["score"]

print(vertex)

# for v, v_data in vertex.items():
#     print(v)
# print(vertex)
