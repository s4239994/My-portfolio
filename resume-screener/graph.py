import networkx as nx
from pyvis.network import Network

NODE_COLORS = {
    "matched": "#39FF88",
    "resume_only": "#4da6ff",
    "gap": "#ff6666",
}


def build_concept_graph(resume_skills: set, jd_skills: set, taxonomy: dict) -> nx.Graph:
    """Nodes colored by status: matched (in both), resume-only, or a gap (JD wants it,
    resume doesn't have it). Edges come from the taxonomy's related-concept links."""
    graph = nx.Graph()

    matched = resume_skills & jd_skills
    resume_only = resume_skills - jd_skills
    gaps = jd_skills - resume_skills

    for skill in matched:
        graph.add_node(skill, status="matched")
    for skill in resume_only:
        graph.add_node(skill, status="resume_only")
    for skill in gaps:
        graph.add_node(skill, status="gap")

    all_skills = matched | resume_only | gaps
    for skill_a, skill_b in taxonomy["related_links"]:
        if skill_a in all_skills and skill_b in all_skills:
            graph.add_edge(skill_a, skill_b)

    return graph


def render_graph_html(graph: nx.Graph) -> str:
    # cdn_resources="in_line" embeds vis-network's JS/CSS directly in the HTML,
    # instead of writing a "lib/" folder and linking to it by relative path --
    # the latter breaks once this HTML is embedded in Streamlit's iframe.
    net = Network(
        height="480px", width="100%", bgcolor="#0e0e10", font_color="#f5f5f5",
        cdn_resources="in_line",
    )
    net.barnes_hut()

    for node, data in graph.nodes(data=True):
        color = NODE_COLORS.get(data.get("status"), "#999999")
        net.add_node(node, label=node, color=color)

    for source, target in graph.edges():
        net.add_edge(source, target, color="#3a3b3f")

    return net.generate_html(notebook=False)
