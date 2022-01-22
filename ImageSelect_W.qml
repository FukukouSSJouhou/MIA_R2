import QtQuick 2.12
import QtQuick.Controls 2.12

Row {
    width: 160
    height: 100

    CheckBox {
        id: checkBox22
        height: 100
        text: ""
    }

    Image {
        id: image
        width: 100
        height: 100
        source: "qrc:/qtquickplugin/images/template_image.png"
        fillMode: Image.PreserveAspectFit
    }
}
