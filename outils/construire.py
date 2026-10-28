# Site du groupe Swipe Learn School (swipelearn.school) : version vraie de la maquette.
# Entrée : maquette-origine.html (design et structure gardés) et formations-cook.json (catalogue réel de Cook).
# Sortie : public/index.html, public/sitemap.xml, public/robots.txt, public/404.html.
# Règles : nom public « Swipe Learn School » (jamais « Swipe and … »), Cook et Sell sont ouvertes, aucun financement
# public annoncé avant Qualiopi, aucun témoignage ni chiffre inventé, liens simples vers les écoles.
import json, re, html, os

ICI = os.path.dirname(os.path.abspath(__file__))
RAC = os.path.dirname(ICI)
h = open(os.path.join(ICI, 'source', 'maquette-origine.html'), encoding='utf-8').read()
F = json.load(open(os.path.join(ICI, 'source', 'formations-cook.json'), encoding='utf-8'))
COOK = 'https://cook.swipelearn.school'
SELL = 'https://sell.swipelearn.school'
SITE = 'https://swipelearn.school'
CONTACT = 'contact@swipeandlearn.school'
NB_F, NB_L, NB_X = 50, 651, 100
# Sell : chiffres et formations lus dans les contenus du site de Sell (dépôt swipe-sell), recopiés dans source/formations-sell.json
FS = json.load(open(os.path.join(ICI, 'source', 'formations-sell.json'), encoding='utf-8'))
SB_F, SB_L, SB_X = FS['nb_formations'], FS['nb_lecons'], FS['nb_examens']
E = lambda s: html.escape(str(s), quote=True)


def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, (a[:90], c)
    h = h.replace(a, b)


def rep_re(motif, b, n=1, flags=re.S):
    global h
    h, c = re.subn(motif, b, h, flags=flags)
    assert c == n, (motif[:90], c)


def prevenir(ecole):
    return f'mailto:{CONTACT}?subject=' + ('Ouverture de ' + ecole).replace(' ', '%20')


# ------------------------------------------------------------------ en-tête : titre, description, données structurées
TITRE = 'Swipe Learn School : écoles de formation en ligne'
DESC = 'Sept écoles de formation, une méthode : cours en ligne avec un formateur. Cook, l’école de cuisine, et Sell, l’école de la vente, sont ouvertes.'
assert len(TITRE) <= 60 and len(DESC) <= 160
LD = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'WebSite', '@id': SITE + '/#site', 'name': 'Swipe Learn School', 'url': SITE + '/', 'inLanguage': 'fr-FR', 'publisher': {'@id': SITE + '/#organisation'}},
    {'@type': 'EducationalOrganization', '@id': SITE + '/#organisation', 'name': 'Swipe Learn School', 'legalName': 'SWIPE LEARN SCHOOL', 'url': SITE + '/',
     'logo': SITE + '/logos/icone-groupe-512.png', 'email': CONTACT,
     'identifier': {'@type': 'PropertyValue', 'propertyID': 'SIRET', 'value': '13129496900012'},
     'address': {'@type': 'PostalAddress', 'streetAddress': '40 rue de la Badouillère', 'postalCode': '42000', 'addressLocality': 'Saint-Étienne', 'addressRegion': 'Auvergne-Rhône-Alpes', 'addressCountry': 'FR'},
     'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Auvergne-Rhône-Alpes'}, {'@type': 'Country', 'name': 'France'}],
     'subOrganization': [{'@type': 'EducationalOrganization', '@id': COOK + '/#ecole', 'name': 'Swipe Learn School · Cook', 'url': COOK + '/'},
                         {'@type': 'EducationalOrganization', '@id': SELL + '/#ecole', 'name': 'Swipe Learn School · Sell', 'url': SELL + '/'}]},
]}
rep_re(r'<title>.*?</title>\s*<meta name="description" content="[^"]*">',
       f'<title>{E(TITRE)}</title>\n<meta name="description" content="{E(DESC)}">\n<link rel="canonical" href="{SITE}/">\n<meta name="robots" content="index,follow,max-image-preview:large">\n'
       f'<meta property="og:site_name" content="Swipe Learn School"><meta property="og:locale" content="fr_FR"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/"><meta property="og:title" content="{E(TITRE)}"><meta property="og:description" content="{E(DESC)}"><meta property="og:image" content="{SITE}/logos/icone-groupe-512.png">\n'
       f'<link rel="icon" type="image/svg+xml" href="/logos/icone-groupe.svg"><link rel="icon" href="/favicon.ico" sizes="48x48">\n<script type="application/ld+json">{json.dumps(LD, ensure_ascii=False)}</script>')
# styles ajoutés : écoles à venir, offre intensive
rep('</style>', '''.ecole.bientot{opacity:.92}.ecole.bientot .tag-etat{background:var(--beige);color:var(--taupe)}.ecole.bientot ul li span{display:none}
.intensif-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:26px}
.intensif-grid .carte{background:var(--blanc);border:1px solid var(--beige-f);border-radius:var(--r);padding:22px}
.intensif-grid .carte b{display:block;font-family:'Baloo 2';font-size:1.15rem;margin-bottom:6px;color:var(--cook)}
.intensif-cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:24px}.intensif-cta small{color:var(--taupe)}
</style>''', n=1)

# ------------------------------------------------------------------ navigation et marque
rep('<span><b>SWIPE AND LEARN</b><small>Groupe de formation</small></span>', '<span><b>SWIPE LEARN SCHOOL</b><small>Groupe de formation</small></span>')
rep('<a class="brand" href="#">', '<a class="brand" href="/">')
rep_re(r'<li><a href="#quiz">Test d\'orientation</a></li>\s*<li><a href="#ecoles">Nos 7 écoles</a></li>', '<li><a href="#ecoles">Nos écoles</a></li><li><a href="#intensif">CAP intensif</a></li>')

