# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

What parts of the Qt framework to use?
--------------------------------------

Summary:

* Either use the new version 2 QtQuick + QML available in Qt 5.
    * This is what Andy Nichols recommends.
* Or use the old QWidgets, QGraphicsView, etc. from Qt 4.
    * This is what pyqtgraph, picasso, cadnano, and labelimg all uses.






Refs:

* https://www.qt.io/blog/2017/01/19/should-you-be-using-qgraphicsview
* https://www.youtube.com/watch?time_continue=45&v=TOqvODKULhw
    * Goes over the different GUI technologies in the Qt framework, and the many options
      for creating widgets - QWidgets, QGraphicsView, QtQuick (1/2), etc.
    * Strongly recommends using the new QtQuick2 introduced with Qt5.
        * Don't use QtQuick1 (from Qt4).
        * Use either QtQuickControl1 or QtQuickControl2 instead of QWidgets.
        * QtQuickControl2 - custom C++, particularly for embedded and mobile platforms.
    * If using any web/HTML, use QtWebEngine.
* https://www.riverbankcomputing.com/static/Docs/PyQt5/qml.html


What parts of Qt does other libraries use?

* https://github.com/pyqtgraph/pyqtgraph
    * Uses the old QtGui.QWidget.

* https://github.com/cadnano/cadnano2.5
    * Uses QMainWindow and QWidgets (in `mainwindow.ui`).
    * Creates a CNGraphicsView, which extends from QGraphicsView for slice/path/grid
        (cadnano.views.cngraphicsview.h)

* https://github.com/jungmannlab/picasso
    * picasso.localize uses `QtWidgets.QGraphicsView` for the central `localize` view widget,
        QtWidgets.QGraphicsScene to display individual frames, and
        QtWidgets.QMainWindow for the main window.
    * picasso.render uses `QtWidgets.QMainWindow` for main window and
        QtWidgets.QLabel for the view, apparently?


Other interesting Qt-dev tools:

python-qt-live-coding:
* https://github.com/machinekoder/python-qt-live-coding
* https://machinekoder.com/speed-up-your-gui-development-with-python-qt-and-qml-live-coding/
* pip install python-qt-live-coding
*


Examples:

* https://www.qt.io/blog/2018/05/14/qml-qt-python
    * Uses `view.setSource(QUrl.fromLocalFile(qmlFile))` to load qml in view.
* https://github.com/pyqtgraph/pyqtgraph/blob/3d3d0a24590a59097b6906d34b7a43d54305368d/doc/source/qtcrashcourse.rst
* https://www.riverbankcomputing.com/static/Docs/PyQt5/qml.html
    * qmlRegisterType(Person, ...)
    * engine = QQmlEngine() # Create a QML engine.
    * component = QQmlComponent(engine)  # Create a component factory
    * component.loadUrl(QUrl('example.qml'))  #  and load the QML script.
    * Also: `pyqt5qmlplugin`, `qmlscene`, and `QQmlExtensionPlugin`.
* https://codeloop.org/pyqt5-qml-model-view-programming/
* https://github.com/seanwu1105/pyqt5-qtquick2-example - QtQuick2 examples with PyQt5.
    engine = QQmlApplicationEngine()
    engine.load(QUrl('qrc:/pyqt5_qtquick2_example/qml/main.qml'))



"""





