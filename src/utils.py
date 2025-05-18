def load_css():
    with open("assets/styles/main.css") as f:
        css = f.read()
    return f"<style>{css}</style>"