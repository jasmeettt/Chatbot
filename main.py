import streamlit as st
# ✅ Set page config at the very start
st.set_page_config(layout="wide", page_title="QuickRail Chatbot", page_icon="🚆")

from streamlit_option_menu import option_menu
import home
import rule_based_chatbot  # ✅ Ensure the file exists in the same directory



# Reducing whitespace on the top of the page
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.app = []

    def add_app(self, title, func):
        self.app.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            st.markdown("""
            <style>
            .gradient-text {
              margin-top: -20px;
            }
            </style>
            """, unsafe_allow_html=True)

            typing_animation = """
            <h3 style="text-align: left;">
            <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=30&Left=true&vLeft=true&width=250&height=80&lines=QuickRail+Chatbot" alt="Typing Animation" />
            </h3>
            """
            st.markdown(typing_animation, unsafe_allow_html=True)
            st.sidebar.write("")

            app = option_menu(
                menu_title='Sections',
                options=['Home', 'Train Ticketing System'],
                default_index=0,
            )

        # Ensure selected app runs correctly
        try:
            if app == "Home":
                home.app()
            elif app == "Train Ticketing System":
                rule_based_chatbot.app()
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
            st.stop()

# Run the multi-app framework
if __name__ == "__main__":
    MultiApp().run()
