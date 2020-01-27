Uniwersytet im. Jana Długosza w Częstochowie
############################################

=================
Praca Inżynierska
=================

Temat: Edytor do nauki programowania w języku Python
****************************************************

Imię i nazwisko autora: Maciej Pawłowski
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Kierunek studiów: Informatyka
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specjalizacja: Inżynieria Oprogramowania
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Opiekun pracy: dr. Lidia Stępień
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Częstochowa, rok adaem. 2019/2020

Spis treści
===========

#. **Wstęp**

#. **Cel i założenia projektu**
    #. Wymagania sprzętowe
    #. Wymagania funkcjonalne
    #. Podstawy użytkowania
#. **Implementacja**
    #. Opis aplikacji
    #. Edytor PyEnlightmentCode
    #. Kolorowanie składni
    #. Narzędzia debugujące
#. **Testy**
    #. Testy wyrażeń regularnych
    #. Testy zarządzania plikami

#. **Podstumowanie**

#. **Bibliografia i literatura**

1. Wstęp
########

Rozwój i popularyzacja komputerów sprawiły że niemalże w każdej dziedzinie odpowiednie maszyny są w stanie zastąpić człowieka dopóki zadane zagadnienie jest problemem przeliczalnym.
Ponadto czas pracy maszyny jest o wiele tańszy niż czas pracy programisty który raz wykonując swoją pracę, może zaoszczędzić setki a nawet tysiące godzin pracy ludzkiej.

Jest to o tyle popularną praktyką aby część pracy ludzkiej przenosić na maszyny, że niektóre firmy specjalizują się wyłącznie w tym kierunku. Potrzeba programistów na rynku wciąż rośnie proporcjonalnie do rozmiarów aplikacji które posiadają coraz większe funkcjonalności.

Aby wykształcić nowych programistów istnieje wiele metod mniej lub bardziej skutecznych. Natomiast dobry programista powinien bezbłednie rozumieć podstawy programowania, potrafić zdebugować kod rozumiejąc co się dzieje na każdym kroku, znaleźć błąd i go naprawić. W tym celu powstał PyEnlightenmentCode (dalej PEC) który skupia się na dostarczeniu narzędzi ułatwiających naukę dla nowych programistów.

1.1 Wymagania sprzętowe
#######################

PyEnlightenmentCode do działania w pełni poprawnie wymaga:

* Środowiska z rodziny systemów Unix 64 bit (Linux)
* Klawiatury, Myszy oraz monitora
* Przeglądarkę internetową wspieraną przez pythontutor.com
* Połączenie z internetem
* Python3 (Interpreter)
* pip3 (Installer pakietów)
* pdb (Debugger)

1.2 Wymagania funkcjonalne
##########################

PyEnlightenmentCode (dalej PEC) spełnia poniżej wymienione wymagania funkcjonalne:

* Edytor tekstu.

Edytor tekstu zawiera w sobie mechanizm kolorujący składnię języka programowania Python z użyciem wyrażeń regularnych.

* Menadżer plików.

PEC umożliwia otwarcie wielu plików, przełączanie się pomiędzy nimi, zapis pojedyńczego pliku, zapis wielu plików, nadpisanie pliku, wczytanie pliku, stworzenie nowego pliku.

* Konsola informująca.

PEC posiada dolny panel który informuje użytkownika o czynnościach które podjął, ostrzeżeniach o potencjalnym niepoprawnym użytkowaniu programu, błędach dla podjętych czynności.

* Narzędzia debugujące.

PEC daje kilka możliwości które mają na celu ułatwienie zrozumienia kodu dla potencjalnego przyszłego programisty. Są one dostępne dla każdego pliku z osobna w zakładce Tools:

Otworzenie zewnętrznego portalu pythontutor.com w domyślnej przeglądarce przekazując kod w postaci url. Portal umożliwia prześledzenie wykonywania programów do 999 kroków z wizualizacją wartości zmiennych.

Sprawdzenie kodu lokalnie pod względem błędów składniowych, takich jak: SyntaxError, NameError i RuntimeError

Zapisanie kodu w pliku tymczasowym i uruchomienie debuggera, plik tymczasowy po zakońćzeniu działania debuggera zostanie usunięty.

Zapisanie kodu w pliku tymczasowym i uruchomienie go.

* Zapisywanie konfiguracji.

Gdy edytor zostanie zamknięty poprawnie, zostanie zapisana lokalizacja i umiejscowienie okna, jeśli krawędź programu miałaby na skutek błędu z rodzielczością znaleźć się poza zasięgiem myszy, program powinien przy ponownym uruchomieniu zostać przyciągnięty do krawędzi ekranu i ewentualnie zmniejszony do rozmiaru ekranu jeśli ten byłby większy niż rozdzielczość ekranu.

