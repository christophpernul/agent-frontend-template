"""
Gradio interface for the tennis booking assistant.
"""

import os
import gradio as gr
from typing import List, Tuple

from src.constants import APPLICATION_NAME, APPLICATION_DESCRIPTION
from src.agent.agent import AIAgent


class ApplicationInterface:
    """Gradio interface for the tennis booking assistant."""

    def __init__(self, openai_api_key: str):
        self.agent = AIAgent(openai_api_key)
        self.chat_history: List[dict] = []

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface."""
        with gr.Blocks(
                title=APPLICATION_NAME,
                theme=gr.themes.Soft(),
                css="""
            .chat-container {
                max-height: 600px;
                overflow-y: auto;
            }
            .response-container {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #007bff;
            }
            """
        ) as interface:
            gr.Markdown(APPLICATION_DESCRIPTION)

            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat with Agent",
                height=500,
                show_label=True,
                container=True,
                type="messages"
            )

            with gr.Row():
                # Text input
                msg = gr.Textbox(
                    label="Submit Message",
                    placeholder="e.g., Tell me something about Munich.",
                    lines=2,
                    scale=3
                )

            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary", size="lg")
                clear_btn = gr.Button("Delete Chat", variant="secondary")

            # Event handlers
            submit_btn.click(
                self.agent.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )

            msg.submit(
                self.agent.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )

            clear_btn.click(
                lambda: ([], ""),
                outputs=[chatbot, msg]
            )

        return interface


def create_app(openai_api_key: str) -> gr.Blocks:
    """Create and return the Gradio app."""
    interface = ApplicationInterface(openai_api_key)
    return interface.create_interface()


if __name__ == "__main__":
    # For testing - you would normally get this from environment
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    app = create_app(api_key)
    app.launch(share=True)
