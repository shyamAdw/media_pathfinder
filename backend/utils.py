import networkx as nx

def build_graph(data):
    graph = nx.DiGraph()
    for item in data:
        # Add nodes and edges based on your data structure
        # Example:
        graph.add_node(item['campaign_id'], type='campaign', name=item['campaign_name'], spend=item['cost'])
        if 'match_type' in item:
            graph.add_node(item['match_type'], type='match_type', spend=item['cost'])
            graph.add_edge(item['campaign_id'], item['match_type'])
    return graph

def aggregate_data(graph, node_id=None):
    # Aggregate data based on the provided node (or the entire graph if node_id is None)
    # Use graph traversal algorithms (DFS/BFS)
    # Calculate revenue-weighted metrics
    if not node_id:
        # Aggregate for the root (customer account)
        data = []
        for node in graph.nodes:
            if graph.nodes[node]['type'] == 'campaign':
                campaign_data = {
                    'name': graph.nodes[node]['name'],
                    'spend': graph.nodes[node]['spend'],
                    'id': node,
                    'children': []
                }
                data.append(campaign_data)

        # Calculate total spend for root level
        total_spend = sum(campaign['spend'] for campaign in data)
        return {'name': 'Account', 'total_spend': total_spend, 'children': data}
    else:
        # Aggregate for the children of the given node
        children_data = []
        for child in graph.neighbors(node_id):
            children_data.append({
                'name': graph.nodes[child].get('name', child),
                'spend': graph.nodes[child]['spend'],
                'id': child,
                'children': [] if graph.nodes[child]['type'] == 'match_type' else None
            })
        return {'name': graph.nodes[node_id]['name'], 'id': node_id, 'children': children_data}


def filter_data(graph, node_id):
    # Filter data based on node_id
    # Example: Filter by campaign type, match type, geography (future), status
    return aggregate_data(graph, node_id)