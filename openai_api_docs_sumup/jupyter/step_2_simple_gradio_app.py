# (Step2) simple gradio app
import gradio as gr


# (Example) Write a checkbox overview and sample programme. -
def basic_function(text):
    output1 = text + ":output-1"
    output2 = text + ":output-2"
    return output1, output2


def main():
    iface = gr.Interface(
        fn=basic_function,
        inputs="text",
        outputs=["text", "text"],
        title="Basic Gradio Test",
        description="A simple test to ensure Gradio is working correctly."
    )

    iface.launch()


if __name__ == "__main__":
    main()
