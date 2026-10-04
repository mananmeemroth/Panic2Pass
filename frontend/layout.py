import tempfile
import os
import gradio as gr
from backend.config import OLLAMA_MODEL
from backend.model_cache import preload_model_into_cache, get_cache_status
from backend.engine import run_panic_stream
from frontend.styles import CUSTOM_CSS


def build_app():
    """
    Builds the Panic2Pass Gradio UI.
    """
    theme = gr.themes.Soft(
        primary_hue="red",
        secondary_hue="blue",
        neutral_hue="slate"
    )

    with gr.Blocks(title="🚨 Panic2Pass | Emergency Pre-Exam AI Rescue") as demo:
        # Hero Header Banner
        gr.HTML(
            f"""
            <div class="hero-header">
                <h1 class="hero-title">🚨 Panic2Pass</h1>
                <p class="hero-subtitle">The Emergency Exam Cramming & Triage Engine &bull; 100% Private Offline AI</p>
                <div class="status-pill-container">
                    <span class="status-badge">🟢 Model: {OLLAMA_MODEL} (Cached in Memory)</span>
                    <span style="background: rgba(239,68,68,0.12); color: #dc2626; padding: 4px 12px; border-radius: 9999px; font-size: 0.82rem; font-weight: 600;">⚡ Instant 30-Min Triage</span>
                    <span style="background: rgba(59,130,246,0.12); color: #2563eb; padding: 4px 12px; border-radius: 9999px; font-size: 0.82rem; font-weight: 600;">🧠 High-Yield Active Recall</span>
                </div>
            </div>
            """
        )

        with gr.Row():
            # Left Column: Material Ingestion & Panic Modes
            with gr.Column(scale=5):
                with gr.Group():
                    gr.Markdown("### 📂 1. Study Material")
                    notes_file = gr.File(
                        label="Upload Syllabus / Lecture Notes (PDF)",
                        file_types=[".pdf"],
                        file_count="single"
                    )
                    notes_text = gr.Textbox(
                        label="Or Paste Notes / Topics Here",
                        placeholder="e.g. Operating Systems: Deadlocks, Banker's Algorithm, Paging, TLB, Virtual Memory...",
                        lines=5,
                    )
                    weak_topic = gr.Textbox(
                        label="🎯 What topic are you most worried about?",
                        placeholder="e.g. Banker's algorithm safety condition & need matrix",
                    )

                with gr.Group():
                    gr.Markdown("### 🚨 2. Trigger Panic Mode")
                    btn_crash = gr.Button("⚡ 30-Min Crash Plan", variant="primary", elem_classes=["btn-crash"])
                    with gr.Row():
                        btn_lost = gr.Button("🆘 I'm Lost (Explain Simply)", elem_classes=["btn-lost"])
                        btn_quiz = gr.Button("📝 Quiz Me (High-Yield)", elem_classes=["btn-quiz"])
                    btn_cheat = gr.Button("📋 Rapid Formula & Cheat Sheet", elem_classes=["btn-cheat"])

            # Right Column: Output Card & Live Streaming
            with gr.Column(scale=7):
                with gr.Group():
                    output_markdown = gr.Markdown(
                        value="### 🏁 Welcome to Panic2Pass!\n\nUpload your notes or paste text on the left, then click any **Panic Mode** button to generate your personalized exam rescue plan.",
                        elem_classes=["output-card"]
                    )
                    with gr.Row():
                        download_btn = gr.DownloadButton("📥 Download Plan (.md)", visible=False)
                        clear_btn = gr.Button("🧹 Clear Output", size="sm")

        temp_file_state = gr.State()

        # Cache preloader on page load
        def on_page_load():
            status = preload_model_into_cache()
            return

        demo.load(fn=on_page_load, inputs=[], outputs=[])

        # Panic execution with stream & file creation
        def handle_panic(file_obj, text, topic, mode):
            accumulated = ""
            for chunk in run_panic_stream(file_obj, text, topic, mode):
                accumulated = chunk
                yield accumulated, gr.update(visible=False), None

            # Generate markdown download
            try:
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, "panic2pass_plan.md")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"# Panic2Pass Plan - {mode}\n\n" + accumulated)
                yield accumulated, gr.update(value=file_path, visible=True), file_path
            except Exception:
                yield accumulated, gr.update(visible=False), None

        # Button bindings
        btn_crash.click(
            fn=lambda f, t, w: handle_panic(f, t, w, "⚡ 30-Min Crash Plan"),
            inputs=[notes_file, notes_text, weak_topic],
            outputs=[output_markdown, download_btn, temp_file_state],
        )

        btn_lost.click(
            fn=lambda f, t, w: handle_panic(f, t, w, "🆘 I'm Lost (Explain Simply)"),
            inputs=[notes_file, notes_text, weak_topic],
            outputs=[output_markdown, download_btn, temp_file_state],
        )

        btn_quiz.click(
            fn=lambda f, t, w: handle_panic(f, t, w, "📝 Quiz Me (High-Yield)"),
            inputs=[notes_file, notes_text, weak_topic],
            outputs=[output_markdown, download_btn, temp_file_state],
        )

        btn_cheat.click(
            fn=lambda f, t, w: handle_panic(f, t, w, "📋 Rapid Cheat Sheet"),
            inputs=[notes_file, notes_text, weak_topic],
            outputs=[output_markdown, download_btn, temp_file_state],
        )

        clear_btn.click(
            fn=lambda: ("### 🏁 Welcome to Panic2Pass!\n\nUpload your notes or paste text on the left, then click any **Panic Mode** button.", gr.update(visible=False), None),
            inputs=[],
            outputs=[output_markdown, download_btn, temp_file_state],
        )

    return demo, theme
