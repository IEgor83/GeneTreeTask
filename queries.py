import os
from collections import defaultdict, deque

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GeneTreeTask.settings')
django.setup()
from relatives.models import Relationship, Person


def find_longest_path(vertex, edges, component):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    filtered_graph = {v: graph[v] for v in component}
    queue = deque([v for v in filtered_graph if in_degree[v] == 0])
    topo_order = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in filtered_graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    longest_path = {v: float('-inf') for v in component}
    longest_path[vertex] = 0

    for u in topo_order:
        for v in filtered_graph[u]:
            if longest_path[u] + 1 > longest_path[v]:
                longest_path[v] = longest_path[u] + 1

    max_path_length = max(longest_path.values())
    return max_path_length


def find_relatives(vertex, edges):
    graph = {}

    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(v):
        visited.add(v)
        for neighbor in graph.get(v, []):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(vertex)

    return visited

if __name__ == '__main__':
    relationships = Relationship.objects.all()
    relationship_pairs = [(relationship.person.id, relationship.parent.id) for relationship in relationships]
    start_vertex = 13 # указать id человека у которого хотим посчитать членов семьи

    connected_graph = find_relatives(start_vertex, relationship_pairs)
    count_gen = find_longest_path(start_vertex, relationship_pairs, connected_graph)

    people = Person.objects.filter(id__in=connected_graph)
    male_count = people.filter(gender='M').count()
    female_count = people.filter(gender='F').count()

    print('Количество человек в семье (включая дальних родственников):', len(connected_graph))
    print('количество поколений в семье', count_gen + 1)
    print(f"Мужчин: {male_count}")
    print(f"Женщин: {female_count}")
