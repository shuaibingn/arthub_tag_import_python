from tk.gui import TkGUI
from utils.yaml_tools import read_yaml


if __name__ == '__main__':
    yaml_data = read_yaml("config.yaml")
    tk = TkGUI("ArtHub Tag", **yaml_data)
    tk.root.mainloop()