# ------------------------------------------------------------------ accueil (hero)
rep_re(r'\s*<span class="sur"><i></i>Le groupe qui forme aux métiers qui recrutent</span>', '')
rep('<h1>Sept écoles.<br>Un seul geste : <span class="m">apprendre.</span></h1>', '<h1>Un groupe, sept écoles.</h1>\n      <p class="geste">Un seul geste&nbsp;: apprendre.</p>')
rep_re(r'<p>Cuisine, vente, santé, numérique, bâtiment, transport, gestion : Swipe and Learn réunit sept écoles.*?</p>',
       '<p>Cuisine, vente, aide à la personne, numérique, bâtiment, transport, gestion : Swipe Learn School réunit sept écoles. Que vous cherchiez un emploi, que vous changiez de métier ou que vous travailliez déjà, chaque formation part des bases. La théorie se suit en ligne ; la pratique se fait en entreprise, près de chez vous. Cook et Sell sont ouvertes ; les autres écoles ouvrent une à une.</p>')
rep_re(r'<a class="btn btn-ghost" href="#ecoles">Voir les écoles</a>', f'<a class="btn btn-ghost" href="{COOK}/">Découvrir Cook, l’école de cuisine</a>')
rep_re(r'(<span>)(<svg[^>]*>(?:(?!</svg>).)*</svg>)Certifications RNCP(</span>)', r'\1\2Cours en ligne avec un formateur\3')
rep_re(r'(<span>)(<svg[^>]*>(?:(?!</svg>).)*</svg>)Éligible CPF(</span>)', r'\1\2Pratique près de chez vous\3')
rep_re(r'(<span>)(<svg[^>]*>(?:(?!</svg>).)*</svg>)Promos à taille humaine(</span>)', r'\1\2Inscription toute l’année\3')
for k, dom in [('Cook', 'Cuisine'), ('Sell', 'Vente'), ('Care', 'Santé'), ('Code', 'Numérique'), ('Build', 'Bâtiment'), ('Manage', 'Gestion'), ('Drive', 'Transport')]:
    rep(f'<b>{dom}</b><br><small>Swipe and {k}</small>', f'<b>{dom}</b><br><small>{k} · {"ouverte" if k in ("Cook", "Sell") else "bientôt"}</small>')
rep('<b>Santé</b><br>', '<b>Aide à la personne</b><br>')

# ------------------------------------------------------------------ chiffres (tous vérifiables sur le site de Cook)
rep_re(r'<div class="chiffres">.*?</div>\s*</div>\s*(?=<section id="ecoles">)',
       f'''<div class="chiffres">
  <div class="wrap">
    <div class="rv"><div class="v">7</div><div class="l">écoles, dont Cook et Sell déjà ouvertes</div></div>
    <div class="rv"><div class="v">{NB_F}</div><div class="l">formations à Cook, dont 16 préparations à un diplôme</div></div>
    <div class="rv"><div class="v">{NB_L}</div><div class="l">leçons et {NB_X} examens blancs en ligne à Cook</div></div>
    <div class="rv"><div class="v">15 j</div><div class="l">au plus pour répondre à votre demande d’inscription</div></div>
  </div>
</div>
''')

# ------------------------------------------------------------------ écoles
rep('<p class="sec-sub rv">Chaque école a sa couleur, sa plateforme et ses formateurs métier — toutes partagent la même exigence et la même pédagogie Swipe and Learn.</p>',
    '<p class="sec-sub rv">Chaque école a sa couleur, sa plateforme et ses formateurs du métier ; toutes partagent la même méthode. Cook et Sell sont ouvertes, les cinq autres arrivent.</p>')
rep_re(r'<div class="mod-lg presentiel"><span class="mod-pastille">Distance \+ centre</span>.*?</div>',
       '<div class="mod-lg presentiel"><span class="mod-pastille">En ligne + en entreprise</span><b>La théorie en ligne, la pratique sur le terrain.</b> Les gestes du métier se pratiquent chez un professionnel près de chez vous ; l’examen officiel, quand il y en a un, se passe dans un centre d’examen.</div>')
PREVUES = {
    'care': ('Aide à la personne &amp; petite enfance', ['Accompagner la personne au quotidien', 'Soins d’hygiène et gestes professionnels', 'Accompagner le jeune enfant', 'ADVF — Assistant de vie aux familles (titre pro)'], 18),
    'code': ('Numérique &amp; développement web', ['Créer un site sans coder', 'Programmation : JavaScript &amp; logique', 'Tout savoir sur l’IA', 'Cybersécurité : les fondamentaux'], 14),
    'build': ('Bâtiment &amp; rénovation énergétique', ['Lire un plan &amp; préparer le chantier', 'Gestes techniques : électricité &amp; plomberie', 'Rénovation énergétique', 'Diagnostic de performance énergétique'], 19),
    'drive': ('Transport &amp; logistique', ['Code &amp; réglementation transport', 'Logistique d’entrepôt &amp; CACES', 'Capacité de transport léger', 'Chauffeur VTC (examen théorique)'], 17),
    'manage': ('Gestion, comptabilité &amp; secrétariat', ['Secrétariat &amp; communication professionnelle', 'Comptabilité : les fondamentaux', 'Paie &amp; administration du personnel', 'Bureautique &amp; IA de bureau'], 18),
}
NOMS = {'cook': 'Cook', 'sell': 'Sell', 'care': 'Care', 'code': 'Code', 'build': 'Build', 'drive': 'Drive', 'manage': 'Manage'}
# carte de Cook : le vrai catalogue
rep_re(r'(<div class="ecole e-cook rv">\s*<div class="ecole-head">\s*<span class="ecole-ic">(?:(?!</span>).)*</span>\s*)<h3>SWIPE AND COOK<small>Cuisine &amp; métiers de bouche</small></h3></div>.*?<a class="btn" href="swipe-and-cook-plateforme.html">Entrer dans l\'école</a>',
       r'\1' + f'''<h3>COOK<small>Cuisine, pâtisserie, bar &amp; hôtellerie</small></h3></div>
      <span class="tag-etat">École ouverte</span>
      <ul>
        <li><b>CAP Cuisine intensif</b><span>6 mois · nouveau</span></li>
        <li><b>CAP Cuisine, candidat libre</b><span>1 290 €</span></li>
        <li><b>CAP Pâtissier, candidat libre</b><span>1 290 €</span></li>
        <li><b>Hygiène alimentaire &amp; HACCP</b><span>290 €</span></li>
        <li><b>+ 46 autres formations</b><span>à découvrir dans l’école</span></li>
      </ul>
      <div class="ecole-meta"><span>{NB_F} formations</span><span>{NB_L} leçons</span><span>{NB_X} examens blancs</span></div>
      <a class="btn" href="{COOK}/">Entrer dans l'école</a>''')
