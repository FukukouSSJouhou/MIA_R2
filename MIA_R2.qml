import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.3
Window {
    property variant subwingengraphsingle;
    width: 640
    height: 480
    id:root
    visible: true
    title: qsTr("MIA R2")
    Component.onCompleted: {
        function onLoad(){
            mainwinconnect.logging_addsignal.connect(
                function logAdd(strkun){
                    textArea_logging.insert(textArea_logging.length,strkun + "<br>")
                    mainwinconnect.print_stdout(strkun)
                }
            );
            mainwinconnect.logging_ansi_addsignal.connect(
                function logAdd(strkun){
                    textArea_logging.insert(textArea_logging.length,strkun + "<br>")
                }
            );
            mainwinconnect.gengraph_dialog_errkunsignal.connect(
                function dialogshowkun(strkun){
                    gengraph_errdialog.open()
                }

            );
            mainwinconnect.show_picture_graph1.connect(
                function dialogpict(strkun,titlekun){

                    var picture_path=strkun
                    var component = Qt.createComponent("SubWindow_FaceOnlyGraphShow.qml")
                    subwingengraphsingle    = component.createObject(root)
                    subwingengraphsingle.imagesourcekun=picture_path
                    subwingengraphsingle.title=titlekun
                    subwingengraphsingle.show()
                }

            );
        }
        onLoad();
    }
    MessageDialog {
        id:gengraph_errdialog
        title:qsTr("Error")
        text:qsTr("Please Run Process first")
        onAccepted:{
            gengraph_errdialog.close()
        }
        icon: StandardIcon.Critical
        standardButtons: StandardButton.OK
    }
    MessageDialog {
        id:beforerunpc_errdialog
        title:qsTr("Error")
        text:qsTr("Please Set File Path and length")
        onAccepted:{
            beforerunpc_errdialog.close()
        }
        icon: StandardIcon.Critical
        standardButtons: StandardButton.OK
    }

    Button {
        id: startbutton
        x: 362
        y: 262
        text: qsTr("Start")
        onClicked: {
            if(videopathtextField.text == ""){
                beforerunpc_errdialog.open()
                return;
            }
            if(videolengthtextField.text == ""){
                beforerunpc_errdialog.open()
                return;
            }

            mainwinconnect.running_syori_clicked(videopathtextField.text,videolengthtextField.text,checkBoxsent.checked)
        }
    }
    FileDialog{
        id: videoOpenFileDialog
        title: qsTr("Please choose video file")
        nameFilters: ["Movie Files (*.mp4 *.mkv *.m2ts *.webm)"]
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
                textFormat: Text.RichText
                placeholderText: qsTr("")
                readOnly: true
            }
    }
    Button {
        id: gengraphbutton
        x: 158
        y: 262
        text: qsTr("GenGraph")
        onClicked: {
            mainwinconnect.genGraph_Clicked()
        }
    }

    CheckBox {
        id: checkBoxsent
        x: 201
        y: 127
        text: qsTr("Sentence")
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}D{i:1}D{i:2}D{i:3}D{i:4}D{i:5}D{i:6}D{i:7}D{i:8}D{i:9}D{i:12}
D{i:11}D{i:13}D{i:14}
}
##^##*/
