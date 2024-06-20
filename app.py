from dash_manager import app
import os


def main():
    os.environ['REACT_VERSION'] = '18.2.0'
    from ui.layout import get_layout
    app.layout = get_layout
    app.run(debug=True)


if __name__ == '__main__':
    main()