# carte de Sell : le vrai catalogue
rep_re(r'(<div class="ecole e-sell rv">\s*<div class="ecole-head">\s*<span class="ecole-ic">(?:(?!</span>).)*</span>\s*)<h3>SWIPE AND SELL<small>.*?</small></h3></div>.*?<a class="btn" href="swipe-and-sell-plateforme.html">Entrer dans l\'école</a>',
       r'\1' + f'''<h3>SELL<small>Vente, commerce &amp; e-commerce</small></h3></div>
      <span class="tag-etat">École ouverte</span>
      <ul>
        {''.join(f'<li><b>{E(x)}</b><span>{next(f["duree"] for f in FS["formations"] if f["nom"] == x)}</span></li>' for x in FS['vitrine'])}
        <li><b>+ {SB_F - len(FS['vitrine'])} autres formations</b><span>à découvrir dans l’école</span></li>
      </ul>
      <div class="ecole-meta"><span>{SB_F} formations</span><span>{SB_L} leçons</span><span>{SB_X} examens blancs</span></div>
      <a class="btn" href="{SELL}/">Entrer dans l'école</a>''')
for k, (dom, liste, n) in PREVUES.items():
    rep_re(r'<div class="ecole e-' + k + r' rv">(\s*<div class="ecole-head">\s*<span class="ecole-ic">(?:(?!</span>).)*</span>\s*)<h3>SWIPE AND [A-Z]+<small>.*?</small></h3></div>.*?<a class="btn" href="swipe-and-' + k + r'-plateforme.html">Entrer dans l\'école</a>',
           f'<div class="ecole e-{k} bientot rv">' + r'\1' + f'''<h3>{NOMS[k].upper()}<small>{dom}</small></h3></div>
      <span class="tag-etat">Ouverture prochaine</span>
      <ul>
        {''.join(f'<li><b>{x}</b></li>' for x in liste)}
        <li><b>{n} formations prévues</b></li>
      </ul>
      <div class="ecole-meta"><span>Programme en préparation</span></div>
      <a class="btn" href="{prevenir(NOMS[k])}">Être prévenu de l’ouverture</a>''')
assert 'SWIPE AND' not in h[h.find('<section id="ecoles">'):h.find('<section id="quiz"')], 'nom restant dans les écoles'

# ------------------------------------------------------------------ parcours
rep('<p class="sec-sub rv">De la candidature à l\'emploi, vous êtes accompagné à chaque étape — c\'est la même promesse dans nos sept écoles.</p>',
    '<p class="sec-sub rv">De la demande d’inscription à l’examen, vous savez toujours où vous en êtes : c’est la même méthode dans toutes nos écoles.</p>')
rep_re(r'<div class="etape rv"><div class="pt">1</div>.*?</div>\s*<div class="etape rv"><div class="pt">2</div>.*?</div>\s*<div class="etape rv"><div class="pt">3</div>.*?</div>\s*<div class="etape rv"><div class="pt">4</div>.*?</div>',
       '''<div class="etape rv"><div class="pt">1</div><h4>Demande</h4><p>Une demande en ligne, puis un entretien pour choisir la bonne formation. Réponse du centre sous 15 jours, aucun diplôme exigé pour suivre la plupart des formations.</p></div>
      <div class="etape rv"><div class="pt">2</div><h4>Financement</h4><p>Aujourd’hui : financement personnel ou par votre employeur. Le CPF, les OPCO et France Travail viendront après la certification Qualiopi de l’école, en cours de préparation.</p></div>
      <div class="etape rv"><div class="pt">3</div><h4>Formation</h4><p>Les cours en ligne sur la plateforme de votre école, avec un formateur joignable ; la pratique en entreprise près de chez vous, que nous cherchons avec vous.</p></div>
      <div class="etape rv"><div class="pt">4</div><h4>Examen</h4><p>Pour un diplôme, vous vous présentez à l’examen officiel en candidat libre : nous vous y préparons avec des examens blancs. Les formations courtes délivrent une attestation.</p></div>''')

