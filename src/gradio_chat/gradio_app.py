"""
Gradio interface for the tennis booking assistant.
"""

import os
import gradio as gr

from src.constants import APPLICATION_NAME, APPLICATION_DESCRIPTION
from src.gradio_chat.gradio_interface import ChatInterface


class ApplicationInterface:
    """Gradio interface for the tennis booking assistant."""

    def __init__(self, llm_api_key: str, llm_name: str):
        self.agent_chat = ChatInterface(llm_api_key, llm_name)
        self.chat_history: list[dict] = []

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface."""
        with gr.Blocks(
                title=APPLICATION_NAME,
        ) as interface:
            gr.Markdown(APPLICATION_DESCRIPTION)

            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat with Agent",
                height=500,
                show_label=True,
                container=True,
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
                self.agent_chat.run,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )

            msg.submit(
                self.agent_chat.run,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )

            clear_btn.click(
                lambda: ([], ""),
                outputs=[chatbot, msg]
            )

        return interface


def create_app(llm_api_key: str, llm_name: str) -> gr.Blocks:
    """Create and return the Gradio app."""
    interface = ApplicationInterface(llm_api_key, llm_name)
    return interface.create_interface()


if __name__ == "__main__":
    # For testing - you would normally get this from environment
    llm_api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    llm_name = os.getenv("OPENAI_MODEL_NAME", "your-api-key-here")
    app = create_app(llm_api_key, llm_name)
    app.launch(share=True)
