import json

EXPLANATIONS = {
    1: {
        "it": "Regola orizzontale: il numero di punti aumenta di 1 da sinistra a destra (1→2→3, 2→3→4, 3→4→5). Regola verticale: il numero aumenta di 1 dall'alto in basso. Nella casella mancante servono esattamente 5 punti.",
        "en": "Horizontal rule: the number of dots increases by 1 from left to right (1→2→3, 2→3→4, 3→4→5). Vertical rule: increases by 1 top-to-bottom. The target cell requires exactly 5 dots in a quincunx pattern.",
        "de": "Horizontale Regel: Die Punktanzahl steigt von links nach rechts um 1 (1→2→3, 2→3→4, 3→4→5). Vertikal ebenfalls +1. Im Zielfeld werden exakt 5 Punkte benötigt.",
        "es": "Regla horizontal: el número de puntos aumenta en 1 de izquierda a derecha (1→2→3, 2→3→4, 3→4→5). Regla vertical: aumenta en 1 de arriba hacia abajo. Faltan exactamente 5 puntos.",
        "pt": "Regra horizontal: o número de pontos aumenta em 1 da esquerda para a direita (1→2→3, 2→3→4, 3→4→5). Regra vertical: aumenta em 1 de cima para baixo. A casa requer 5 pontos.",
        "fr": "Règle horizontale : le nombre de points augmente de 1 de gauche à droite (1→2→3, 2→3→4, 3→4→5). Règle verticale : augmente de 1 de haut en bas. Il faut exactement 5 points."
    },
    2: {
        "it": "Regola orizzontale: lo stato di riempimento evolve da Vuoto → Semipieno (sinistra) → Completamente pieno. Regola verticale: la forma geometrica rimane costante per riga (Cerchio, Quadrato, Triangolo). Manca il Triangolo pieno.",
        "en": "Horizontal rule: fill state transitions from Empty → Half-filled (left) → Solid full. Vertical rule: outer geometry is constant per row (Circle, Square, Triangle). The target is a fully solid Triangle.",
        "de": "Horizontale Regel: Füllung wechselt von Leer → Halbvoll → Voll ausgefüllt. Vertikal bleibt die Grundform gleich (Kreis, Quadrat, Dreieck). Es fehlt das vollflächig gefüllte Dreieck.",
        "es": "Regla horizontal: el llenado evoluciona de Vacío → Semilleno → Completamente lleno. Regla vertical: la figura se conserva por fila (Círculo, Cuadrado, Triángulo). Falta el Triángulo lleno.",
        "pt": "Regra horizontal: o preenchimento evolui de Vazio → Metade → Totalmente preenchido. Regra vertical: a forma geométrica é constante por linha. Falta o Triângulo preenchido.",
        "fr": "Règle horizontale : l'état de remplissage évolue de Vide → Semi-rempli → Plein. Règle verticale : la forme est constante par ligne (Cercle, Carré, Triangle). Il manque le Triangle plein."
    },
    3: {
        "it": "Regola orizzontale: la freccia ruota in senso orario di 90° ad ogni casella (0°→90°→180°, 90°→180°→270°, 180°→270°→0°). Dopo aver puntato a sinistra (270°), la freccia punta verso l'alto (0°).",
        "en": "Horizontal rule: the arrow rotates 90° clockwise at each step (0°→90°→180°, 90°→180°→270°, 180°→270°→0°). Rotating 90° CW from left (270°) results in pointing straight Up (0°).",
        "de": "Horizontale Regel: Der Pfeil rotiert schrittweise um 90° im Uhrzeigersinn. Nach der Ausrichtung nach links (270°) zeigt der Pfeil wieder nach oben (0°).",
        "es": "Regla horizontal: la flecha rota 90° en sentido horario por casilla. Tras apuntar hacia la izquierda (270°), la rotación la sitúa apuntando hacia arriba (0°).",
        "pt": "Regra horizontal: a seta gira 90° no sentido horário a cada passo. Após apontar para a esquerda (270°), volta a apontar para cima (0°).",
        "fr": "Règle horizontale : la flèche tourne de 90° dans le sens horaire. Après avoir pointé vers la gauche (270°), elle pointe vers le haut (0°)."
    },
    4: {
        "it": "Regola orizzontale: il numero di segmenti/lati/raggi aumenta di 1 (3→4→5). Riga 1: poligoni a 3, 4, 5 lati; Riga 2: 3, 4, 5 linee parallele; Riga 3: cerchio con 3 raggi, 4 raggi, quindi cerchio con 5 raggi.",
        "en": "Horizontal rule: number of segments/sides/spokes increases by 1 (3→4→5). Row 1: 3, 4, 5 sides; Row 2: 3, 4, 5 lines; Row 3: circle with 3 spokes, 4 spokes, thus 5 spokes.",
        "de": "Horizontale Regel: Anzahl der Elemente/Seiten steigt um 1 (3→4→5). Zeile 1: 3-, 4-, 5-Eck; Zeile 2: 3, 4, 5 Linien; Zeile 3: Kreis mit 3, 4, also 5 Speichen.",
        "es": "Regla horizontal: el número de lados o radios aumenta en 1 (3→4→5). Fila 1: polígonos de 3, 4, 5 lados; Fila 3: círculo con 3, 4 y finalmente 5 radios.",
        "pt": "Regra horizontal: o número de lados/raios aumenta em 1 (3→4→5). Linha 3: círculo com 3 raios, 4 raios e portanto 5 raios.",
        "fr": "Règle horizontale : le nombre de côtés/rayons augmente de 1 (3→4→5). Ligne 3 : cercle avec 3 rayons, 4 rayons, donc 5 rayons."
    },
    5: {
        "it": "Regola orizzontale: il punto nero scorre verso destra lungo la riga. Regola verticale: la riga attiva scende dall'alto in basso. Nella casella mancante il punto si trova in basso a destra.",
        "en": "Horizontal rule: the black dot shifts rightward across columns. Vertical rule: active row descends from top to bottom. In the target cell, the dot is in the bottom-right corner.",
        "de": "Horizontale Regel: Der schwarze Punkt wandert nach rechts. Vertikal wandert die Zeile nach unten. Im Zielfeld befindet sich der Punkt unten rechts.",
        "es": "Regla horizontal: el punto se desplaza hacia la derecha. Regla vertical: la fila activa baja. En la casilla final, el punto está en la esquina inferior derecha.",
        "pt": "Regra horizontal: o ponto move-se para a direita. Regra vertical: a linha ativa desce. Na casa final, o ponto fica no canto inferior direito.",
        "fr": "Règle horizontale : le point noir se déplace vers la droite. Règle verticale : la rangée active descend. Le point se trouve en bas à droite."
    },
    6: {
        "it": "Regola orizzontale: la scala della figura cresce da Sinistra a Destra (Piccolo → Medio → Grande). Regola verticale: la forma si conserva per riga. Manca l'Esagono Grande.",
        "en": "Horizontal rule: scale grows left-to-right (Small → Medium → Large). Vertical rule: shape is constant per row (Circle, Diamond, Hexagon). Target is the Large Hexagon.",
        "de": "Horizontale Regel: Größe wächst von links nach rechts (Klein → Mittel → Groß). Form bleibt zeilenweise gleich. Gesucht ist das große Sechseck.",
        "es": "Regla horizontal: el tamaño crece de izquierda a derecha (Pequeño → Mediano → Grande). Falta el Hexágono Grande.",
        "pt": "Regra horizontal: o tamanho cresce da esquerda para a direita (Pequeno → Médio → Grande). Falta o Hexágono Grande.",
        "fr": "Règle horizontale : la taille augmente de gauche à droite (Petit → Moyen → Grand). Il manque le Grand Hexagone."
    },
    7: {
        "it": "Quadrato Latino: ogni riga e colonna contiene esattamente una volta Cerchio, Quadrato e Croce. Nella terza riga e colonna manca il Quadrato.",
        "en": "Latin Square: each row and column contains exactly one Circle, Square, and Cross. The third row and column lack the Square.",
        "de": "Lateinisches Quadrat: Jede Zeile und Spalte enthält genau einmal Kreis, Quadrat und Kreuz. Es fehlt das Quadrat.",
        "es": "Cuadrado Latino: cada fila y columna contiene exactamente un Círculo, Cuadrado y Cruz. Falta el Cuadrado.",
        "pt": "Quadrado Latino: cada linha e coluna possui Círculo, Quadrado e Cruz. Falta o Quadrado.",
        "fr": "Carré Latin : chaque ligne et colonne contient Cercle, Carré et Croix. Il manque le Carré."
    },
    8: {
        "it": "Quadrato Latino a 2 attributi: 1) Forma: Triangolo, Cerchio, Quadrato; 2) Riempimento: Vuoto, Tratteggiato, Pieno. Manca il Cerchio Vuoto.",
        "en": "2-Attribute Latin Square: 1) Shape: Triangle, Circle, Square; 2) Fill: Empty, Hatched, Solid. The target cell requires the Empty Circle.",
        "de": "Lateinisches Quadrat mit 2 Attributen: Form (Dreieck, Kreis, Quadrat) und Füllung (Leer, Schraffiert, Voll). Es fehlt der leere Kreis.",
        "es": "Cuadrado Latino de 2 variables: 1) Forma: Triángulo, Círculo, Cuadrado; 2) Relleno: Vacío, Rayado, Sólido. Falta el Círculo Vacío.",
        "pt": "Quadrado Latino de 2 atributos: Forma e Preenchimento (Vazio, Hachurado, Cheio). Falta o Círculo Vazio.",
        "fr": "Carré Latin à 2 attributs : Forme et Remplissage (Vide, Hachuré, Plein). Il manque le Cercle Vide."
    },
    9: {
        "it": "Quadrato Latino congiunto: forma esterna (Esagono, Cerchio, Quadrato) e simbolo interno (+, •, -). Nella terza riga mancano il Cerchio e il Più (+).",
        "en": "Joint Latin Square: outer shape (Hexagon, Circle, Square) and inner symbol (+, •, -). The target cell requires the Circle with the Plus (+) sign.",
        "de": "Kombiniertes lateinisches Quadrat: Außenform (Sechseck, Kreis, Quadrat) und Innensymbol (+, •, -). Gesucht ist der Kreis mit dem Pluszeichen.",
        "es": "Cuadrado Latino conjunto: forma exterior (Hexágono, Círculo, Cuadrado) y símbolo interior (+, •, -). Falta el Círculo con el signo Más (+).",
        "pt": "Quadrado Latino conjunto: forma externa e símbolo interno (+, •, -). Falta o Círculo com o sinal Mais (+).",
        "fr": "Carré Latin combiné : forme externe et symbole interne (+, •, -). Il manque le Cercle avec le Plus (+)."
    },
    10: {
        "it": "Regola orizzontale: la lancetta avanza in senso orario di 45° ad ogni casella. Aggiungendo 45° a 225° si ottiene 270° (lancetta orizzontale a sinistra).",
        "en": "Horizontal rule: clock hand advances 45° clockwise per cell. Adding 45° to 225° yields 270° (hand pointing straight left at 9:00).",
        "de": "Horizontale Regel: Uhrzeiger dreht sich um +45° im Uhrzeigersinn. 225° + 45° = 270° (Zeiger zeigt waagerecht nach links auf 9 Uhr).",
        "es": "Regla horizontal: la manecilla gira 45° en sentido horario por casilla. Sumando 45° a 225° resulta 270° (horizontal hacia la izquierda).",
        "pt": "Regra horizontal: o ponteiro avança 45° no sentido horário. Somando 45° a 225° obtém-se 270° (apontando para a esquerda).",
        "fr": "Règle horizontale : l'aiguille avance de 45° dans le sens horaire. 225° + 45° donne 270° (vers la gauche)."
    },
    11: {
        "it": "Due movimenti simultanei: 1) Triangolo esterno ruota di 90° orario (in riga 3 punta in alto); 2) Il punto orbita i quattro angoli in senso antiorario (in riga 3 va in Alto-Sinistra).",
        "en": "Dual movements: 1) Outer triangle rotates 90° CW (points Up in row 3); 2) Dot orbits corners counter-clockwise (lands at Top-Left in row 3).",
        "de": "Zwei Bewegungen: Dreieck dreht sich um 90° im Uhrzeigersinn (zeigt nach oben); Punkt wandert gegen den Uhrzeigersinn in die Ecke oben links.",
        "es": "Dos movimientos: el triángulo gira 90° horario (apunta hacia arriba) y el punto orbita antihorario hacia la esquina superior izquierda.",
        "pt": "Dois movimentos: triângulo gira 90° horário (aponta para cima) e o ponto orbita anti-horário até o canto superior esquerdo.",
        "fr": "Deux mouvements : le triangle tourne de 90° horaire (vers le haut) et le point orbite antihoraire vers le coin supérieur gauche."
    },
    12: {
        "it": "Quadrato Latino: orientamento linea (Orizzontale, Verticale, Diagonale) e terminazioni (Pallini, Frecce, Trattini T). Manca la linea Verticale con Pallini.",
        "en": "Latin Square: line orientation (Horizontal, Vertical, Diagonal) and end caps (Dots, Arrows, T-bars). Target is the Vertical line with Dots.",
        "de": "Lateinisches Quadrat: Linienausrichtung und Endstücke (Punkte, Pfeile, T-Balken). Gesucht ist die vertikale Linie mit Endpunkten.",
        "es": "Cuadrado Latino: orientación de línea y extremos (Puntos, Flechas, Barras T). Falta la línea Vertical con Puntos.",
        "pt": "Quadrado Latino: orientação da linha e terminações (Pontos, Setas, Barras T). Falta a linha Vertical com Pontos.",
        "fr": "Carré Latin : orientation de la ligne et extrémités (Points, Flèches, Barres T). Il manque la ligne Verticale avec Points."
    },
    13: {
        "it": "Unione grafica diretta: Col 1 + Col 2 = Col 3. Sovrapponendo il cerchio della prima colonna e il quadrato della seconda si ottiene il quadrato con cerchio inscritto.",
        "en": "Direct Graphical Union: Col 1 + Col 2 = Col 3. Overlaying the circle from col 1 and square from col 2 yields the Square with inscribed Circle.",
        "de": "Direkte grafische Vereinigung: Spalte 1 + Spalte 2 = Spalte 3. Kreis und Quadrat überlagert ergeben das Quadrat mit einbeschriebenem Kreis.",
        "es": "Unión gráfica directa: Col 1 + Col 2 = Col 3. Superponiendo el círculo y el cuadrado se obtiene el cuadrado con círculo inscrito.",
        "pt": "União gráfica direta: Col 1 + Col 2 = Col 3. A sobreposição do círculo com o quadrado gera o quadrado com círculo inscrito.",
        "fr": "Union graphique directe : Col 1 + Col 2 = Col 3. La superposition du cercle et du carré donne le carré avec cercle inscrit."
    },
    14: {
        "it": "Addizione quantitativa: il numero di segmenti in Col 3 è la somma di Col 1 e Col 2. In riga 3: 3 diagonali + 3 diagonali = 6 segmenti diagonali.",
        "en": "Quantitative addition: count in Col 3 = Col 1 + Col 2. In row 3: 3 diagonal slashes + 3 diagonal slashes = 6 diagonal slashes.",
        "de": "Quantitative Addition: Spalte 3 = Spalte 1 + Spalte 2. Zeile 3: 3 diagonale Linien + 3 diagonale Linien = 6 diagonale Linien.",
        "es": "Suma cuantitativa: la cantidad en Col 3 es la suma de Col 1 y Col 2. Fila 3: 3 diagonales + 3 diagonales = 6 diagonales.",
        "pt": "Soma quantitativa: a quantidade em Col 3 é a soma de Col 1 e Col 2. Linha 3: 3 diagonais + 3 diagonais = 6 diagonais.",
        "fr": "Addition quantitative : le nombre en Col 3 est la somme de Col 1 et Col 2. Ligne 3 : 3 diagonales + 3 diagonales = 6 diagonales."
    },
    15: {
        "it": "Sottrazione grafica: Col 1 - Col 2 = Col 3. Dal cerchio con croce interna (+) si sottrae il raggio verticale, lasciando il cerchio con la sola linea orizzontale.",
        "en": "Graphical Subtraction: Col 1 - Col 2 = Col 3. Subtracting the vertical line from the circle with cross (+) leaves the Circle with horizontal diameter.",
        "de": "Grafische Subtraktion: Spalte 1 - Spalte 2 = Spalte 3. Kreis mit Kreuz minus vertikale Linie ergibt Kreis mit waagerechter Linie.",
        "es": "Resta gráfica: Col 1 - Col 2 = Col 3. Del círculo con cruz se resta la línea vertical, quedando el círculo con la línea horizontal.",
        "pt": "Subtração gráfica: Col 1 - Col 2 = Col 3. Do círculo com cruz subtrai-se a linha vertical, restando a linha horizontal.",
        "fr": "Soustraction graphique : Col 1 - Col 2 = Col 3. Du cercle avec croix on soustrait la ligne verticale, restant le diamètre horizontal."
    },
    16: {
        "it": "Salto orbitale perimetrale: il punto salta 2 posizioni in senso orario lungo gli 8 vertici del quadrato (+2 mod 8). Da Basso-Destra passa a Basso-Sinistra.",
        "en": "Perimeter orbital movement: the dot jumps 2 positions clockwise around the 8 perimeter points. From Bottom-Right, +2 steps lands at Bottom-Left.",
        "de": "Umlaufbewegung: Der Punkt springt 2 Positionen im Uhrzeigersinn an den 8 Randpunkten entlang. Von unten rechts gelangt er nach unten links.",
        "es": "Salto orbital perimetral: el punto avanza 2 posiciones horarias sobre los 8 puntos del borde. De abajo-derecha pasa a abajo-izquierda.",
        "pt": "Movimento orbital: o ponto salta 2 posições no sentido horário pelos 8 nós perimetrais, indo para o canto inferior esquerdo.",
        "fr": "Saut orbital périmétrique : le point saute de 2 positions dans le sens horaire, atterrissant dans le coin inférieur gauche."
    },
    17: {
        "it": "Intersezione insiemistica (AND booleano): solo le regioni colorate in entrambe le figure rimangono piene. Nella terza riga è piena solo l'intersezione dei due rombi.",
        "en": "Boolean Intersection (AND): only regions filled in both figures remain filled in Col 3. In row 3, only the overlapping lens of the two diamonds is filled.",
        "de": "Mengen-Schnittmenge (Boolesches UND): Nur Bereiche, die in beiden Figuren gefüllt sind, bleiben gefüllt. Das betrifft die Schnittfläche der Rauten.",
        "es": "Intersección booleana (AND): solo las zonas rellenas en ambas figuras permanecen rellenas. En la fila 3, solo se rellena la intersección de los rombos.",
        "pt": "Interseção booleana (AND): apenas as regiões preenchidas em ambas as figuras permanecem preenchidas. Fica preenchida apenas a interseção dos losangos.",
        "fr": "Intersection booléenne (AND) : seules les zones remplies dans les deux figures restent pleines. Seule l'intersection des deux losanges est remplie."
    },
    18: {
        "it": "Traiettorie incrociate continue: il pallino nero avanza verso destra (x=75) e il quadrato cavo sale dal basso verso l'alto (y=25).",
        "en": "Intersecting trajectories: the solid dot moves rightward (x=75) while the hollow square ascends from bottom to top (y=25).",
        "de": "Gekreuzte Pfade: Der Punkt wandert nach rechts (x=75), während das Quadrat von unten nach oben steigt (y=25).",
        "es": "Trayectorias cruzadas: el punto se mueve hacia la derecha (x=75) y el cuadrado hueco asciende hacia arriba (y=25).",
        "pt": "Trajetórias cruzadas: o ponto sólido vai para a direita (x=75) e o quadrado oco sobe para cima (y=25).",
        "fr": "Trajectoires croisées : le point plein va vers la droite (x=75) et le carré creux monte vers le haut (y=25)."
    },
    19: {
        "it": "XOR orizzontale su 3 linee: le linee presenti in entrambe si cancellano; quelle presenti in una sola rimangono. [Top, Mid] XOR [Top] = resta solo la linea Centrale.",
        "en": "Horizontal Line XOR: common lines cancel out; lines in only one cell remain. [Top, Mid] XOR [Top] = Top cancels out, leaving only the Middle line.",
        "de": "Boolesches XOR auf 3 Linien: Gemeinsame Linien heben sich auf. [Oben, Mitte] XOR [Oben] = Oben hebt sich auf, es bleibt die mittlere Linie.",
        "es": "XOR en 3 líneas: las líneas comunes se cancelan. [Superior, Central] XOR [Superior] = se cancela Superior y queda la línea Central.",
        "pt": "XOR em 3 linhas: linhas comuns anulam-se. [Superior, Central] XOR [Superior] = anula-se a Superior, restando apenas a Central.",
        "fr": "XOR sur 3 lignes : les lignes communes s'annulent. [Haut, Milieu] XOR [Haut] = le Haut s'annule, laissant la ligne du Milieu."
    },
    20: {
        "it": "XOR su croce a 4 bracci: [Nord, Est, Ovest] XOR [Est, Sud, Ovest] = Est e Ovest si cancellano, lasciando i bracci Nord e Sud (linea verticale).",
        "en": "4-Spoke Cross XOR: [North, East, West] XOR [East, South, West] = East and West cancel out, leaving North and South spokes (vertical line).",
        "de": "XOR auf Kreuzarmen: [Nord, Ost, West] XOR [Ost, Süd, West] = Ost und West löschen sich aus, es bleiben Nord und Süd (vertikale Linie).",
        "es": "XOR en cruz de 4 brazos: Este y Oeste son comunes y se eliminan, quedando Norte y Sur (línea vertical).",
        "pt": "XOR nos braços da cruz: Leste e Oeste anulam-se, restando Norte e Sul (linha vertical).",
        "fr": "XOR sur croix à 4 branches : Est et Ouest s'annulent, laissant Nord et Sud (ligne verticale)."
    },
    21: {
        "it": "Doppia regola: diagonali seguono XOR (\\ XOR X = resta /); il simbolo centrale segue un Quadrato Latino (Stella, Cerchio, Triangolo). Risposta: / con Triangolo.",
        "en": "Dual rule: diagonals follow XOR (\\ XOR X = / remains); central symbol follows Latin Square (Star, Circle, Triangle). Target: / with Triangle.",
        "de": "Doppelregel: Diagonalen folgen XOR (\\ XOR X = /); Zentralsymbol folgt lateinischem Quadrat. Lösung: / mit Dreieck im Zentrum.",
        "es": "Regla dual: las diagonales siguen XOR (\\ XOR X = /); el núcleo sigue Cuadrado Latino. Solución: / con Triángulo.",
        "pt": "Regra dupla: as diagonais seguem XOR (\\ XOR X = /); o símbolo central segue Quadrado Latino. Resposta: / com Triângulo.",
        "fr": "Double règle : diagonales selon XOR (\\ XOR X = /) ; symbole central selon Carré Latin. Réponse : / avec Triangle."
    },
    22: {
        "it": "Rotazione 90° oraria + perdita di raggi: in riga 3 la rotazione porta a 0° e il numero di raggi scende da 6 → 5 → 4 raggi interni nell'esagono.",
        "en": "90° CW rotation + spoke loss: in row 3, rotation brings orientation to 0° and spoke count decreases from 6 → 5 → 4 spokes inside the hexagon.",
        "de": "90° Drehung im Uhrzeigersinn + Verlust von Speichen: Zeile 3 rotiert auf 0°, Speichenzahl sinkt von 6 auf 5 auf 4.",
        "es": "Rotación 90° horario + pérdida de radios: la orientación llega a 0° y los radios bajan de 6 → 5 → 4 dentro del hexágono.",
        "pt": "Rotação 90° horária + perda de raios: orientação atinge 0° e os raios descem de 6 → 5 → 4 dentro do hexágono.",
        "fr": "Rotation 90° horaire + perte de rayons : orientation à 0° et diminution de 6 → 5 → 4 rayons dans l'hexagone."
    },
    23: {
        "it": "XOR su griglia 3x3 di 9 punti: Alto-Dx e Centro sono comuni e si annullano; rimangono Alto-Sx, Basso-Sx e Basso-Dx (3 punti a forma di L).",
        "en": "3x3 Dot Grid XOR: Top-Right and Center dots are common and cancel out; Top-Left, Bottom-Left, and Bottom-Right remain (3 dots in an L-shape).",
        "de": "XOR auf 3x3-Punktmatrix: Oben-Rechts und Mitte löschen sich aus; Oben-Links, Unten-Links und Unten-Rechts bleiben übrig (L-Form).",
        "es": "XOR en matriz 3x3 de puntos: Arriba-Derecha y Centro se cancelan; quedan Arriba-Izquierda, Abajo-Izquierda y Abajo-Derecha (forma de L).",
        "pt": "XOR na grade 3x3 de pontos: Alto-Direita e Centro anulam-se; restam Alto-Esquerda, Baixo-Esquerda e Baixo-Direita (formato L).",
        "fr": "XOR sur grille de points 3x3 : Haut-Droite et Centre s'annulent ; restent Haut-Gauche, Bas-Gauche et Bas-Droite (en L)."
    },
    24: {
        "it": "Nodi da linee incidenti: N linee orizzontali × M verticali generano N×M nodi neri. Nella cella (3,3) si incrociano 3 linee H e 3 V, creando 9 nodi.",
        "en": "Intersection nodes: N horizontal × M vertical lines yield N×M black intersection nodes. In cell (3,3), 3 H-lines cross 3 V-lines = 9 nodes.",
        "de": "Schnittknoten: N horizontale × M vertikale Linien erzeugen N×M schwarze Punkte. Bei 3 H- und 3 V-Linien entstehen 9 Knotenpunkte.",
        "es": "Nodos de intersección: N líneas horizontales × M verticales generan N×M nodos negros. 3 líneas H y 3 V = 9 nodos.",
        "pt": "Nós de interseção: N linhas horizontais × M verticais geram N×M nós pretos. 3 linhas H e 3 V = 9 nós.",
        "fr": "Nœuds d'intersection : N lignes horizontales × M verticales génèrent N×M nœuds noirs. 3 lignes H et 3 V = 9 nœuds."
    },
    25: {
        "it": "Triplo Quadrato Latino: poligono esterno (manca l'Esagono), tratteggio (manca l'Orizzontale) e satellite (manca Basso-Destra).",
        "en": "Triple Latin Cube: outer shape (Hexagon missing), hatching angle (Horizontal missing), satellite dot (Bottom-Right missing).",
        "de": "Dreifaches lateinisches Quadrat: Außenform (Sechseck fehlt), Schraffur (horizontal fehlt), Satellit (unten rechts fehlt).",
        "es": "Triple Cuadrado Latino: forma exterior (falta Hexágono), rayado (falta Horizontal) y satélite (falta Abajo-Derecha).",
        "pt": "Triplo Quadrado Latino: forma externa (falta Hexágono), hachura (falta Horizontal) e satélite (falta Baixo-Direita).",
        "fr": "Triple Carré Latin : forme externe (Hexagone), hachures (Horizontales) et satellite (Bas-Droite manquants)."
    },
    26: {
        "it": "Rotazione modulare (+45° per colonna) e decremento rami (-1 per cella). In riga 3 resta un singolo ramo puntato a 270° (sinistra).",
        "en": "Modular rotation (+45° per step) and branch loss (-1 per cell). In cell (3,3), exactly 1 branch remains pointing left at 270°.",
        "de": "Modulare Rotation (+45° pro Schritt) und Speichenabnahme (-1). Es bleibt genau 1 Ast übrig, der bei 270° nach links zeigt.",
        "es": "Rotación modular (+45° por casilla) y pérdida de ramas (-1). Queda exactamente 1 rama apuntando a 270° (izquierda).",
        "pt": "Rotação modular (+45° por passo) e redução de ramos (-1). Resta exatamente 1 ramo apontando para 270° (esquerda).",
        "fr": "Rotation modulaire (+45° par étape) et perte de branches (-1). Il reste 1 seule branche pointée à 270° (gauche)."
    },
    27: {
        "it": "XOR composto con riflessione speculare: le barre seguono XOR tra Col 1 e Col 2, e il risultato viene ribaltato orizzontalmente in Col 3.",
        "en": "Composite XOR with horizontal reflection: horizontal bars follow XOR, then the resulting pattern is flipped left-to-right in Col 3.",
        "de": "Zusammengesetztes XOR mit horizontaler Spiegelung: Balken folgen XOR, das Ergebnis wird in Spalte 3 horizontal gespiegelt.",
        "es": "XOR compuesto con reflexión especular: las barras siguen XOR y el resultado se voltea horizontalmente en Col 3.",
        "pt": "XOR composto com reflexão especular: as barras seguem XOR e o resultado é invertido horizontalmente na Col 3.",
        "fr": "XOR composé avec réflexion horizontale : les barres suivent XOR puis le motif est inversé horizontalement en Col 3."
    },
    28: {
        "it": "Integrazione multi-variabile a 3 vincoli: 1) Poligono esterno (Quadrato Latino): in riga 3 manca l'Esagono; 2) Asse interno (Quadrato Latino): in riga 3 manca l'Asse Verticale; 3) I nodi ruotano di +45° ad ogni casella (in riga 3: 180°→225°→270°), e il nodo che interseca l'asse verticale diventa pieno. La figura corretta è l'Esagono con asse verticale e nodo inferiore pieno.",
        "en": "Tri-variate integration: 1) Outer polygon (Latin square): row 3 requires Hexagon; 2) Internal axis (Latin square): row 3 requires Vertical Axis; 3) Orbital nodes advance by +45° per step (in row 3: 180°→225°→270°), with the node intersecting the vertical axis turning solid. The correct figure is Hexagon with vertical axis and solid bottom node.",
        "de": "Drei unabhängige Variablen: 1) Äußeres Polygon (Lateinisches Quadrat): In Zeile 3 fehlt das Sechseck; 2) Interne Achse (Lateinisches Quadrat): In Zeile 3 fehlt die vertikale Achse; 3) Knoten rotieren um +45° (Zeile 3: 180°→225°→270°), und der Knoten auf der vertikalen Achse ist ausgefüllt. Die richtige Figur ist das Sechseck mit vertikaler Achse.",
        "es": "Integración multi-variable: 1) Polígono externo (Cuadrado Latino): en fila 3 falta el Hexágono; 2) Eje interno (Cuadrado Latino): en fila 3 falta el Eje Vertical; 3) Los nodos rotan +45° por paso (fila 3: 180°→225°→270°), y el nodo que interseca el eje vertical es sólido. La figura correcta es el Hexágono con eje vertical y nodo inferior sólido.",
        "pt": "Integração multi-variável: 1) Polígono externo (Quadrado Latino): na linha 3 falta o Hexágono; 2) Eixo interno (Quadrado Latino): na linha 3 falta o Eixo Vertical; 3) Os nós orbitais giram +45° por passo (linha 3: 180°→225°→270°), e o nó que cruza o eixo vertical fica sólido. A figura correta é o Hexágono com eixo vertical e nó inferior sólido.",
        "fr": "Intégration multi-variable : 1) Polygone externe (Carré Latin) : ligne 3 nécessite l'Hexagone ; 2) Axe interne (Carré Latin) : ligne 3 nécessite l'Axe Vertical ; 3) Les nœuds orbitaux avancent de +45° par étape (ligne 3 : 180°→225°→270°), le nœud croisant l'axe vertical devenant plein. La figure correcte est l'Hexagone avec axe vertical et nœud inférieur plein."
    },
    29: {
        "it": "Trasformazione polare a tre regole simultanee: 1) L'arco esterno semicircolare ruota di +90° in senso orario (in riga 3: 180°→270°→0°); 2) L'arco interno a quadrante ruota di 90° in senso antiorario (in riga 3: 180°→90°→0°); 3) Il nucleo centrale segue un Quadrato Latino (in riga 3 manca il Quadrato); 4) I marcatori a rombo aumentano di 1 per riga (in riga 3 sono esattamente 3). La figura corretta ha aperture a 0°, nucleo quadrato e 3 marcatori.",
        "en": "Tri-variate polar transformation: 1) Outer semicircular arc rotates +90° CW (row 3: 180°→270°→0°); 2) Inner quadrant arc rotates 90° CCW (row 3: 180°→90°→0°); 3) Central core follows a Latin square (row 3 requires Square); 4) Diamond markers increase by 1 per row (row 3 has exactly 3). The unique correct figure has openings at 0°, central square, and 3 markers.",
        "de": "Drei simultane Polartransformationen: 1) Äußerer Bogen rotiert +90° im Uhrzeigersinn (Zeile 3: 180°→270°→0°); 2) Innerer Bogen rotiert 90° gegen den Uhrzeigersinn (Zeile 3: 180°→90°→0°); 3) Zentraler Kern folgt einem Lateinischen Quadrat (Zeile 3: Quadrat); 4) Diamant-Markierungen erhöhen sich um 1 pro Zeile (Zeile 3: genau 3). Die richtige Figur hat Öffnungen bei 0°, zentrales Quadrat und 3 Markierungen.",
        "es": "Transformación polar a tres reglas: 1) El arco externo rota +90° horario (fila 3: 180°→270°→0°); 2) El arco interno rota 90° antihorario (fila 3: 180°→90°→0°); 3) El núcleo central sigue un Cuadrado Latino (fila 3: Cuadrado); 4) Los marcadores de diamante aumentan de 1 por fila (fila 3: exactamente 3). La figura correcta tiene aberturas a 0°, núcleo cuadrado y 3 marcadores.",
        "pt": "Transformação polar com três regras: 1) O arco externo gira +90° no sentido horário (linha 3: 180°→270°→0°); 2) O arco interno gira 90° no sentido anti-horário (linha 3: 180°→90°→0°); 3) O núcleo central segue um Quadrado Latino (linha 3: Quadrado); 4) Os marcadores em losango aumentam em 1 por linha (linha 3: exatamente 3). A figura correta tem aberturas em 0°, núcleo quadrado e 3 marcadores.",
        "fr": "Transformation polaire à trois lois : 1) L'arc externe tourne de +90° dans le sens horaire (ligne 3 : 180°→270°→0°) ; 2) L'arc interne tourne de 90° dans le sens anti-horaire (ligne 3 : 180°→90°→0°) ; 3) Le noyau central suit un Carré Latin (ligne 3 : Carré) ; 4) Les marqueurs en losange augmentent de 1 par ligne (ligne 3 : exactement 3). La figure correcte présente des ouvertures à 0°, un noyau carré et 3 marqueurs."
    },
    30: {
        "it": "Il Problema Maestro: anello esterno ruota +90° orario, medio -90° antiorario, interno inverte 180°. Conservazione di 6 nodi con migrazione verso l'esterno: 6 nodi esterni, 0 interni.",
        "en": "The Master Matrix: outer ring rotates +90° CW, middle -90° CCW, inner flips 180°. Conservation of 6 total dots with outward migration = 6 outer dots, 0 inner dots.",
        "de": "Die Meister-Matrix: Äußerer Ring rotiert +90° CW, mittlerer -90° CCW, innerer 180°. Erhaltung von 6 Punkten mit Wanderung nach außen = 6 äußere, 0 innere Punkte.",
        "es": "La Matriz Maestra: anillo exterior rota +90° horario, medio -90° antihorario, interior 180°. Conservación de 6 puntos = 6 puntos exteriores, 0 interiores.",
        "pt": "A Matriz Mestra: anel externo gira +90° horário, médio -90° anti-horário, interno 180°. Conservação de 6 nós = 6 nós externos, 0 internos.",
        "fr": "La Matrice Maîtresse : anneau externe tourne +90° horaire, moyen -90° antihoraire, interne 180°. Conservation de 6 points = 6 points externes, 0 internes."
    }
}

print(f"Loaded multilingual explanations for all {len(EXPLANATIONS)} questions.")
