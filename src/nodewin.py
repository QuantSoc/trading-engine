from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.node_node import Node
from nodeeditor.node_socket import Socket
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_scene import Scene
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QAction

# Assuming AdditionNode and AdditionNodeContent are already defined as in the previous example

class NodeEditorMainWindow(NodeEditorWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Strategy Creator")

if __name__ == "__main__":
    app = QApplication([])
    main_window = NodeEditorMainWindow()
    main_window.show()
    app.exec_()