# ------------------------------------------------------------------ témoignages → l'offre qui distingue Cook : le CAP Cuisine intensif
rep_re(r'<section id="temoignages">.*?</section>', f'''<section id="intensif">
  <div class="wrap">
    <h2 class="sec-titre rv">Nouveau à Cook : le CAP Cuisine intensif<span class="tiret"></span></h2>
    <p class="sec-sub rv">Six mois pour se préparer au CAP Cuisine sans quitter sa région : toute la théorie en ligne, la pratique dans un restaurant près de chez vous, et un objectif clair, l’examen.</p>
    <div class="intensif-grid">
      <div class="carte rv"><b>En ligne, à un rythme soutenu</b>Les deux pôles du CAP Cuisine, les fiches techniques, les quiz et les examens blancs, avec un formateur du métier joignable par la messagerie.</div>
      <div class="carte rv"><b>En restaurant, près de chez vous</b>Depuis la session 2026, le candidat libre doit justifier d’au moins 4 semaines en restaurant pour le pôle 1 et 10 semaines pour le pôle 2. Nous cherchons avec vous un restaurateur partenaire près de chez vous.</div>
      <div class="carte rv"><b>Jusqu’à l’examen</b>L’inscription à l’examen se fait une fois par an, à l’automne, auprès de votre académie : vous la faites vous-même, nous vous guidons. Le diplôme est délivré par l’Éducation nationale.</div>
    </div>
    <div class="intensif-cta rv"><a class="btn btn-m" href="{COOK}/#inscription">Demander un rendez-vous</a><a class="btn btn-ghost" href="{COOK}/formations/cap-cuisine.html">Voir le programme du CAP Cuisine</a><small>Tarif et calendrier de la prochaine session : lors de l’entretien.</small></div>
  </div>
</section>''')

# ------------------------------------------------------------------ méthode (ce qui existe sur la plateforme de Cook)
rep('<h2 class="sec-titre rv">La méthode Swipe and Learn<span class="tiret"></span></h2>', '<h2 class="sec-titre rv">La méthode Swipe Learn School<span class="tiret"></span></h2>')
rep('<p class="sec-sub rv">Une plateforme e-learning identique dans les sept écoles, pensée pour apprendre du bout des doigts et aller jusqu\'à la certification.</p>',
    '<p class="sec-sub rv">La même plateforme dans chaque école, pensée pour apprendre sur téléphone et aller jusqu’à l’examen.</p>')
for a, b in [
    ('<p>Des leçons courtes en cartes à swiper, avec encadrés « repère » de professionnels, à suivre depuis le téléphone entre deux moments de la journée.</p>', '<p>Des leçons courtes qui tiennent en quelques minutes, avec l’essentiel à retenir, le piège à éviter et une mise en pratique, à suivre sur téléphone, tablette ou ordinateur.</p>'),
    ('<p>Chaque pôle se termine par un quiz de dix questions et deux examens blancs (mi-parcours et final) pour s\'entraîner dans les conditions du diplôme.</p>', '<p>Des quiz à chaque étape et des examens blancs pour s’entraîner dans les conditions de l’examen.</p>'),
    ('<h4>Planning de formation</h4>', '<h4>Votre itinéraire</h4>'),
    ('<p>Un rétroplanning se génère automatiquement selon la durée de votre parcours : vous savez semaine par semaine ce qu\'il reste à travailler.</p>', '<p>Vous avancez station par station et vous voyez toujours votre prochain arrêt ; des révisions espacées reviennent sur ce qui doit être retenu.</p>'),
    ('<h4>Émargement DocuSign</h4>', '<h4>Émargement électronique</h4>'),
    ('<p>Les feuilles de présence sont signées électroniquement via DocuSign, avec certificat de preuve : un émargement conforme, sans papier, pour les organismes financeurs.</p>', '<p>Vos présences se signent en ligne, avec une preuve horodatée : sans papier, et prêtes pour les financeurs le jour où l’école sera certifiée Qualiopi.</p>'),
    ('<h4>Classe virtuelle &amp; visio</h4>', '<h4>Un formateur joignable</h4>'),
    ('<p>Des rendez-vous en direct avec les formateurs complètent l\'e-learning : questions, corrections et entraînement à l\'oral avant les épreuves.</p>', '<p>Une messagerie avec le centre pour vos questions et vos travaux ; le formateur suit votre progression.</p>'),
    ('<h4>Un référent dédié</h4>', '<h4>Une équipe qui vous suit</h4>'),
    ('<p>Un accompagnateur suit votre progression du premier jour à l\'emploi : motivation, financement, stages et mise en relation avec les employeurs.</p>', '<p>L’équipe repère quand vous décrochez, vous relance et vous aide à trouver une entreprise pour la pratique.</p>'),
]:
    rep(a, b)

# ------------------------------------------------------------------ métiers et comparateur (données réelles de Cook)
rep('<p class="sec-sub rv">Missions réelles, salaires indicatifs, débouchés et formation associée. Cliquez sur un métier pour voir sa fiche complète.</p>',
    '<p class="sec-sub rv">Les métiers de Cook et de Sell : missions, débouchés et formation associée. Les métiers des autres écoles arriveront avec leur ouverture.</p>')
rep('<p class="sec-sub rv">Durée, niveau, rythme et financement : filtrez pour trouver le parcours qui colle à votre situation.</p>',
    f'<p class="sec-sub rv">Les formations de Cook et de Sell : niveau, durée indicative et prix par stagiaire. Filtrez pour trouver celle qui vous correspond.</p>')

# ------------------------------------------------------------------ financement et reconversion : aujourd'hui, et après Qualiopi
rep_re(r'<div class="guide-fin">.*?</div>\s*(?=<aside class="reconv rv">)', '''<div class="guide-fin">
        <details class="gcard rv" open>
          <summary><span class="gc-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/></svg></span><span class="gc-t"><b>Aujourd’hui</b><small>Financement personnel ou employeur</small></span></summary>
          <div class="gc-body"><p>Vous pouvez financer vous-même votre formation, ou la faire payer par votre employeur sur son propre budget de formation. Le prix est affiché sur chaque fiche de formation.</p><p><b class="hl">Entreprises :</b> devis sur demande pour former vos équipes.</p></div>
        </details>
        <details class="gcard rv">
          <summary><span class="gc-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/></svg></span><span class="gc-t"><b>Après Qualiopi</b><small>CPF, OPCO, France Travail</small></span></summary>
          <div class="gc-body"><p>Les financements publics (CPF, OPCO, France Travail) exigent que l’organisme soit certifié Qualiopi. L’école prépare cette certification : tant qu’elle n’est pas obtenue, nous ne vous les proposons pas.</p><p><b class="hl">Bon à savoir :</b> le CPF finance les formations qui mènent à une certification enregistrée, comme un CAP ou un titre professionnel.</p></div>
        </details>
      </div>
      ''')
