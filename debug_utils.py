import itertools
import matplotlib.pyplot as plt
import networkx as nx


def _filter_pairs(
    golden_pairs, unclustered_pairs, dedupe_pairs, other_pairs, ids_of_interest
):
    golden_pairs = [
        (x, y) for x, y in golden_pairs if x in ids_of_interest or y in ids_of_interest
    ]
    unclustered_pairs = [
        (x, y) for x, y in unclustered_pairs if x in ids_of_interest or y in ids_of_interest
    ]
    dedupe_pairs = [
        (x, y) for x, y in dedupe_pairs if x in ids_of_interest or y in ids_of_interest
    ]
    other_pairs = [
        (x, y) for x, y in other_pairs if x in ids_of_interest or y in ids_of_interest
    ]
    ids_of_interest = set(
        itertools.chain.from_iterable(golden_pairs + dedupe_pairs + other_pairs)
    )
    return (
        golden_pairs,
        unclustered_pairs,
        dedupe_pairs,
        other_pairs,
        ids_of_interest,
    )


def draw_pairs_graph(df, edges, nodes, score_dict, title):
    G = nx.Graph()
    for node in nodes:
        G.add_node(node, name=str(node) + ":" + df.loc[node]["name"])
    G.add_edges_from(edges)

    plt.figure(figsize=(10, 6))
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, alpha=0.3, node_size=1000)
    nx.draw_networkx_labels(
        G, pos, labels=nx.get_node_attributes(G, "name"), font_size=20
    )
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=4)
    edge_labels = {pair: score_dict[pair] for pair in edges if pair in score_dict}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=20)
    plt.margins(0.5, 0.2)
    plt.axis("off")
    plt.title(title, fontdict={"fontsize": 24, "fontweight": "bold"})
    plt.show()


def show_cluster_graphs(
    df,
    golden_pairs,
    unclustered_pairs,
    dedupe_pairs,
    other_pairs,
    score_dict,
    ids_of_interest,
):
    (
        golden_pairs,
        unclustered_pairs,
        dedupe_pairs,
        other_pairs,
        ids_of_interest,
    ) = _filter_pairs(
        golden_pairs,
        unclustered_pairs,
        dedupe_pairs,
        other_pairs,
        ids_of_interest
    )
    display(df.loc[list(ids_of_interest)])
    draw_pairs_graph(df, golden_pairs, ids_of_interest, {}, "Truth")
    draw_pairs_graph(df, unclustered_pairs, ids_of_interest, score_dict, "Unclustered")
    draw_pairs_graph(df, dedupe_pairs, ids_of_interest, score_dict, "Dedupe")
    draw_pairs_graph(df, other_pairs, ids_of_interest, score_dict, "Other")
