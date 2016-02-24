# DICCIONARIO ESPAÑOL-NËME
## SPANISH-NËME DICTIONARY

###[ESP]
El método de uso es bastante intuitivo. Las palabras se muestran en una ScrolledWindow, podemos filtrar palabras a través del widget de Entry, eligiendo explícitamente en qué idioma estamos buscando la palabra en cuestión; y después tenemos botones para agregado y modificado de entradas. En cuanto al botón "eliminar", trabaja directamente con la fila seleccionada en la ScrolledWindow, a diferencia de los botones "agregar" y "modificar" que abren ventanas nuevas.
<p>El método de modificación se lleva a cabo eligiendo primero el idioma de la palabra que queremos modificar, en función del cual se modifica el menú desplgable; se selecciona la palabra y se escribe la modificación en el entry inmediatamente inferior al menú.
<p>En cuanto al conjugador de verbos, como con el botón "borrar", trabaja directamente seleccionando una fila de la ScrolledWindow. Se selecciona una y el programa devolverá inmediatamente las conjugaciones del verbo en todos los tiempos gramaticales.

La idea de este programa nació como necesidad de poder agregar palabras de un idioma ficticio (conlang, en inglés) a un diccionario a medida que se me fueran ocurriendo sin tener que crear un documento de texto donde guardarlas y después tener que buscarlas manualmente -como hice en un principio-.

Más allá de que el actual script viene acompañado de una base de datos con palabras en nëme y su traducción correspondiente al español, el usuario es totalmente libre de borrar dicha base de datos y emplear el programa para llenar el diccionario con palabras de su propio idioma ficticio, con los respectivos arreglos al script. Cabe aclarar que el script está diseñado para detectar verbos en _español_, ya que se emplea un filtro basado en la terminación de las palabras que permite separar verbos de las demás palabras y es el medio que le permite luego al programa poder conjugar los verbos en nëme. Pero, visto que el script se apoya en la distinción de verbos por terminaciones que se repiten, sería muy fácil traducirlo a idiomas como el alemán o el francés, que tienen características de terminación repetitiva como el español. El inglés es otro tema, porque sus verbos no tienen terminaciones que se emplean para todos -vamos desde _sing_ a _elevate_ a _fear_ y podemos seguir-.

Aclaración con respecto al número de lineas de código: la elevada cantidad de líneas se debe a mi arduo empleo de líneas de referencia para el debugging; todas las líneas para printear son líneas de referencia, y decidí no eliminarlas por si alguien quiere modificar el código y necesita ver qué sucede en la consola.

Algunas cosas que me gustaría poder modificar de la interfaz:
<p>-el tamaño de los botones en la stack inicial
<p>-la longitud del campo de las entries en el stack de conjugación de verbos
<p>-el menú de "modificación" en el stack principal, que crea menús de lista infinitos

###[ENG]
This program is of very intuitive use, I think. Words are shown on the ScrolledWindow and we can filter them by writing on the entry widget on the right, explicitly indicating to which language the word belongs to; and then we have "add" and "modify" options. The thing with the "delete" button is more intuitive than the other ones because you directly select the row containing the word you want to delete, and press it; while "add" and "modify" open a new window.
When it comes to the modifing method, you choose the language of the word you want to modify and the dropdown menu will display all the words available from the database; once the word's been chosen, you can write the new word that will replace the latter and after a click on "accept", the database and the displaying words will be instantly refreshed.
The verb conjugator works directly like the "delete" button; you chose a row, and the program will instantly conjugate that verb in every gramatical tense.

The reason for the existence of this program was my need to be able to add words from a conlang I've came up with to a dictionary as I invented them without having to create a text document and have to look for them manually -which I did at first-.

Although the actual script comes with a database with words in nëme -the conlang in question- and its spanish translations, the user is totally free to delete said database and use the program to fill a dictionary with words from his/her own conlang, with the respective needed changes on the script. It must be said that this script in particular is designed to detect _spanish_ verbs as it employs a word-termination-based filter that allows the program to distinguish between verbs and other types of words and that is what later allows the program to conjugate nëme verbs. But, as seen as the scrip is interested in word terminations to filter verbs from other words, it would be easy for translation into languages like German or French, that have verbs that usually have regular word-endings, like Spanish does. English is another matter altogether, and I dare anyone who speaks it as their mother language to see if they can translate the script so it works with English words, too; that would be awesome.

Something to say about the codeline counting: the high amount of lines in this script has to do with my asiduous use of the print command for debugging purpouses, as I'm always setting debugging reference points so that I know where something went wrond; and I think that's the reason why I haven't get rid of it in this commit, as I think it would be usefull for someone if they were to modify the script to see what's going on undereneath.

Somethings that I would love to improve about the UI:
<p>-the size of the inicial's stack buttons
<p>-the width of the verb conjunction's stack entries.
<p>-the infinite dropdown menus creation in the "modify" window
