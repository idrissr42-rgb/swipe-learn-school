# Site du groupe Swipe Learn School (swipelearn.school)

Page d'accueil du groupe : les sept écoles, le test d'orientation, les métiers et le comparateur des formations de Cook.
Seule Cook est ouverte ; les six autres écoles proposent « Être prévenu de l'ouverture ».

Mise en ligne : un site Netlify relié à ce dossier (publish = public), puis le domaine swipelearn.school pointé dessus.

Reconstruire la page après une modification : `python3 outils/construire.py`
(source : outils/source/maquette-origine.html pour le design, outils/source/formations-cook.json pour le catalogue de Cook).

À rendre vrai avant de l'écrire sur la page : déclaration d'activité enregistrée, certification Qualiopi,
formations éligibles au CPF, vrais avis d'élèves (avec leur accord), réseau de restaurants partenaires.

## Téléphone et application installable

- `outils/mobile_appli.py` (appelé par `construire.py`) : styles pour téléphone, carrousels à faire glisser
  (écoles, CAP intensif, méthode, métiers), bandeau « Installer l’application » (Android et ordinateur : bouton ;
  iPhone : « Partager, puis Sur l’écran d’accueil »), lien « Installer l’application » dans le pied de page.
- Fichiers écrits : `manifest.webmanifest`, `sw.js` (réseau d’abord, dernière version vue hors connexion),
  `hors-ligne.html`, `_headers`, icônes `logos/icone-groupe-masquable-512.png` et `logos/apple-touch-icon.png`.
- Captures montrées par Android dans la fenêtre d’installation : `node outils/captures.js && python3 outils/construire.py`.
- Après un changement du service worker, augmenter `VERSION_CACHE` dans `mobile_appli.py`.