rep('<li><div><b>Clarifiez votre projet</b><p>Nos conseillers et le quiz d\'orientation vous aident à cibler le métier réaliste et motivant pour vous.</p></div></li>',
    '<li><div><b>Clarifiez votre projet</b><p>Le test d’orientation et un entretien avec l’école vous aident à cibler un métier réaliste et motivant pour vous.</p></div></li>')
rep('<li><div><b>Vérifiez le marché</b><p>Privilégiez un métier qui recrute près de chez vous : nos sept écoles ciblent des secteurs en tension.</p></div></li>',
    '<li><div><b>Vérifiez le marché</b><p>Privilégiez un métier qui recrute près de chez vous : renseignez-vous auprès des employeurs et des offres d’emploi de votre secteur.</p></div></li>')
rep('<li><div><b>Sécurisez le financement</b><p>CPF, alternance, France Travail : on identifie ensemble la solution qui évite l\'avance de frais.</p></div></li>',
    '<li><div><b>Prévoyez le financement</b><p>Aujourd’hui, personnel ou par votre employeur ; les financements publics viendront après la certification Qualiopi de l’école.</p></div></li>')
rep('<li><div><b>Formez-vous à votre rythme</b><p>E-learning mobile, classes virtuelles et stages : compatible avec une vie active.</p></div></li>',
    '<li><div><b>Formez-vous à votre rythme</b><p>Les leçons en ligne quand vous le pouvez, la pratique en entreprise près de chez vous : compatible avec une vie active.</p></div></li>')
rep('<li><div><b>Décrochez l\'emploi</b><p>Certification, préparation aux entretiens et mise en relation avec notre réseau d\'employeurs.</p></div></li>',
    '<li><div><b>Visez l’examen</b><p>Pour un diplôme, l’examen officiel en candidat libre, préparé avec nos examens blancs ; pour une formation courte, une attestation.</p></div></li>')
rep('<h2 class="sec-titre rv">Financer &amp; réussir sa reconversion<span class="tiret"></span></h2>', '<h2 class="sec-titre rv">Financer et réussir sa reconversion<span class="tiret"></span></h2>')
rep('<p class="sec-sub rv">Tout ce qu\'il faut savoir pour financer sa formation et réussir son changement de voie, expliqué simplement.</p>',
    '<p class="sec-sub rv">Ce qui est possible aujourd’hui, ce qui viendra après Qualiopi, et les étapes d’un changement de métier.</p>')

# ------------------------------------------------------------------ questions fréquentes
rep_re(r'<div class="faq-list">.*?</div>\s*</div>\s*</section>', '''<div class="faq-list">
      <details class="faq-item rv"><summary>Faut-il un diplôme pour s'inscrire ?</summary><div class="faq-c"><p>Non pour suivre la plupart des formations : il faut lire et écrire le français et disposer d’un ordinateur, d’une tablette ou d’un téléphone connecté. Les conditions d’accès aux examens officiels, quand il y en a, vous sont précisées à l’entretien.</p></div></details>
      <details class="faq-item rv"><summary>Les formations sont-elles finançables par le CPF ?</summary><div class="faq-c"><p>Pas encore : le CPF, les OPCO et France Travail exigent la certification Qualiopi, que l’école prépare. Aujourd’hui, le financement est personnel ou assuré par votre employeur.</p></div></details>
      <details class="faq-item rv"><summary>Comment se déroule concrètement la formation ?</summary><div class="faq-c"><p>Vous suivez les leçons, les quiz et les examens blancs sur la plateforme de votre école, avec un formateur joignable par la messagerie. Quand la formation comporte de la pratique, elle se fait en entreprise, près de chez vous.</p></div></details>
      <details class="faq-item rv"><summary>Où se fait la pratique ?</summary><div class="faq-c"><p>Près de chez vous, chez un professionnel partenaire que nous cherchons avec vous : un restaurant pour Cook, par exemple. Le siège de l’école est à Saint-Étienne.</p></div></details>
      <details class="faq-item rv"><summary>Puis-je me former tout en travaillant ?</summary><div class="faq-c"><p>Oui. Les leçons sont courtes et se suivent quand vous le pouvez, sur téléphone. Pour aller plus vite vers le CAP Cuisine, il existe aussi le CAP Cuisine intensif, en six mois.</p></div></details>
      <details class="faq-item rv"><summary>Les diplômes sont-ils délivrés par l’école ?</summary><div class="faq-c"><p>Non. Les diplômes préparés (CAP, BP, certificats de spécialisation, titres professionnels) sont délivrés par l’État ou leur certificateur après l’examen ; l’école vous y prépare. Les formations courtes délivrent une attestation de fin de formation et un certificat de réalisation.</p></div></details>
      <details class="faq-item rv"><summary>Les formations sont-elles accessibles en situation de handicap ?</summary><div class="faq-c"><p>Contactez-nous dès votre demande : nous étudions avec vous l’adaptation du parcours (rythme, supports, conditions de pratique).</p></div></details>
    </div>
  </div>
</section>''')

