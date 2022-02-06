import QtQuick 2.12

import QtQuick.Window 2.12
import QtQuick.Controls 2.12


Window {
    width: 640
    height: 480

    Label {
        id: label
        x: 48
        y: 61
        text: qsTr("Threads : ")
        font.pointSize: 12
    }

    CheckBox {
        id: autothreadscheckbox
        x: 48
        y: 15
        text: qsTr("Threads Auto")
        display: AbstractButton.TextOnly
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.1}D{i:1}D{i:2}
}
##^##*/
