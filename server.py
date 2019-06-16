import json
from aiohttp import web

app = web.Application()


def to_cytoscape():
    vertex = {'v1': {'score': 0, 'path': 'v1', 'neighbors': {'v8', 'v4', 'v6'}},
              'v2': {'score': 34, 'path': 'v1->v4->v6->v2', 'neighbors': {'v6', 'v4', 'v3'}},
              'v3': {'score': 55, 'path': 'v1->v4->v6->v5->v3', 'neighbors': {'v5', 'v7', 'v2'}},
              'v4': {'score': 24, 'path': 'v1->v4', 'neighbors': {'v5', 'v1', 'v6', 'v2'}},
              'v5': {'score': 29, 'path': 'v1->v4->v6->v5', 'neighbors': {'v8', 'v7', 'v4', 'v6', 'v3'}},
              'v6': {'score': 26, 'path': 'v1->v4->v6', 'neighbors': {'v5', 'v8', 'v1', 'v4', 'v2'}},
              'v7': {'score': 44, 'path': 'v1->v4->v6->v5->v7', 'neighbors': {'v5', 'v3'}},
              'v8': {'score': 27, 'path': 'v1->v8', 'neighbors': {'v5', 'v1', 'v6'}}}

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

    answer = []

    for k, v in vertex.items():
        # {data: {id: 'a', name: 'Albert'}},
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


async def get(request):
    print("GET")
    # answer = [
    #     {"data": {"id": 'a'}},
    #     {"data": {"id": 'b'}},
    #
    #     {"data": {"id": 'c'}},
    #     {"data": {"id": 'd'}},
    #
    #     {"data": {
    #         "id": 'ab',
    #         "source": 'a',
    #         "target": 'b'
    #     }},
    #
    #     {"data": {
    #         "id": 'ab1',
    #         "source": 'a',
    #         "target": 'c'
    #     }},
    #
    #     {"data": {
    #         "id": 'ab2',
    #         "source": 'a',
    #         "target": 'd'
    #     }}
    #
    # ]
    answer = to_cytoscape()

    h = {'Access-Control-Allow-Origin': '*'}

    return web.Response(body=json.dumps(answer), headers=h)


app.router.add_get('/d', get)

host = 'localhost'
port = 9996

if __name__ == '__main__':
    web.run_app(app, host=host, port=port)
