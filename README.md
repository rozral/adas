# Gala projekts priekšmetā Adaptīvas datu apstrādes sistēmas(1),24/25-P
Atbilstoši semestra laikā izveidotajiem praktiskajiem darbiem, izveidots prototips programmatūrai veikala pasūtījumu apstrādei. Izveidotā programmā sniedz iespēju pievienot produktus datubāzei jeb noliktavai un veikt pasūtījumus, izvēloties produktus no datubāzes.

Izveidojot produktu, produktam tiek piešķirts unikāls ID, kas tiek izmantots kā produkta primārā atslēgā. Lai izveidotu produktu, nepieciešams arī norādīt tā atlikumu noliktavā un cenu. Produktu izveidošanas funkcionalitāte ir pamatā izveidota, lai demonstrētu pasūtījumu izveidošanu.

Izveidojot pasūtījumu, ja produkta ID atbilst kādam produktam noliktavā, tiek automātiski aizpildīts produkta nosaukums. Ir iespējams arī izvēlēties produktu no saraksta, pēc tā nosaukuma – šajā gadījumā, pēc produkta izvēles, produkta ID tiek automātiski aizpildīts. Ir iespējams pievienot vairākus produktu vienam pasūtījumam, izmantojot “+ Rinda” pogu, kas pievieno jaunu produkta rindu. Produktu izvēles procesā dati tiek dinamiski pārbaudīti un tiek izvadīti kļūdas paziņojumi, ja kādi no datiem nav atbilstoši (piem. neeksistējošs produkta ID). Ja visi dati ir atbilstoši, tiek aktivizēta “Nosūtīt pasūtījumu” poga un pēc tās nosūtīšanas izvadīts paziņojums par veiksmīgu pasūtījuma nosūtīšanu – “Pasūtījums #[pasūtījuma nr] pieņemts! (€[pasūtījuma summa])”


## Programmas palaišanas instrukcija
1. Darba vides sagatavošana - nepieciešams sistēmā uzstādīt Python, pip un citu programmatūru, kas nepieciešama Python koda palaišanai
2. Jāinstalē visas [requirements.txt](requirements.txt) failā esošās programmatūras atkarības (dependencies), šo var veikt izveidojot virtuālo vidi vai izmantojot komandu `pip install -r requirements.txt`
3. Komandrindā jāizvēlas projekta mape un jāizmanto komanda `fastapi dev main.py`, lai palaistu programmas API
4. Jāatver [index.html](index.html) fails sev vēlamā pārlukprogrammā