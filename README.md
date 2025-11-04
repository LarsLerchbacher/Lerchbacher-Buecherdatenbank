
Lerchbacher Bücherdatenbank
============================

## Ueber dieses Projekt
Dies ist ein Bücherverwaltungssystem, welche in zwei grosse Teile aufgespalten ist: die Desktop Applikation und die Website.

Ich mache dieses Projekt hauptsächlich für meine Familie, allerdings werde ich dieses Repo veröffentlichen, um es anderen Menschen zugänglich zu machen.
Feature-Requests werden nur von meiner Familie und Freunden akzeptiert. 


Ein öffentlicher Release als kompilierte Version (.exe Datei) ist nicht möglich, da das Projekt in seiner Abhängigkeitskette einige Packages/Module/Bibliotheken unter nicht mit der AGPL kompatiblen Linzenzen hat. Beim kompilieren würden diese miteingebaut werden. Da ich diese aber nicht verteilen darf, muss ich leider darauf verzichten.


Ausser Fehlerbehebungen werden wahrscheinlich kaum Updates veröffentlicht werden, da ich auch an anderen Projekten arbeite, und das auch nur in meiner Freizeit.

Alle Fehler oder mögliche Sicherheitslücken können über Github Issues gemeldet werden, wofür ich sehr dankbar wäre wenn diese gemeldet werden.

Es ist auch möglich, dass dieses Projekt umschriebene Umlaute (ae, ue, oe) enthält, da ich normalerweise das US Tastaturlayout benutze und nicht immer zum deutschen wechseln kann und will.


**Bitte seid so nett und ignoriert meinen fürchterlichen Code-Stil in diesem Projekt. Einige Teile sind schon sehr alt. Damals wusste ich noch nichts über
die Konventionen für sauberen Code... Ich habe versucht, den Code vor dem Release möglichst gut auszubessern und besser zu strukturieren (nur Desktop Version).**


### Die Desktop Applikation
Die Desktop Applikation ist der Kern des Systems, mit seiner Hilfe werden Bücher und Autoren verwaltet. Sie beinhaltet ebenfalls eine Suchfunktion.

Alle Aenderungen werden automatisch nach dem abschliessen der Aktion (Erstellen, Bearbeiten, Löschen) gespeichert.

Die Desktop Applikation kann für einzelanwender ohne die Website Version oder einen Server genutzt werden, da die Datenbank nur eine lokale Datei ist. Bei mehreren
Nutzern empfiehlt es sich, die Applikation samt Dateien und Ordnern in einen Netzwerk-/Cloudordner zu verschieben, da die Datenbank somit für alle Nutzer synchron bleibt.


### Die Website
**DIE WEBSITE IST IN EINEM NICHT FERTIGEN ZUSTAND UND KANN NICHT VERWENDET WERDEN! BITTE IGNORIEREN SIE SIE!**
Daran werde ich später einmal arbeiten, im Moment aber nicht.

Die Website ist eine Möglichkeit, die Datenbank auch auf Geräten, auf denen die Desktop Applikation nicht installiert ist (Handys, Tablets, etc.), zu durchsuchen.

Die Vorraussetzung dafür ist allerdings, das sich das Gerät im selben Netzwerk wie der Website Server befindet.

Die Website enthält KEINE Möglichkeiten zur Erstellung, Bearbeitung oder Löschung von Daten.


## Lizenz
Dieses Projekt und alle enthaltenen Dateien werden unter der GNU AGPL-v3 zur Verfügung gestellt.
Genaüre Infos finden sich an den Anfängen der Qüllcode-Dateien und ebenfalls in der LICENSE Datei.


## Organisation
Ja, ich weiss. Dieses Repo ist nicht sehr gut organisiert. Ich habe nur einen einzigen Branch für alle Commits.

Das hat den Grund, dass dies eines der ersten meiner Git Repos überhaupt ist. Inzwischen habe ich auch gelernt, wie man Branches und PRs verwendet.

Dieses Repo umzustrukturieren wäre allerdings sehr aufwendig gewesen, und das Verschieben von Commits in andere Branches führt bei mir meistens immer noch zu Chaos. Daher werde ich es einfach so 
weiterführen wie bisher.

Und bitte ignoriert meinen fürchterlichen Commit Stil in den Anfängen des Projekts. Die (meisten) Infos zu den Aenderungen dieser Commits finden sich in der Datei Changelog.md, welche nur in älteren Versionen existiert.

