
Lerchbacher Bücherdatenbank
============================
![Sprache: Python](https://img.shields.io/badge/Sprache-Python-blue)
![UI Bibliothek: Tkinter](https://img.shields.io/badge/UI_Bibliothek-customkinter-blue)
![Datenbanksystem: SQLite3](https://img.shields.io/badge/Datenbanksystem-SQLite3-lightblue)
![Codezeilen: Über 2000](https://img.shields.io/badge/Zeilen_Code-%C3%9Cber_2000-green)

## Über dieses Projekt
Dies ist ein Bücherverwaltungssystem, welche in zwei große Teile aufgespalten ist: die Desktop Applikation und die Website.

Ich mache dieses Projekt hauptsächlich für meine Familie, allerdings werde ich dieses Repo veröffentlichen, um es anderen Menschen zugänglich zu machen.
Feature-Requests werden nur von meiner Familie und Freunden akzeptiert. 


Ausser Fehlerbehebungen werden wahrscheinlich kaum Updates veröffentlicht werden (dachte ich zumindest, meine Familie hat sich bisher eine MENGE Änderungen gewünscht), da ich auch an anderen Projekten arbeite, und das auch nur in meiner Freizeit.

Alle Fehler oder mögliche Sicherheitslücken können über Github Issues gemeldet werden, wofür ich sehr dankbar wäre.

Es ist auch möglich, dass dieses Projekt umschriebene Umlaute (ae, ue, oe) enthält, da ich normalerweise das US Tastaturlayout benutze und nicht immer zum deutschen wechseln kann und will.


**Bitte seid so nett und ignoriert meinen fürchterlichen Code-Stil in diesem Projekt. Einige Teile sind schon sehr alt. Damals wusste ich noch nichts über
die Konventionen für sauberen Code... Ich versuche immer wieder, Code-Teile auszubessern, wenn mir diese besonders stark aufallen.**


### Die Desktop Applikation
Die Desktop Applikation ist der Kern des Systems, mit seiner Hilfe werden Bücher und Autoren verwaltet. Sie beinhaltet ebenfalls eine Suchfunktion.

Alle Änderungen werden automatisch nach dem abschliessen der Aktion (Erstellen, Bearbeiten, Löschen) gespeichert.

Die Desktop Applikation kann für Einzelanwender ohne die Website Version oder einen Server genutzt werden, da die Datenbank nur eine lokale Datei ist. Bei mehreren
Nutzern empfiehlt es sich, die Applikation samt Dateien und Ordnern in einen Netzwerk-/Cloudordner zu verschieben, da die Datenbank somit für alle Nutzer synchron bleibt.


### Die Website
**DIE WEBSITE IST IN EINEM NICHT FERTIGEN ZUSTAND UND KANN NICHT VERWENDET WERDEN! BITTE IGNORIEREN SIE SIE!**
Daran werde ich später einmal arbeiten, im Moment aber nicht.

Die Website ist eine Möglichkeit, die Datenbank auch auf Geräten, auf denen die Desktop Applikation nicht installiert ist (Handys, Tablets, etc.), zu durchsuchen.

Die Vorraussetzung dafür ist allerdings, das sich das Gerät im selben Netzwerk wie der Website Server befindet.

Die Website enthält KEINE Möglichkeiten zur Erstellung, Bearbeitung oder Löschung von Daten.


## Lizenz
Dieses Projekt und alle enthaltenen Dateien, ausgenommen der Dateien im docs Verzeichnis und allen seinen Subverzeichnissen, werden unter der GNU AGPL-v3 zur Verfügung gestellt.
Genauere Infos finden sich an den Anfängen der Quellcode-Dateien und ebenfalls in der LICENSE Datei.

Die Dokumentation, inklusive aller HTML, CSS und Javascript Dateien im docs Verzeichnis und allen seinen Subverzeichissen, wird unter der
Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) zur Verfügung gestellt.


## Organisation
Ja, dieses Repo ist leider nicht sehr gut organisiert. Ich versuche es zu verbessern, aber es ist inzwischen sehr groß geworden.
Ich weiß nicht wieso, aber ich habe zuerst gelernt, Pull-Requests zu verwenden und erst später, wie man Merges mit der git CLI macht. Ich werde ab Version 1.2.1 wahrscheinlich auf letzteres umsteigen.

Und bitte ignoriert meinen fürchterlichen Commit Stil in den Anfängen des Projekts. Dieses Repo ist eines meiner ersten überhaupt. Damals wusste ich nicht wirklich, wie man Commits beyeichnen soll. Die (meisten) Infos zu den Änderungen dieser Commits finden sich in der Datei Changelog.md, welche nur in älteren Versionen existiert. Später habe ich das dann geändert und normale Commit-Messages verwendet.
