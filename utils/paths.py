import os
import sys


def get_base_path():
    """
    Retorna o caminho base do projeto,
    compatível com PyInstaller
    """

    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS

    return os.path.abspath(".")


def get_asset_path(filename):
    """
    Retorna caminho absoluto para assets
    """

    base_path = get_base_path()

    return os.path.join(
        base_path,
        "assets",
        filename
    )