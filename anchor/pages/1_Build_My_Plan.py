import streamlit as st

from common import db, style

st.set_page_config(page_title="Build My Plan — Anchor", page_icon="\U0001F9ED", layout="centered")
style.inject_base_css()

conn = db.get_connection()

if "plan_step" not in st.session_state:
    st.session_state.plan_step = 0

STEPS = ["Metaphor", "Warning signs", "What helps", "Your people", "Reasons & goals", "Message to you", "Done"]
step = st.session_state.plan_step

st.progress(step / (len(STEPS) - 1))
st.markdown(f'<p class="muted">Step {step + 1} of {len(STEPS)} -- {STEPS[step]}</p>', unsafe_allow_html=True)


def list_editor(title, items, add_fn, delete_fn, placeholder):
    st.markdown(f"##### {title}")
    for item in items:
        col1, col2 = st.columns([5, 1])
        col1.markdown(f'<div class="calm-card" style="margin-bottom:0.4rem;">{item["text"]}</div>', unsafe_allow_html=True)
        if col2.button("✕", key=f"del_{title}_{item['id']}"):
            delete_fn(conn, item["id"])
            st.rerun()
    new_text = st.text_input(placeholder, key=f"new_{title}", label_visibility="collapsed", placeholder=placeholder)
    if st.button(f"Add", key=f"add_{title}") and new_text.strip():
        add_fn(conn, new_text.strip())
        st.rerun()


if step == 0:
    st.markdown("### What does it feel like, when it's hard?")
    st.markdown('<p class="muted">Pick whatever fits -- this becomes a visual on your home screen and in Right Now mode.</p>', unsafe_allow_html=True)
    current = db.get_meta(conn)["metaphor"]
    cols = st.columns(len(db.METAPHORS))
    for i, (key, m) in enumerate(db.METAPHORS.items()):
        with cols[i]:
            selected = key == current
            label = f"{m['emoji']}\n{m['label']}"
            if st.button(label, key=f"metaphor_{key}", use_container_width=True):
                db.set_meta(conn, metaphor=key)
                st.rerun()
            if selected:
                st.markdown('<p style="text-align:center; color:#7c8fd6;">selected</p>', unsafe_allow_html=True)

elif step == 1:
    st.markdown("### What do you notice, right before things get hard?")
    st.markdown('<p class="muted">In your own words. Maybe it\'s pulling away from people, not eating, not sleeping -- whatever it actually is for you.</p>', unsafe_allow_html=True)
    list_editor("Warning signs", db.list_warning_signs(conn), db.add_warning_sign, db.delete_warning_sign, "e.g. I stop replying to texts")

elif step == 2:
    st.markdown("### What actually helps you?")
    st.markdown('<p class="muted">Not what\'s supposed to help. What actually has, before.</p>', unsafe_allow_html=True)
    list_editor("What helps", db.list_coping_strategies(conn), db.add_coping_strategy, db.delete_coping_strategy, "e.g. calling my sister")

elif step == 3:
    st.markdown("### Who's actually there for you?")
    st.markdown('<p class="muted">People you could call at 3am. Even just one person is enough.</p>', unsafe_allow_html=True)
    contacts = db.list_contacts(conn)
    for c in contacts:
        col1, col2 = st.columns([5, 1])
        col1.markdown(f'<div class="calm-card" style="margin-bottom:0.4rem;"><b>{c["name"]}</b> -- {c["relationship"]} -- {c["phone"]}</div>', unsafe_allow_html=True)
        if col2.button("✕", key=f"del_contact_{c['id']}"):
            db.delete_contact(conn, c["id"])
            st.rerun()
    with st.form("add_contact", clear_on_submit=True):
        name = st.text_input("Name")
        rel = st.text_input("Relationship (e.g. best friend, mum)")
        phone = st.text_input("Phone number")
        if st.form_submit_button("Add") and name and phone:
            db.add_contact(conn, name, rel, phone)
            st.rerun()

elif step == 4:
    st.markdown("### Why you're staying, and where you're headed.")
    list_editor("Reasons to stay", db.list_reasons(conn), db.add_reason, db.delete_reason, "e.g. my dog needs me")
    st.write("")
    list_editor("Goals & dreams", db.list_goals(conn), db.add_goal, db.delete_goal, "e.g. finish my degree")

elif step == 5:
    st.markdown("### Leave a message for yourself.")
    st.markdown('<p class="muted">Write it now, while you\'re steady, for the version of you who might need to hear it later.</p>', unsafe_allow_html=True)
    current_msg = db.get_meta(conn)["future_message"]
    msg = st.text_area("Your message", value=current_msg, height=160, label_visibility="collapsed")
    if st.button("Save message"):
        db.set_meta(conn, future_message=msg)
        st.success("Saved.")

elif step == 6:
    st.markdown("### Your plan is ready.")
    st.markdown('<p class="muted">It\'ll be exactly where you left it, whenever you need it. You can update any part of it, anytime.</p>', unsafe_allow_html=True)
    if st.button("Try Right Now mode →", use_container_width=True):
        st.session_state.rn_step = 0
        st.switch_page("pages/2_Right_Now.py")

st.write("")
col1, col2 = st.columns(2)
with col1:
    if step > 0 and st.button("← Back"):
        st.session_state.plan_step -= 1
        st.rerun()
with col2:
    if step < len(STEPS) - 1 and st.button("Next →"):
        st.session_state.plan_step += 1
        st.rerun()