* Pasek menu

Pasek menu umożliwia zarządzanie plikami jak wyżej wymieniono.

1.3 Podstawy użytkowania
########################

Aby skorzystać z edytora wystarczy uruchomić dostarczony plik binarny. Zalecane jednak jest umieścić plik binarny w lokalizacji /usr/bin z uprawnieniami do wykonywania przez aktualnego użytkownika. Wtedy staje się dostępny z poziomu konsoli i potencjalnych dowiązań (ikon szybkiego dostępu / skrótów). 

2. Implementacja
################

Do implementacji zostały wykorzystane następujące pakiety:

* tkinter
* ttk
* ttkthemes
* typing
* logging
* os
* sys
* subprocess
* threading
* json
* webbrowser
* urllib
* tempfile

Wszystkie są dostępne w standardowej biblitece pythona, bądź w ramach pakietów dostępnych porzez pip3.

Na implementację PyEnlightenmentCode składa się wiele klas, które zapewniają strukturyzację kodu:

* **MainWindow:** Wzorzec Singleton i Obserwator

    `'PyEnligtenmentCode/main_frame.py'`

Trzon aplikacji odpowiadający za stworzenie głównego okna i zarządzanie poszczególnymi menadżerami które zostaną wypisane poniżej.

* **MainFrameErrorCatcher:** Menadżer błędów

    `'PyEnligtenmentCode/main_frame.py'`

Opakowanie (ang. Wrapper) przechwytywanych błędów i przekierowanie ich do konsoli informującej użytkownika o błędach w trakcie wykonywania programu, przekazuje je do modułu logging który jest singletonem dostępnym z każdego miejsca w programie.

* **Default:** Menadżer konfiguracji

    `'PyEnligtenmentCode/defaults/tkhelper.py'`

Jest to struktura słownikowa która zawiera całą informację o konfiguracji PEC. Umożliwia odczytanie i zapis konfiguracji do pliku `'~/.config/PyEnlightmentCode/config.json'` oraz zmianę parametrów. 

* **MenuBar:** Menadżer paska menu, górny panel.

    `'PyEnligtenmentCode/components/menu_frame.py'`

Menadżer konfiguruje menu i komendy przypisane pod konkretne opcje z rozwijanego menu, komunikując MenuBar z MainWindow.

* **BottomPanel:** Menadżer konsoli informującej, dolny panel.

    `'PyEnligtenmentCode/components/bottom_frame.py'`

Menadżer konfiguruje lokalizację klasy `'TextHandler'` i przypisuje modułowi logging jako miejsce wyświetlania komunikatów dla użytkownika.

    * **TextHandler:** Widżet konsoli informacyjnej

        `'PyEnligtenmentCode/components/bottom_frame.py'`

    Wczytuje z Default kolor komunikatów zależny od poziomu komunikatu, wyróżnia się tutaj 6 typów komunikatów, kolejno:
    `"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"`

        * Critical - uniemożliwia dalsze działanie aplikacji.
        * Error - podczas wykonywania instrukcji edytor napotkał błąd i nie może jej wykonać.
        * Warning - ostrzeżenie przed wykonaniem czynności która może odnieść nieoczekiwany skutek.
        * Info - informacja dla użytkownika.
        * Debug - domyślnie nie wyświetlane dla użytkownika, ma za zadanie przekazać pełną informację co się dzieje w programie, są to komunikaty typowo dla developera.
        * Notset - domyślnie nie wyświetlane dla użytkownika i developera. Zawiera komunikaty bezpośrednio z samego modułu logging.

    Przed emisją komunikatu oznacza wiadomość odpowiednim tagiem pozwalając na zastosowanie odpowiedniego koloru dla danego poziomu komunikatu. Konkretne ustawienie poziomu modułu `'logging'` zawiera wszystkie wyższego poziomu, domyślne ustawienie dla użytkownika to `'INFO'` które zawiera również powyższe dla niego: `'Critical', 'Error' i 'Warning'`

* **EditorManager:** Menadżer plików.

    `'PyEnligtenmentCode/components/file_frame.py'`

Umożliwia zarządzanie plikami, przełączanie się pomiędzy nimi, wytypowanie aktywnego pliku do kolorowania składni. Plikami zarządza z pomocą Menadżera pliku `'FileContent'`.

    * **FileContent:** Menadżer pliku.

        `'PyEnligtenmentCode/components/file_frame.py'`

    Przechowuje informacje o pliku takie jak nazwa i ścieżka, tworzy zakładki dla widżetów `'ProgrammingText'` oraz `'ExecutionTools'`. Przy wyświetlaniu (Na przykład przy zmianie z innego pliku na ten) konkretnego pliku oznacza jego treść do kolorowania składni.












