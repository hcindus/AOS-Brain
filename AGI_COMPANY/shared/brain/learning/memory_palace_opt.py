"""
Memory Palace Optimization Module
Cluster memories and build portals.
"""


def cluster_memories(memory_store, min_shared=2):
    """
    Cluster memories by shared concepts.
    
    Args:
        memory_store: Object with .traces list
        min_shared: Minimum shared concepts to cluster
    """
    clusters = []
    for t in memory_store.traces:
        placed = False
        for cluster in clusters:
            if any(len(set(t["concepts"]) & set(o["concepts"])) >= min_shared for o in cluster):
                cluster.append(t)
                placed = True
                break
        if not placed:
            clusters.append([t])
    return clusters


def build_portals(clusters, coactivation_threshold=5):
    """
    Build portals between frequently co-activated clusters.
    
    Args:
        clusters: List of memory clusters
        coactivation_threshold: Minimum shared activations for portal
    """
    portals = []
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            c1, c2 = clusters[i], clusters[j]
            shared = 0
            for t1 in c1:
                for t2 in c2:
                    if set(t1["concepts"]) & set(t2["concepts"]):
                        shared += 1
            if shared >= coactivation_threshold:
                portals.append((i, j))
    return portals


def optimize_memory_palace(memory_store):
    """
    Optimize memory palace structure.
    
    Returns:
        (clusters, portals) - Optimized structure
    """
    clusters = cluster_memories(memory_store)
    portals = build_portals(clusters)
    return clusters, portals
