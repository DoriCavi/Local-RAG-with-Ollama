import gradio as gr
# import 3_chatbot

# msg = gr.Textbox()
# chatbot = gr.Chatbot() 

questions = []

def store_question(input_prompt: str):
#    input_prompt = input_prompt.strip()
   if input_prompt:
        questions.append(input_prompt)
        # print("Stored:", input_prompt)


def respond(message, chat_history):
    message = message.strip()

    if not message:
        return "", chat_history

    bot_message = chatbot_function(message)
            
    # Add both messages to chat history
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_message})
    
    return "", chat_history

    


def create_demo(chatbot_function):
    # ---------- UI ----------
    with gr.Blocks() as demo:
    # ---------- HEADER ----------
        with gr.Row(elem_id="header"):
            gr.Markdown('<div class="header-title">💬 Apple Watch User Guide ChatBot</div>')
        
        # ---------- CENTERED CHAT INTERFACE ----------
        with gr.Row():
            with gr.Column(scale=1):
                pass  # Empty column for centering
            
            with gr.Column(scale=3, elem_id="center-chat"):
                # Chatbot
                chatbot = gr.Chatbot(
                    elem_id="chatbot",
                    height="60vh",
                    show_label=False,
                    avatar_images=(None, "🤖"),
                    type="messages",
                    show_copy_button=True,
                    allow_tags=False
                )
                
                # Input row with arrow button
                with gr.Row(elem_id="input-wrapper"):
                    msg = gr.Textbox(
                        placeholder="Ask any question about the Apple Watch User Guide...",
                        show_label=False,
                        container=False,
                        elem_classes="input-textbox",
                        lines=1,
                        max_lines=5,
                        scale=10
                    )
                    submit = gr.Button("➤", elem_classes="send-btn-arrow", scale=1, size="lg")
                
                # Clear button
                with gr.Row():
                    clear = gr.Button("🗑️ Clear Chat", elem_classes="clear-btn", size="sm")
            
            with gr.Column(scale=1):
                pass  # Empty column for centering
        
        # ---------- PDF LINK AT BOTTOM ----------
        with gr.Row(elem_id="footer"):
            pdf_url = "https://help.apple.com/pdf/watch/8/en_US/apple-watch-user-guide-watchos8.pdf"
            gr.Markdown(
                    f"### 📄 Online PDF\n[Open PDF in new tab]({pdf_url})"
                )
            gr.HTML(
                    f"""
                    <iframe class="pdf-frame"
                            src="{pdf_url}"
                            title="PDF Viewer">
                    </iframe>
                    """
                )
            def respond(message, chat_history):
                """Handle user message and get bot response."""
                # Check if message is empty
                if not message.strip():
                    return "", chat_history
                
                # Call the backend function (ask_question from 3_chatbot.py)
                bot_message = chatbot_function(message)
                
                # Add user message and bot response to chat history
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": bot_message})
                
                # Return empty string (clears textbox) and updated history
                return "", chat_history
            

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            submit.click(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: [], None, chatbot)
                
        return demo


   
# ---------- LAUNCH ----------
custom_css = """
/* Header */
#header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    text-align: center;
}

.header-title {
    color: white;
    font-size: 28px;
    font-weight: 600;
    margin: 0;
}

/* Center chat container */
#center-chat {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Chatbot styling */
#chatbot {
    border-radius: 12px;
    border: 1px solid #e5e5e5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Input wrapper */
#input-wrapper {
    margin-top: 15px;
    gap: 10px;
}

.input-textbox textarea {
    border: 2px solid #e5e5e5 !important;
    border-radius: 25px !important;
    padding: 12px 20px !important;
    font-size: 15px !important;
    transition: border-color 0.3s ease !important;
}

.input-textbox textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Arrow send button */
.send-btn-arrow {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    font-size: 24px !important;
    cursor: pointer !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.send-btn-arrow:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

/* Clear button */
.clear-btn {
    border: 1px solid #e5e5e5 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

.clear-btn:hover {
    border-color: #667eea !important;
    color: #667eea !important;
}

/* Footer PDF link */
#footer {
    background: #f9fafb;
    margin-top: 20px;
}

#pdf-link a {
    color: #667eea !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}

#pdf-link a:hover {
    text-decoration: underline !important;
}

/* Responsive */
@media (max-width: 768px) {
    #center-chat {
        padding: 10px;
    }
}
"""


if __name__ == "__main__":
   demo = create_demo()
   demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False,
    )
