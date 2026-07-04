import tempfile
from pathlib import Path

import streamlit as st

import extractor
import graph
import scoring
import skills
import sound

st.set_page_config(page_title="AI Resume Screener", page_icon="🧭", layout="wide")

STATUS_COLORS = {"good": "#39FF88", "partial": "#f5c542", "weak": "#ff6666"}
TIER_LABELS = {"good": "Strong match", "partial": "Partial match", "weak": "Weak match"}


def render_tags(skill_set: set, color: str) -> None:
    if not skill_set:
        st.caption("None")
        return
    tags_html = "".join(
        f'<span class="skill-tag" style="background:{color}22; color:{color}; '
        f'border: 1px solid {color};">{s}</span>'
        for s in sorted(skill_set)
    )
    st.markdown(tags_html, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    @keyframes pulse-good {
        0% { box-shadow: 0 0 0 0 rgba(57,255,136,0.6); }
        70% { box-shadow: 0 0 0 20px rgba(57,255,136,0); }
        100% { box-shadow: 0 0 0 0 rgba(57,255,136,0); }
    }
    @keyframes pulse-partial {
        0% { box-shadow: 0 0 0 0 rgba(245,197,66,0.6); }
        70% { box-shadow: 0 0 0 20px rgba(245,197,66,0); }
        100% { box-shadow: 0 0 0 0 rgba(245,197,66,0); }
    }
    @keyframes shake-weak {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-4px); }
        40% { transform: translateX(4px); }
        60% { transform: translateX(-4px); }
        80% { transform: translateX(4px); }
    }
    .pulse-good { animation: pulse-good 1.6s ease-out 2; border-radius: 16px; }
    .pulse-partial { animation: pulse-partial 1.6s ease-out 2; border-radius: 16px; }
    .pulse-weak { animation: shake-weak 0.5s ease-in-out 1; border-radius: 16px; }
    .skill-tag {
        display: inline-block; padding: 3px 10px; margin: 3px;
        border-radius: 999px; font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        font-size: 0.8rem;
    }
    .terminal-tag {
        font-family: "Consolas", "SFMono-Regular", Menlo, monospace;
        color: #39FF88;
        opacity: 0.85;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(245,197,66,0.10), rgba(57,255,136,0.02));
        border: 1px solid #2a2b2f;
        border-left: 4px solid #f5c542;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.75rem;
    }
    .hero-title { margin: 0.3rem 0 0.4rem; font-size: 1.9rem; }
    .hero-caption { color: #9a9a9a; margin: 0; font-size: 0.95rem; }
    .input-card {
        background: #17181b; border: 1px solid #2a2b2f; border-radius: 12px;
        padding: 1.1rem 1.25rem 0.6rem; height: 100%;
    }
    .input-card h4 { margin-top: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <p class="terminal-tag">&gt; VIBE STATE: AI SCREENING VIBRATION ACTIVE</p>
        <p class="hero-title">🧭 AI Resume Screening &amp; Keyword Matcher</p>
        <p class="hero-caption">Parses a resume, maps it to a skill graph, and scores it
        against a job description -- skills, experience, and semantic potential.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

taxonomy = skills.load_taxonomy()

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-card"><h4>📄 Resume</h4>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload a resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    resume_text_input = st.text_area("...or paste resume text", height=200)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-card"><h4>🎯 Job description</h4>', unsafe_allow_html=True)
    jd_text_input = st.text_area("Paste the job description", height=280, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

screen_clicked = st.button("Screen Resume", type="primary")

if screen_clicked:
    if resume_file is not None:
        suffix = Path(resume_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(resume_file.getbuffer())
            tmp_path = tmp.name
        resume_text = extractor.extract_text(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)
    else:
        resume_text = extractor.clean_text(resume_text_input)

    jd_text = extractor.clean_text(jd_text_input)

    if not resume_text or not jd_text:
        st.warning("Please provide both a resume and a job description.")
    else:
        with st.spinner("Screening..."):
            sound.play_screening_cue()
            resume_skills = skills.extract_skills(resume_text, taxonomy)
            jd_skills = skills.extract_skills(jd_text, taxonomy)
            resume_years = skills.extract_experience_years(resume_text)
            jd_years = skills.extract_experience_years(jd_text)
            result = scoring.compute_match(resume_skills, jd_skills, resume_years, jd_years)

        sound.play_result_cue(result["tier"])

        pulse_class = f"pulse-{result['tier']}"
        color = STATUS_COLORS[result["tier"]]

        st.markdown(
            f"""
            <div class="{pulse_class}" style="border: 2px solid {color}; padding: 24px; text-align: center;">
                <div style="font-size: 0.9rem; color: #9a9a9a; font-family: 'Consolas', 'SFMono-Regular', Menlo, monospace;">OVERALL MATCH</div>
                <div style="font-size: 3rem; font-weight: 700; color: {color};">{result['overall_score']}%</div>
                <div style="font-size: 1rem; color: {color};">{TIER_LABELS[result['tier']]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        bar_col1, bar_col2 = st.columns(2)
        with bar_col1:
            st.caption(f"Skill coverage -- {result['skill_score']}%")
            st.progress(result["skill_score"] / 100)
        with bar_col2:
            years_label = jd_years if jd_years else "not specified"
            st.caption(
                f"Experience match -- {result['experience_score']}% "
                f"(resume: {resume_years} yrs, required: {years_label})"
            )
            st.progress(result["experience_score"] / 100)

        st.write("")
        tab_skills, tab_graph = st.tabs(["📋 Skill Breakdown", "🕸️ Concept Graph"])

        with tab_skills:
            st.markdown("**Matched skills**")
            render_tags(result["exact_matches"], "#39FF88")

            if result["related"]:
                st.markdown("**Related skills found (semantic match)**")
                for gap_skill, info in result["related"].items():
                    st.write(
                        f"- Resume's **{info['closest_skill']}** is related to "
                        f"required **{gap_skill}** (similarity {info['similarity']})"
                    )

            remaining_gaps = result["gaps"] - set(result["related"].keys())
            if remaining_gaps:
                st.markdown("**Missing skills**")
                render_tags(remaining_gaps, "#ff6666")

        with tab_graph:
            concept_graph = graph.build_concept_graph(resume_skills, jd_skills, taxonomy)
            if concept_graph.number_of_nodes() == 0:
                st.info("No recognized skills found to graph.")
            else:
                html = graph.render_graph_html(concept_graph)
                st.components.v1.html(html, height=500, scrolling=True)
                st.caption("Green = matched, blue = resume only, red = required but missing")
