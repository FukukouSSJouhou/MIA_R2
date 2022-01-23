import QtQuick 2.12

import QtQuick.Window 2.12
import QtQuick.Controls 2.12

Window  {
    width: 640
    height: 480
    property url imagesourcekun;
    Image {
        id: imageGraphkun
        x: 0
        y: 0
        source: imagesourcekun
        fillMode: Image.PreserveAspectFit
    }
}
