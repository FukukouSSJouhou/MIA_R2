import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12

Window {
    width: 640
    height: 480
    title: "aa"
    id:windowkun
    signal savedconfig(bool checkedobj,int datanums)
    Label {
        id: label
        x: 48
        y: 61
        text: qsTr("Threads : ")
        font.pointSize: 12
    }

    property bool enabledautothreads;
    CheckBox {
        id: autothreadscheckbox
        x: 48
        y: 15
        text: qsTr("Threads Auto")
        display: AbstractButton.TextOnly
        //checked: enabledautothreads
    }

    Button {
        id: savebutton
        x: 472
        y: 394
        text: qsTr("Save")
        onClicked: {
            savedconfig(autothreadscheckbox.checked,0)
            windowkun.close()
        }
    }

    Button {
        id: closebutton
        x: 65
        y: 394
        text: qsTr("Close")
        onClicked: {
            windowkun.close()
        }
    }
}