# ------------------------------------------------------------------ bloc financement, appel final, pied de page
rep_re(r'<section id="financement" class="financement">.*?</section>', '')
rep('<p>Nos conseillers en formation vous aident à choisir le parcours adapté à votre projet, votre rythme et votre financement — entretien gratuit et sans engagement.</p>',
    '<p>Parlons de votre projet : un entretien pour choisir la formation adaptée à votre métier visé, à votre rythme et à votre budget.</p>')
rep('<a class="btn btn-m" href="#contact">Être rappelé par un conseiller</a>', f'<a class="btn btn-m" href="{COOK}/#inscription">Demander un rendez-vous</a>')
rep('<b class="baloo" style="color:var(--creme);letter-spacing:.05em">SWIPE AND LEARN</b>', '<b class="baloo" style="color:var(--creme);letter-spacing:.05em">SWIPE LEARN SCHOOL</b>')
rep('<p style="font-size:.88rem;max-width:36ch">Le groupe de formation aux métiers qui recrutent. Sept écoles, une méthode, des certifications reconnues.</p>',
    '<p style="font-size:.88rem;max-width:36ch">Organisme de formation. Sept écoles, une méthode : la théorie en ligne, la pratique sur le terrain.</p>')
rep('<p style="margin-top:12px;font-size:.88rem">15 rue des Écoles — 69000 Lyon<br>contact@swipeandlearn.com · 04 00 00 00 00</p>',
    f'<p style="margin-top:12px;font-size:.88rem">40 rue de la Badouillère, 42000 Saint-Étienne<br><a href="mailto:{CONTACT}" style="color:inherit">{CONTACT}</a></p>')
rep_re(r'<li><i style="background:var\(--cook\)"></i><a href="swipe-and-cook-plateforme.html">Swipe and Cook — Cuisine</a></li>',
       f'<li><i style="background:var(--cook)"></i><a href="{COOK}/">Cook : cuisine, pâtisserie, bar et hôtellerie</a></li>')
rep(f'<li><i style="background:var(--sell)"></i><a href="swipe-and-sell-plateforme.html">Swipe and Sell — Vente &amp; e-commerce</a></li>',
    f'<li><i style="background:var(--sell)"></i><a href="{SELL}/">Sell : vente, commerce et e-commerce</a></li>')
for k, lib in [('care', 'Santé'), ('code', 'Numérique'), ('build', 'Bâtiment'), ('drive', 'Transport'), ('manage', 'Gestion &amp; secrétariat')]:
    nouveau = {'care': 'Aide à la personne'}.get(k, lib)
    rep(f'<li><i style="background:var(--{k})"></i><a href="swipe-and-{k}-plateforme.html">Swipe and {NOMS[k]} — {lib}</a></li>',
        f'<li><i style="background:var(--{k})"></i><span>{NOMS[k]} : {nouveau}, bientôt</span></li>')
rep('<li><a href="#guide">Financements</a></li>', '<li><a href="#guide">Financement</a></li>')
rep('<li><a href="#">Accessibilité &amp; handicap</a></li>', '<li><a href="#faq">Accessibilité &amp; handicap</a></li>')
rep_re(r'<div class="legal">.*?</div>',
       '<div class="legal">SWIPE LEARN SCHOOL, SAS · SIRET 131 294 969 00012 · 40 rue de la Badouillère, 42000 Saint-Étienne · Directeur de la publication : Idriss ROUGAI · '
       'Déclaration d’activité d’organisme de formation en cours d’enregistrement · Démarche de certification Qualiopi en cours · Site hébergé par Netlify.</div>')

# ------------------------------------------------------------------ script : écoles, métiers, comparateur, test d'orientation
ECOLES_JS = "const ECOLES={\n" + ",\n".join(
    f"  {k}:{{nom:'{NOMS[k]}',dom:'{d}',url:'{u}',ouvert:{'true' if k in ('cook', 'sell') else 'false'}}}"
    for k, d, u in [('cook', 'Cuisine, pâtisserie, bar & hôtellerie', COOK + '/'), ('sell', 'Vente, commerce & e-commerce', SELL + '/'), ('care', 'Aide à la personne & petite enfance', prevenir('Care')),
                    ('code', 'Numérique & développement web', prevenir('Code')), ('build', 'Bâtiment & rénovation énergétique', prevenir('Build')), ('drive', 'Transport & logistique', prevenir('Drive')),
                    ('manage', 'Gestion, comptabilité & secrétariat', prevenir('Manage'))]) + "\n};"
