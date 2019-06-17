import json
from aiohttp import web
from aiofile import AIOFile

def find_path(vertex, edges):
    for edge in edges:
        for v in edge:
            vertex[v]["neighbors"].update(set(edge))

    min_vertex = "v1"
    ber = list(vertex.keys())

    for _ in vertex:
        vertex_data = vertex[min_vertex]
        vertex_data["neighbors"].remove(min_vertex)
        for neighbor in vertex_data["neighbors"]:
            p = edges.get((min_vertex, neighbor)) or edges.get((neighbor, min_vertex))  # не проверяется направленность
            a = vertex[min_vertex]["score"] + p

            if a < vertex[neighbor]["score"]:
                vertex[neighbor]["path"] = vertex[min_vertex]["path"] + "->" + neighbor
                vertex[neighbor]["score"] = vertex[min_vertex]["score"] + p

        ber.remove(min_vertex)

        mn = float("inf")
        for v in ber:
            if vertex[v]["score"] < mn:
                min_vertex = v
                mn = vertex[v]["score"]
    return vertex


def to_cytoscape(vertex, edges):
    answer = []

    for k, v in vertex.items():
        answer.append({"group": "nodes",
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
        }, )

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
