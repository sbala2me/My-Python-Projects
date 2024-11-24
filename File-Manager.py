# file_manager.py

import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileSystemModel, QMessageBox,
    QInputDialog, QMenu, QTreeView, QListView, QSplitter,
    QToolBar, QAction, QStatusBar, QWidget, QVBoxLayout, QLineEdit,
    QLabel
)
from PyQt5.QtCore import Qt, QDir, QModelIndex, QSize
from PyQt5.QtGui import QIcon, QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Advanced File Manager")
        MainWindow.resize(1024, 768)
        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # Toolbar
        self.toolBar = QToolBar(MainWindow)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        # Actions
        self.actionNew_Folder = QAction(QIcon.fromTheme("folder-new"), "New Folder", MainWindow)
        self.actionDelete = QAction(QIcon.fromTheme("edit-delete"), "Delete", MainWindow)
        self.actionRefresh = QAction(QIcon.fromTheme("view-refresh"), "Refresh", MainWindow)

        self.toolBar.addAction(self.actionNew_Folder)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionRefresh)

        # Search Bar
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Search...")
        self.toolBar.addWidget(self.searchLineEdit)

        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.verticalLayout.addWidget(self.splitter)

        # Directory Tree
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.splitter.addWidget(self.treeView)

        # Right Pane Splitter
        self.rightSplitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.rightSplitter)

        # File List
        self.listView = QListView()
        self.rightSplitter.addWidget(self.listView)

        # Preview Pane
        self.previewLabel = QLabel("File Preview")
        self.previewLabel.setAlignment(Qt.AlignCenter)
        self.rightSplitter.addWidget(self.previewLabel)

        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)


class FileManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(FileManager, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # Set up the file system model
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath('/')
        self.dir_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('/')
        # Include directories in the file model
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)

        # Configure the tree view (directory tree)
        self.treeView.setModel(self.dir_model)
        self.treeView.setRootIndex(self.dir_model.index('/'))
        self.treeView.clicked.connect(self.on_tree_view_clicked)

        # Configure the list view (file list)
        self.listView.setModel(self.file_model)
        self.listView.setRootIndex(self.file_model.index('/'))
        self.listView.doubleClicked.connect(self.on_file_double_clicked)
        self.listView.clicked.connect(self.on_file_clicked)

        # Connect toolbar actions
        self.actionNew_Folder.triggered.connect(self.create_new_folder)
        self.actionDelete.triggered.connect(self.delete_item)
        self.actionRefresh.triggered.connect(self.refresh_views)

        # Context menu for list view
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.open_context_menu)

        # Search functionality
        self.searchLineEdit.returnPressed.connect(self.search_files)

        # Drag-and-drop support
        self.listView.setDragEnabled(True)
        self.listView.setAcceptDrops(True)
        self.listView.setDefaultDropAction(Qt.MoveAction)
        self.listView.setDropIndicatorShown(True)

        # Load styles
        self.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        QTreeView, QListView {
            background-color: #3c3f41;
            color: #dcdcdc;
            selection-background-color: #606366;
        }
        QToolBar {
            background-color: #3c3f41;
        }
        QStatusBar {
            background-color: #3c3f41;
            color: #dcdcdc;
        }
        QLineEdit {
            background-color: #2b2b2b;
            color: #dcdcdc;
            border: 1px solid #606366;
            border-radius: 4px;
            padding: 4px;
        }
        QLabel {
            color: #dcdcdc;
        }
        """)

        # Initial status bar message
        self.statusbar.showMessage("Welcome to Advanced File Manager", 5000)

    def on_tree_view_clicked(self, index):
        # Update list view based on selected directory
        dir_path = self.dir_model.fileInfo(index).absoluteFilePath()
        self.listView.setRootIndex(self.file_model.setRootPath(dir_path))
        self.statusbar.showMessage(f"Current Directory: {dir_path}")

    def on_file_double_clicked(self, index):
        # Handle file opening or navigation
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        if os.path.isdir(file_path):
            # Open directory in list view
            self.listView.setRootIndex(self.file_model.setRootPath(file_path))
            self.statusbar.showMessage(f"Current Directory: {file_path}")
        else:
            # Open file with default application
            os.system(f'xdg-open "{file_path}"')

    def on_file_clicked(self, index):
        # Preview file content or image
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        if os.path.isfile(file_path):
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                pixmap = QPixmap(file_path)
                self.previewLabel.setPixmap(pixmap.scaled(
                    self.previewLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif file_path.lower().endswith(('.txt', '.py', '.md', '.log', '.ini', '.cfg')):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    self.previewLabel.setText(content)
                except Exception as e:
                    self.previewLabel.setText(f"Could not open file:\n{e}")
            else:
                self.previewLabel.setText("No preview available.")
        else:
            self.previewLabel.setText("")

    def create_new_folder(self):
        index = self.treeView.currentIndex()
        dir_path = self.dir_model.fileInfo(index).absoluteFilePath()
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Folder Name:")
        if ok and folder_name:
            new_folder_path = os.path.join(dir_path, folder_name)
            try:
                os.mkdir(new_folder_path)
                self.refresh_views()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder:\n{e}")

    def delete_item(self):
        index = self.listView.currentIndex()
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        reply = QMessageBox.question(
            self, "Delete", f"Are you sure you want to delete '{file_path}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                self.refresh_views()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete item:\n{e}")

    def refresh_views(self):
        self.dir_model.refresh()
        self.file_model.refresh()
        self.statusbar.showMessage("Views refreshed", 2000)

    def open_context_menu(self, position):
        index = self.listView.indexAt(position)
        if not index.isValid():
            return
        menu = QMenu()
        open_action = menu.addAction("Open")
        delete_action = menu.addAction("Delete")
        rename_action = menu.addAction("Rename")
        permissions_action = menu.addAction("Permissions")
        action = menu.exec_(self.listView.mapToGlobal(position))
        if action == open_action:
            self.on_file_double_clicked(index)
        elif action == delete_action:
            self.delete_item()
        elif action == rename_action:
            self.rename_item(index)
        elif action == permissions_action:
            self.manage_permissions(index)

    def rename_item(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        new_name, ok = QInputDialog.getText(self, "Rename", "New Name:")
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            try:
                os.rename(file_path, new_path)
                self.refresh_views()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename item:\n{e}")

    def search_files(self):
        search_query = self.searchLineEdit.text().lower()
        root_index = self.listView.rootIndex()
        for i in range(self.file_model.rowCount(root_index)):
            index = self.file_model.index(i, 0, root_index)
            file_name = self.file_model.fileName(index).lower()
            self.listView.setRowHidden(i, root_index, search_query not in file_name)

    def manage_permissions(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        permissions = oct(os.stat(file_path).st_mode)[-3:]
        new_permissions, ok = QInputDialog.getText(
            self, "Permissions", f"Current permissions: {permissions}\nEnter new permissions (e.g., 755):"
        )
        if ok and new_permissions:
            try:
                os.chmod(file_path, int(new_permissions, 8))
                QMessageBox.information(self, "Success", "Permissions updated successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not change permissions:\n{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec_())
