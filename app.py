from dash_manager import app
import os

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

if __name__ == '__main__':
    os.environ['REACT_VERSION'] = '18.2.0'
    from ui.layout import get_layout
    app.layout = get_layout
    app.run(debug=True)
