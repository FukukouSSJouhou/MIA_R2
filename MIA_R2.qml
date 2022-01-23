import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.3
Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("MIA R2")
    Component.onCompleted: {
        function onLoad(){
            mainwinconnect.logging_addsignal.connect(
                function logAdd(strkun){
                    textArea_logging.insert(textArea_logging.length,strkun + "\n")
                    mainwinconnect.print_stdout(strkun)
                }
            );
        }
        onLoad();
    }

    Button {
        id: startbutton
        x: 362
        y: 262
        text: qsTr("Start")
        onClicked: {
            mainwinconnect.running_syori_clicked(videopathtextField.text,videolengthtextField.text)
        }
    }
    FileDialog{
        id: videoOpenFileDialog
        title: qsTr("Please choose video file")
        nameFilters: ["Movie Files (*.mp4 *.mkv *.m2ts)"]
        selectFolder: false
        onAccepted:{
            //videopathtextField.text=videoOpenFileDialog.fileUrl.toLocaleString()
            videopathtextField.text=mainwinconnect.videoFilePathSet(videoOpenFileDialog.fileUrl)
            videoOpenFileDialog.close()
        }

    }

    Label {
        id: labelvfile
        x: 8
        y: 23
        text: qsTr("Video File:")
        font.pointSize: 9
    }
    TextField {
        id: videopathtextField
        x: 90
        y: 11
        width: 491
        height: 40
        placeholderText: qsTr("Video Path")
    }

    Button {
        id: videopathbutton
        x: 587
        y: 11
        width: 43
        height: 40
        text: qsTr("...")
        onClicked: videoOpenFileDialog.open()
    }

    Label {
        id: labelnumvideo
        x: 41
        y: 67
        text: qsTr("length")
    }

    TextField {
        id: videolengthtextField
        x: 90
        y: 57
        placeholderText: qsTr("Text Field")
        validator: DoubleValidator{
            bottom:0
        }
        text:"1"
    }
    ScrollView {
        id:logging_scrollview
        x: 1
        y: 328
        width: 629
        height: 145
            TextArea {
                id: textArea_logging
                text:""
                wrapMode: Text.Wrap
                textFormat: Text.AutoText
                placeholderText: qsTr("")
                readOnly: true
            }
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.25}D{i:1}D{i:2}D{i:3}D{i:4}D{i:5}D{i:6}D{i:7}D{i:10}D{i:9}
}
##^##*/
