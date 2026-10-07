import QtQuick 2.0
import calamares.slideshow 1.0

Presentation
{
    id: presentation

    Timer {
        interval: 12000
        repeat: true
        running: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#11111b"

            Image {
                id: logo
                source: "markos-orbit.svg"
                width: 210
                height: 210
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 18
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: logo.bottom
                anchors.topMargin: 8

                text: qsTr("Welcome to MarkOS")

                color: "#ffffff"
                font.pixelSize: 27
                font.bold: true
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: logo.bottom
                anchors.topMargin: 50

                width: 560

                text: qsTr(
                    "A modern Debian-based Linux experience, "
                    + "designed for everyday life."
                )

                color: "#cdd6f4"
                font.pixelSize: 15

                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#11111b"

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 75

                text: qsTr("Make MarkOS yours")

                color: "#cba6f7"
                font.pixelSize: 27
                font.bold: true
            }

            Text {
                anchors.centerIn: parent
                width: 570

                text: qsTr(
                    "Cosmic. Midnight. Aurora. Dawn.<br/><br/>"
                    + "Choose a complete appearance preset and MarkOS "
                    + "adapts the wallpaper, colours, icons and terminal "
                    + "to match your style."
                )

                color: "#cdd6f4"
                font.pixelSize: 16

                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#11111b"

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 75

                text: qsTr("Ready from the first boot")

                color: "#74c7ec"
                font.pixelSize: 27
                font.bold: true
            }

            Text {
                anchors.centerIn: parent
                width: 570

                text: qsTr(
                    "GNOME, Flatpak, LibreOffice, gaming tools, "
                    + "a polished terminal and useful desktop features "
                    + "are ready when you are.<br/><br/>"
                    + "Built for a brighter tomorrow."
                )

                color: "#cdd6f4"
                font.pixelSize: 16

                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