rep_re(r'const ECOLES=\{.*?\n\};', ECOLES_JS.replace('\\', '\\\\'))
METIERS = [
    ('Cuisinier', 'CAP Cuisine', 'cuisinier', "Composer, cuisiner et dresser des plats en respectant les règles d’hygiène, du bistrot au restaurant gastronomique.", ['Préparer les entrées, plats et desserts', 'Gérer les cuissons et le dressage', 'Appliquer les règles d’hygiène (HACCP)', 'Gérer les stocks et l’économat'], 'Restaurants, collectivités, hôtels, traiteurs, en France comme à l’étranger.'),
    ('Pâtissier', 'CAP Pâtissier', 'patissier', "Réaliser entremets, viennoiseries et desserts avec la précision d’un métier où tout se pèse.", ['Réaliser crèmes, pâtes et montages', 'Travailler le chocolat et le sucre', 'Assurer la régularité et l’hygiène', 'Créer et dresser des desserts'], 'Pâtisseries, boulangeries, restaurants, hôtels.'),
    ('Boulanger', 'CAP Boulanger', 'boulanger', "Maîtriser la farine, la fermentation et la cuisson pour les pains et les viennoiseries.", ['Pétrir, façonner et cuire', 'Gérer les fermentations', 'Réaliser les viennoiseries', 'Organiser sa production'], 'Boulangeries artisanales, grandes surfaces, restauration.'),
    ('Traiteur', 'Métier de traiteur', 'traiteur', "Préparer et livrer des repas pour les événements : cocktails, buffets, plateaux.", ['Concevoir des menus et des devis', 'Produire en quantité et en sécurité', 'Organiser la livraison et le service', 'Respecter la chaîne du froid'], 'Traiteurs, réceptions, création de sa propre activité.'),
    ('Barman et serveur', 'CS Métiers du bar', 'bar-salle', "Accueillir, conseiller, servir et créer des cocktails : les métiers qui font l’expérience du client.", ['Accueillir et conseiller', 'Réaliser les cocktails et les boissons', 'Servir en salle', 'Encaisser et respecter les obligations'], 'Bars, restaurants, hôtels, événementiel.'),
    ('Réceptionniste', 'Titre pro Réceptionniste', 'hotellerie', "Accueillir les clients d’un hôtel, gérer les réservations et le séjour.", ['Accueillir et informer les clients', 'Gérer les réservations', 'Assurer la facturation', 'Traiter les demandes et réclamations'], 'Hôtels, résidences de tourisme, hôtellerie de plein air.'),
]
metiers_js = "const METIERS=[\n" + ",\n".join(
    ["  {ec:'cook',nom:%s,for:%s,url:%s,pitch:%s,miss:%s,deb:%s}" % tuple(json.dumps(x, ensure_ascii=False) for x in (n, f, f'{COOK}/metiers/{s}.html', p, m, d))
     for n, f, s, p, m, d in METIERS] +
    ["  {ec:'sell',nom:%s,for:%s,url:%s,pitch:%s,miss:%s,deb:%s}" % tuple(json.dumps(x, ensure_ascii=False) for x in (m['nom'], m['formation'], f"{SELL}/metiers/{m['s']}.html", m['pitch'], m['missions'][:4], m['deb']))
     for m in FS['metiers']]) + "\n];"
rep_re(r'const METIERS=\[.*?\n\];', metiers_js.replace('\\', '\\\\'))
rep("const METIER_PHARE={\n  cook:'Cuisinier',sell:'Conseiller de vente',care:'Assistant de vie aux familles',", "const METIER_PHARE={\n  cook:'Cuisinier',sell:'Conseiller de vente',care:'Assistant de vie aux familles',")
# fiches métiers : plus de salaires ni de niveaux de demande (non sourcés) ; lien vers la page métier de Cook
rep('<div class="mcard-stats"><span><i>●</i> ${m.sal}</span><span><i>●</i> Demande : ${m.dem}</span></div>', '<div class="mcard-stats"><span>${m.for}</span></div>')
rep_re(r'<div class="mmodal-stats">.*?</div>\s*</div>\s*(?=<h5>Le métier</h5>)', '<div class="mmodal-stats"><div><b>${m.for}</b><small>Formation associée</small></div></div>\n      ')
rep('<a class="btn btn-m mmodal-cta" href="${e.url}">Découvrir la formation', '<a class="btn btn-m mmodal-cta" href="${m.url}">Découvrir le métier et ses formations')
rep_re(r'<p style="font-size:\.74rem;color:var\(--taupe\);margin-top:14px">Salaires et niveaux de demande.*?</p>', '')
# comparateur : les 50 formations de Cook, prix au lieu du financement
form_js = "const FORMATIONS=" + json.dumps([{'ec': 'cook', **x} for x in F] + [{'ec': 'sell', **x} for x in FS['formations']], ensure_ascii=False) + ";"
rep_re(r'const FORMATIONS=\[.*?\n\];', form_js.replace('\\', '\\\\'))
rep_re(r'const FILTRES=\[.*?\n\];', '''const FILTRES=[
  {id:'tous',lab:'Toutes'},
  {id:'diplo',lab:'Préparation à un diplôme',test:f=>['CAP','BP','CS','Titre pro','Bac pro','BTS'].includes(f.niv)},
  {id:'module',lab:'Modules de diplôme',test:f=>f.niv==='Module'},
  {id:'court',lab:'Formations courtes',test:f=>f.niv==='Courte'}
];''')
rep('<span>Formation</span><span>Niveau</span><span>Durée</span><span>Rythme</span><span></span>', '<span>Formation</span><span>Niveau</span><span>Durée</span><span>Prix</span><span></span>')
rep('<span class="comp-cell mut" data-l="Rythme">${f.rythme}</span>', '<span class="comp-cell mut" data-l="Prix">${f.prix}</span>')
rep('<a class="btn-mini" href="${ECOLES[f.ec].url}">Voir</a>', '<a class="btn-mini" href="${f.url}">Voir</a>')
# test d'orientation : une école encore fermée propose d'être prévenu
rep("  const forms=FORMATIONS.filter(f=>f.ec===top).slice(0,3).map(f=>f.nom);", "  const forms=e.ouvert?FORMATIONS.filter(f=>f.ec===top).slice(0,3).map(f=>f.nom):[];")
rep('<p class="res-desc">D’après vos réponses, c’est vers ce métier et cette école que votre profil penche le plus. Explorez les formations pour vous faire une idée concrète.</p>',
    '<p class="res-desc">${e.ouvert?"D’après vos réponses, c’est vers ce métier et cette école que votre profil penche le plus. Explorez les formations pour vous faire une idée concrète.":"D’après vos réponses, c’est vers ce métier que votre profil penche le plus. Cette école ouvre bientôt : écrivez-nous pour être prévenu de son ouverture."}</p>')
