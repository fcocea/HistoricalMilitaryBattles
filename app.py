from dash_manager import app
import os


def main():
    os.environ['REACT_VERSION'] = '18.2.0'
    from ui.layout import get_layout
    app.layout = get_layout
    app.run(debug=True, dev_tools_ui=False, dev_tools_props_check=False,
            dev_tools_serve_dev_bundles=False)


if __name__ == '__main__':
    main()
