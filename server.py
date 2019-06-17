import json
from aiohttp import web
from aiofile import AIOFile


def find_path(vertex, edges):
    for edge in edges:
        for v in edge:
            vertex[v]["neighbors"].update(set(edge))

    vertex_with_min_score = "v1"
    need_visit = list(vertex.keys())

    for _ in vertex:
        vertex_data = vertex[vertex_with_min_score]
        vertex_data["neighbors"].remove(vertex_with_min_score)
        for neighbor in vertex_data["neighbors"]:
            # При выборе не проверяется направленность ребра.
            score = edges.get((vertex_with_min_score, neighbor)) or edges.get((neighbor, vertex_with_min_score))

            # Находим минимальный маршрут до вершины neighbor.
            if (vertex[vertex_with_min_score]["score"] + score) < vertex[neighbor]["score"]:
                vertex[neighbor]["path"] = vertex[vertex_with_min_score]["path"] + "->" + neighbor
                vertex[neighbor]["score"] = vertex[vertex_with_min_score]["score"] + score

        need_visit.remove(vertex_with_min_score)

        # Определяем новую вершину с минимальным весом.
        minimum_score = float("inf")
        for v in need_visit:
            if vertex[v]["score"] < minimum_score:
                minimum_score = vertex[v]["score"]
                vertex_with_min_score = v

    return vertex


def to_cytoscape(vertex, edges):
    answer = []

    for k, v in vertex.items():
        answer.append({
            "group": "nodes",
            "classes": "l1",
            "data": {"id": k,
                     "score": v["score"],
                     "path": v["path"],
                     }
        })

    for k, v in edges.items():
        answer.append({
            "data": {
                "id": "_".join(k),
                "source": k[0],
                "target": k[1],
                "label": v,
                "width": v
            }
        })

    return answer


async def get_json(request):
    infinity = float("inf")
    headers = {'Access-Control-Allow-Origin': '*'}

    vertex = {
        "v1": {"score": 0, "path": "v1", "neighbors": set()},
        "v2": {"score": infinity, "path": "", "neighbors": set()},
        "v3": {"score": infinity, "path": "", "neighbors": set()},
        "v4": {"score": infinity, "path": "", "neighbors": set()},
        "v5": {"score": infinity, "path": "", "neighbors": set()},
        "v6": {"score": infinity, "path": "", "neighbors": set()},
        "v7": {"score": infinity, "path": "", "neighbors": set()},
        "v8": {"score": infinity, "path": "", "neighbors": set()}
    }
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

    vertex = find_path(vertex, edges)
    answer = to_cytoscape(vertex, edges)
    
    return web.Response(body=json.dumps(answer), headers=headers)


async def get_index(request):
    async with AIOFile("index.html", 'r') as afp:
        text = await afp.read()
        
    return web.Response(text=text, content_type='text/html', )


app = web.Application()
app.router.add_get('/', get_index)
app.router.add_get('/get_json', get_json)
app.router.add_static('/lib', 'lib', name='lib')

host = 'localhost'
port = 9996

if __name__ == '__main__':
    web.run_app(app, host=host, port=port)