rep('<a class="btn btn-m" href="${e.url}">Découvrir ${e.nom}', '<a class="btn btn-m" href="${e.url}">${e.ouvert?"Découvrir "+e.nom:"Être prévenu de l’ouverture"}')
rep('<p style="font-size:.74rem;color:#C9BE9E;margin-top:18px">Ce test est indicatif et ne remplace pas un entretien d’orientation. Nos conseillers affinent votre projet avec vous.</p>',
    '<p style="font-size:.74rem;color:#C9BE9E;margin-top:18px">Ce test est indicatif et ne remplace pas un entretien d’orientation.</p>')
# plus de renvoi par script vers des adresses de maquette : les liens sont de vrais liens
rep_re(r'<script>\s*\(function\(\)\{\s*var ADRESSES=.*?\}\)\(\);\s*</script>', '')

# ------------------------------------------------------------------ passage de design (outils/style_gout.py)
import sys
sys.path.insert(0, ICI)
import style_gout as SG
rep_re(r'<link[^>]*fonts\.googleapis\.com/css2[^>]*>', SG.precharger() + '<style>' + SG.faces() + '</style>')
rep_re(r'<link rel="preconnect"[^>]*>\s*', '', n=h.count('<link rel="preconnect"'))
h = re.sub(r'<style>(.*?)</style>', lambda m: '<style>' + (m.group(1) if '@font-face' in m.group(1) or 'SL_' in m.group(1) else SG.nettoyer(m.group(1))) + '</style>', h, flags=re.S)
rep('</head>', SG.STYLE + '\n</head>')
# méthode : les six points sans icônes, à côté de vrais écrans de la plateforme de Cook
def _methode(m):
    items = re.sub(r'\s*<span class="meth-ic">.*?</span>', '', m.group(1), flags=re.S)
    return '<div class="meth-split">\n      ' + SG.ECRANS + '\n      <div class="meth-liste">' + items + '</div>\n    </div>\n  </div>\n</section>'
rep_re(r'<div class="meth-grid">(.*?)</div>\s*</div>\s*</section>', _methode)
rep_re(r'(<div class="intensif-grid">.*?</div>\s*</div>)(\s*<div class="intensif-cta)', lambda m: '<div class="intensif-split">' + m.group(1) + SG.EXAMEN + '</div>' + m.group(2))
# métiers : plus de pastille d'icône
rep('<span class="mcard-ic">${svg(m.ec)}</span>', '')
rep_re(r'(<span class="mcard-more">Voir la fiche métier)\s*<svg.*?</svg>', r'\1')
# pied de page : le nom revient en grand
rep('<div class="legal">', '<p class="f-nom">Swipe Learn School</p>\n    <div class="legal">')

# ------------------------------------------------------------------ téléphone et application installable (outils/mobile_appli.py)
import mobile_appli as MA
rep('</head>', MA.tete() + '\n' + MA.STYLE + '\n</head>')
rep('<li><a href="#faq">Accessibilité &amp; handicap</a></li>',
    '<li><a href="#faq">Accessibilité &amp; handicap</a></li>\n        <li><a href="#" id="sl-installer-lien">Installer l’application</a></li>')
rep('</body>', MA.SCRIPT + '\n</body>')
rep('setInterval(()=>allerA((cIdx+1)%slides.length),2600)', 'setInterval(()=>allerA((cIdx+1)%slides.length),1700)')
rep('const COMP_MAX=12;', "const COMP_MAX=window.matchMedia('(max-width:700px)').matches?6:12;")
# typographie : pas de « ? » seul en début de ligne dans les questions
h = re.sub(r'(<summary>[^<]*?) \?</summary>', lambda m: m.group(1) + '&nbsp;?</summary>', h)

# ------------------------------------------------------------------ contrôles
for interdit in ['Swipe and', 'SWIPE AND', 'swipeandlearn.com', '04 00 00 00 00', 'maquette', 'DocuSign', 'plateforme.html', 'Éligible CPF', '100 %', 'témoign', 'sans avance de frais', 'Lyon<br>']:
    assert interdit not in h, 'reste : ' + interdit
os.makedirs(os.path.join(RAC, 'public'), exist_ok=True)
open(os.path.join(RAC, 'public/index.html'), 'w', encoding='utf-8').write(h)
open(os.path.join(RAC, 'public/robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(RAC, 'public/sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{SITE}/</loc><priority>1.0</priority></url>\n</urlset>\n')
open(os.path.join(RAC, 'public/404.html'), 'w', encoding='utf-8').write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page introuvable · Swipe Learn School</title><meta name="robots" content="noindex"></head><body style="font-family:Nunito,Arial,sans-serif;padding:40px;color:#2E2415;background:#FAF6EE"><h1>Cette page n’existe pas</h1><p><a href="/">Retour à l’accueil de Swipe Learn School</a> · <a href="{COOK}/">Cook, l’école de cuisine</a></p></body></html>')
# icônes du groupe : l'or du groupe (même dessin que dans le pilote)
import shutil
shutil.copy(os.path.join(ICI, 'source', 'favicon-groupe.ico'), os.path.join(RAC, 'public', 'favicon.ico'))
shutil.copy(os.path.join(ICI, 'source', 'icone-groupe.svg'), os.path.join(RAC, 'public', 'logos', 'icone-groupe.svg'))
SG.copier_polices(os.path.join(ICI, 'source', 'polices'), os.path.join(RAC, 'public'))
MA.fichiers(os.path.join(RAC, 'public'), DESC, [('Nos écoles', '/#ecoles'), ('Test d’orientation', '/#quiz'), ('Comparer les formations', '/#comparateur')])
open(os.path.join(RAC, 'netlify.toml'), 'w').write('[build]\n  publish = "public"\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Content-Type-Options = "nosniff"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n'
                                                   '\n[[headers]]\n  for = "/sw.js"\n  [headers.values]\n    Cache-Control = "no-cache"\n')
print('ok', len(h))
