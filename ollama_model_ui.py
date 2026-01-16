"""
Simple Streamlit UI to browse local Ollama models and query them.
"""
import subprocess
from typing import List, Dict

import streamlit as st


def list_ollama_models(timeout: int = 10) -> List[Dict[str, str]]:
    """Return local Ollama models from `ollama list`."""
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to list models.")

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) <= 1:
        return []

    models = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 3:
            continue
        name = parts[0]
        model_id = parts[1]
        size = parts[2]
        modified = " ".join(parts[3:]) if len(parts) > 3 else ""
        models.append(
            {
                "name": name,
                "id": model_id,
                "size": size,
                "modified": modified
            }
        )
    return models


def run_ollama(model: str, prompt: str, timeout: int) -> str:
    """Run `ollama run` and return the response."""
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        error_msg = result.stderr.strip() or "Unknown Ollama error."
        raise RuntimeError(error_msg)

    return result.stdout.strip()


def reset_responses_on_new_question(question: str) -> None:
    """Clear stored responses when the question changes."""
    if st.session_state.get("last_question") != question:
        st.session_state["responses_by_model"] = {}
        st.session_state["last_question"] = question


def main() -> None:
    st.set_page_config(
        page_title="Local Ollama Models",
        page_icon="🧠",
        layout="wide"
    )

    st.title("Local Ollama Model Explorer")
    st.write(
        "Select a local model, ask a question, and compare responses across models. "
        "This demo highlights how Ollama enables local LLMs and helps pick the right "
        "model for different use cases."
    )

    st.sidebar.header("Settings")
    timeout = st.sidebar.slider("Timeout (seconds)", min_value=30, max_value=600, value=300, step=30)

    try:
        models = list_ollama_models()
    except Exception as exc:
        st.error(f"Failed to list models: {exc}")
        st.stop()

    if not models:
        st.warning("No Ollama models found. Run `ollama pull <model>` first.")
        st.stop()

    model_names = [m["name"] for m in models]
    selected_model = st.selectbox("Choose a local model", model_names)

    st.caption("Installed models")
    st.dataframe(models, use_container_width=True)

    question = st.text_area("Your question", placeholder="Ask something like: What is RAG?")
    reset_responses_on_new_question(question)

    if "responses_by_model" not in st.session_state:
        st.session_state["responses_by_model"] = {}

    if st.button("Ask selected model", type="primary", disabled=not question.strip()):
        with st.spinner(f"Running {selected_model}..."):
            try:
                answer = run_ollama(selected_model, question, timeout=timeout)
                st.session_state["responses_by_model"][selected_model] = answer
            except Exception as exc:
                st.error(f"Model error: {exc}")

    if st.session_state["responses_by_model"]:
        st.subheader("Responses by model")
        for model_name, answer in st.session_state["responses_by_model"].items():
            st.markdown(f"**{model_name}**")
            st.write(answer)

    st.divider()
    st.info(
        "Tip: Ask the same question across multiple models to compare speed, "
        "verbosity, and quality. This is a great way to choose a model for your use case."
    )


if __name__ == "__main__":
    main()
