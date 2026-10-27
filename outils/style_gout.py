# Passage de design (tasteskill) sur le site du groupe : moins d'effets génériques, plus de matière vraie.
# - polices servies par le site (Baloo 2 et Nunito, licence OFL) : plus de dépendance à Google Fonts, et
#   l'application installée garde ses polices hors connexion ;
# - une couleur de fond « os » neutre, l'or du groupe pour l'action, l'encre brune pour le texte ;
# - ni ombres, ni dégradés, ni filets, ni petites étiquettes en capitales, ni cartes coiffées d'icônes ;
# - la méthode montrée avec de vrais écrans de la plateforme de Cook (contenus réels du CAP Cuisine).
import os, re, shutil

LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'
POLICES = [('Baloo 2', 'baloo-2', w) for w in (600, 700, 800)] + [('Nunito', 'nunito', w) for w in (400, 700, 800)]


def faces():
    out = []
    for fam, fic, w in POLICES:
        for sous, plage in (('latin-ext', LATIN_EXT), ('latin', LATIN)):
            out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};"
                       f"src:url(/polices/{fic}-{sous}-{w}-normal.woff2) format('woff2');unicode-range:{plage}}}")
    return '\n'.join(out)


def precharger():
    return ''.join(f'<link rel="preload" href="/polices/{f}" as="font" type="font/woff2" crossorigin>'
                   for f in ('baloo-2-latin-800-normal.woff2', 'nunito-latin-400-normal.woff2'))


def copier_polices(source, public):
    d = os.path.join(public, 'polices')
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(source):
        shutil.copy(os.path.join(source, f), d)


STYLE = r'''<style>/* SL_GOUT : passage de design */
:root{--creme:#F2F1EE;--beige:#E8E6E1;--beige-f:#D3CEC4;--blanc:#FFFFFF;--encre:#2A2116;--taupe:#5A5143;--moutarde-f:#7A5D12;--fond-sombre:#2B2213}
html{-webkit-text-size-adjust:100%}
body{background:var(--creme);color:var(--encre);font-size:16px;line-height:1.6}
button,input,select,textarea{font-family:inherit}
/* plus d'ombres au repos ni de flou (seules la barre de navigation, la fenêtre métier et le bandeau d'installation flottent) */
body *:not(nav):not(.mmodal-card):not(#sl-installer):not(.ui){box-shadow:none!important;text-shadow:none!important}
/* barre du haut brun foncé : le logo doré (celui du favicon) ressort */
nav{background:var(--fond-sombre);border-bottom:0}
nav ul a{color:#F2EDE2}
nav ul a:hover{color:var(--moutarde)}
nav ul.open a{color:var(--encre)}
nav ul.open a:hover{color:var(--moutarde-f)}
.brand b{color:#F2EDE2}
.brand .lg{background:var(--moutarde)}
.burger span{background:#F2EDE2}
.nav-cta{background:var(--moutarde)!important;color:var(--encre)!important}
nav.scrolled{box-shadow:0 1px 0 rgba(42,33,22,.08)} /* taste-skill-ignore : barre fixe ou écran réel de la plateforme */
/* ornements retirés : halos, arcs, ruban d'icônes, tirets sous les titres */
.hero::before,.hero::after,.grand-cta .arc,.quiz::before,.quiz::after,.scene .halo,.ruban,.sec-titre .tiret{display:none!important}
.slide:not(.on){visibility:hidden}
@media(prefers-reduced-motion:reduce){.slide:not(.on){display:none}}
/* marque : à plat */
.f-brand .lg{background:var(--moutarde)}
nav.scrolled{box-shadow:0 1px 0 rgba(0,0,0,.25)} /* taste-skill-ignore : barre fixe */
.brand small{text-transform:none;letter-spacing:0;font-size:14px;font-weight:700;color:#D9CFB8}
.brand b{letter-spacing:.01em}
/* titres : serrés, à gauche ; texte courant dans l'encre pleine, à 16 px et plus */
.sec-titre{text-align:left;letter-spacing:-.02em;line-height:1.05;font-size:clamp(2rem,3.6vw,3.2rem)}
.sec-sub{text-align:left;margin-left:0;margin-right:0;max-width:60ch;color:var(--encre);font-weight:400;font-size:18px;line-height:1.55}
.quiz .sec-titre,.quiz .sec-sub{text-align:left}
.quiz .sec-sub{color:#E9E1CF}
.hero p,.meth p,.etape p,.mcard-body p,.gc-body p,.faq-c p,.intensif-grid .carte{color:var(--encre)}
/* accueil */
.hero .wrap{grid-template-columns:1.2fr .8fr;gap:40px}
.sur{display:none}
.hero h1{font-size:clamp(2.6rem,5.4vw,5.4rem);line-height:1;letter-spacing:-.025em;word-spacing:0}
.hero .geste{margin:18px 0 0;font-family:'Baloo 2';font-weight:700;font-size:clamp(1.5rem,2.3vw,2.2rem);line-height:1.15;color:var(--moutarde-f)}
.hero .geste + p{margin-top:22px;font-size:18px;line-height:1.6;max-width:54ch}
.confiance{font-size:14px;color:var(--encre)}
.confiance svg{color:var(--moutarde-f)}
/* boutons : à plat, entièrement ronds */
.btn{box-shadow:none}
.btn-m{background:var(--moutarde);color:var(--encre)}
.btn-m:hover{background:#B88C22}
.btn-ghost{background:var(--beige);color:var(--encre);border-color:var(--beige)}
.btn-ghost:hover{background:var(--beige-f);border-color:var(--beige-f)}
.btn:focus-visible,.comp-filtre:focus-visible,.sl-points button:focus-visible{outline:3px solid var(--encre);outline-offset:3px}
/* écoles : sans pastille d'icône, couleurs de l'école assombries pour être lisibles */
.ecole{border:0!important;background:var(--blanc)}
.ecole-ic{display:none!important}
.ecole h3{font-size:1.5rem;letter-spacing:-.01em;color:color-mix(in srgb,var(--c) 70%,#000)}
.ecole h3 small{font-family:'Nunito';font-size:15px;font-weight:700;color:var(--encre);letter-spacing:0;text-transform:none}
.ecole .tag-etat,.ecole.bientot .tag-etat{text-transform:none;letter-spacing:0;font-family:'Nunito';font-size:14px;font-weight:800;color:color-mix(in srgb,var(--c) 55%,#000)}
.ecole li{background:var(--creme);font-size:15px}
.ecole li span{font-size:14px;color:var(--taupe)}
.ecole-meta span{font-family:'Nunito';font-size:14px;font-weight:800;color:color-mix(in srgb,var(--c) 62%,#000)}
.ecole .btn{background:color-mix(in srgb,var(--c) 70%,#000);color:#fff}
.mod-lg{border:0!important;font-size:15px;color:var(--encre)}
.mod-lg.distance,.mod-lg.presentiel{color:var(--encre)}
.mod-lg.distance{background:#E1ECE6}
.mod-lg.presentiel{background:#EFE5DA}
.mod-lg .mod-pastille{text-transform:none;letter-spacing:0;font-size:14px;background:var(--encre)!important;color:#fff!important}
/* chiffres */
.chiffres .l{font-size:14px;opacity:1;color:#E9E1CF}
/* test d'orientation : fond plein */
.quiz{background:var(--fond-sombre)}
.quiz-box{border:0!important;background:#3A2F1C}
.quiz-progress i{background:var(--moutarde)}
.quiz-box button,.quiz-box .opt,.quiz-box label{border-color:transparent!important}
/* parcours */
.etape .pt{border-width:3px}
.etape h4{font-size:1.15rem}
.etape p{font-size:16px}
/* CAP intensif : les trois points en liste, à côté d'un vrai écran d'examen blanc */
.intensif-split{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,.7fr);gap:48px;align-items:start;margin-top:26px}
.intensif-split .intensif-grid{grid-template-columns:1fr;gap:22px;margin-top:0}
.intensif-split .intensif-grid .carte{background:none;padding:0}
.intensif-ecran{margin:0}
.intensif-ecran figcaption{font-size:14px;color:var(--taupe);margin-top:8px}
/* questions fréquentes : le titre à gauche, les questions à droite */
.faq .wrap{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);column-gap:56px;align-items:start}
.faq .sec-titre,.faq .sec-sub{grid-column:1}
.faq-list{grid-column:2;grid-row:1/span 3;max-width:none;margin:0}
.intensif-grid .carte{border:0!important;background:var(--blanc);font-size:16px}
.intensif-cta small{font-size:14px;color:var(--taupe)}
/* méthode : de vrais écrans de Cook à gauche, les six points à droite */
.meth-split{display:flex;flex-direction:column;gap:48px;margin-top:8px}
.meth-ecrans{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;align-items:start}
.meth-ecrans figure{margin:0}
.meth-ecrans figcaption{font-size:14px;color:var(--taupe);margin-top:8px;line-height:1.4}
.meth-liste{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px 40px}
.meth-liste .meth{background:none;border:0!important;padding:0}
.meth-liste .meth h4{font-size:1.3rem;line-height:1.2;letter-spacing:-.01em}
.meth-liste .meth p{font-size:16px;line-height:1.6;margin-top:8px}
.meth-ic{display:none!important}
/* écrans de la plateforme (fragments d'interface réels, couleurs de Cook) */
.ui{--b:#2E5BE3;--i:#17265C;--j:#F2B01E;--f:#F8F4EE;font-family:'Nunito';background:#fff;color:var(--i);border-radius:18px;padding:18px;font-size:14px;line-height:1.45;border:1px solid #E6E1D7;box-shadow:0 18px 36px rgba(23,38,92,.10);min-height:230px} /* taste-skill-ignore : barre fixe ou écran réel de la plateforme */
.ui .ui-haut{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:800;color:#4A557F;margin-bottom:8px}
.ui .ui-haut i{width:8px;height:8px;border-radius:50%;background:var(--b)}
.ui b.ui-t{display:block;font-family:'Baloo 2';font-size:19px;line-height:1.2;margin-bottom:6px}
.ui .ui-bloc{background:var(--f);border-radius:12px;padding:9px 11px;margin-top:8px}
.ui .ui-bloc b{display:block;font-size:13px;margin-bottom:3px}
.ui .ui-bloc.piege{background:#FFF1D1}
.ui ul{margin:0;padding-left:16px}
.ui .ui-opt{display:block;border:1.5px solid #E3E7F5;border-radius:10px;padding:7px 10px;margin-top:6px;font-weight:700} /* taste-skill-ignore : barre fixe ou écran réel de la plateforme */
.ui .ui-opt.ok{border-color:#1E9E62;background:#E8F7EF}
.ui .ui-expl{margin-top:8px;font-size:13px;color:#33406E}
.ui .ui-barre{height:6px;border-radius:9px;background:#E3E7F5;overflow:hidden;margin:4px 0 10px}
.ui .ui-barre span{display:block;height:100%;background:var(--b)}
.ui ol{list-style:none;margin:0;padding:0;position:relative}
.ui ol li{display:flex;align-items:center;gap:9px;padding:5px 0;font-weight:700}
.ui ol li i{width:22px;height:22px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:13px;font-weight:800;background:#E3E7F5;color:#4A557F}
.ui ol li.fait i{background:var(--b);color:#fff}
.ui ol li.ici{color:var(--b)}
.ui ol li.ici i{background:var(--j);color:var(--i)}
.ui ol li small{margin-left:auto;font-size:13px;font-weight:700;color:#4A557F}
.ui .ui-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.ui .ui-chips span{background:var(--f);border-radius:99px;padding:4px 10px;font-weight:800;font-size:13px}
.ui .ui-bouton{display:block;text-align:center;margin-top:10px;background:var(--b);color:#fff;border-radius:99px;padding:8px;font-weight:800}
/* petites tailles relevées à 13 px et plus */
.slide small{font-size:14px;color:var(--encre)}
.quiz-count,.quiz-box small{font-size:14px}
.quiz-nav span{font-size:14px!important}
.comp-row .btn-mini{font-size:14px;background:var(--beige);color:var(--encre)}
.comp-row .btn-mini:hover{background:var(--moutarde)}
.gcard .gc-t small{font-size:14px;color:var(--taupe)}
.faq-c,.fin p{color:var(--encre)}
.intensif-grid .carte b{color:color-mix(in srgb,var(--cook) 72%,#000)}
/* métiers */
.mcard{border:0!important;background:var(--blanc)}
.mcard-ic{display:none!important}
.mcard-top b{font-size:1.3rem}
.mcard-top small{font-size:14px;color:var(--encre);letter-spacing:0}
.mcard-stats span{font-size:14px}
.mcard-more{font-size:15px}
/* comparateur : une table sans filets, une ligne sur deux teintée */
.comp-table{border:0!important;background:var(--blanc)}
.comp-row{border-bottom:0!important}
.comp-row:not(.comp-head):nth-child(odd){background:#F7F6F3}
.comp-head{text-transform:none;letter-spacing:0;font-family:'Nunito';font-size:14px;font-weight:800;color:var(--encre)}
.comp-row .cf-nom small{font-size:14px;color:var(--taupe)}
.comp-cell{font-size:15px}
.comp-cell.mut{color:var(--encre)}
.comp-badge{font-size:13px;color:var(--moutarde-f)}
.comp-filtres{justify-content:flex-start}
.comp-filtre{border-color:transparent!important;background:var(--blanc);font-size:15px}
.comp-filtre.on,.comp-filtre[aria-pressed="true"]{background:var(--encre);color:#fff}
.btn-mini{font-size:14px}
/* financement et questions */
.gcard,.faq-item{border:0!important;background:var(--blanc)}
.gcard small,.gc-t small{font-size:14px;color:var(--taupe)}
.reconv .rc-sub{font-size:15px}
.faq-item summary{font-size:1.08rem}
/* appel final et pied de page : le nom revient en grand */
.grand-cta{background:var(--fond-sombre)}
footer{background:#221A0C}
footer a,footer li,footer p{font-size:15px}
.legal{border-top:0!important;font-size:14px;color:#BFB49B}
.f-nom{grid-column:1/-1;min-width:0;margin:26px 0 0;font-family:'Baloo 2';font-weight:800;font-size:calc((min(100vw,1180px) - 48px) / 8.6);line-height:.95;white-space:nowrap;letter-spacing:-.035em;color:var(--moutarde)}
@media(max-width:900px){.hero .wrap{grid-template-columns:1fr}.meth-ecrans,.meth-liste{grid-template-columns:1fr 1fr}.intensif-split,.faq .wrap{grid-template-columns:1fr}.faq-list{grid-column:1;grid-row:auto}}
@media(max-width:700px){
  .sec-titre{font-size:1.75rem}
  .sec-sub{font-size:16px}
  .hero h1{font-size:clamp(2.1rem,10vw,2.6rem)}
  .hero .geste{font-size:1.45rem}
  .hero .geste + p{font-size:16px}
  .meth-liste{grid-template-columns:1fr;gap:20px}
  .meth-liste .meth h4{font-size:1.12rem}
  .meth-ecrans{display:grid;grid-template-columns:1fr}
  .ecole h3{font-size:1.3rem}
  .f-nom{font-size:calc((100vw - 32px) / 8.6)}
}
@media(prefers-reduced-motion:reduce){.slide{transition:none!important}}
</style>'''

# --------------------------------------------------------------- écrans réels de la plateforme de Cook (CAP Cuisine)
EXAMEN = '''<figure class="rv intensif-ecran"><div class="ui" data-ui>
          <div class="ui-haut"><i></i>Examen blanc</div>
          <b class="ui-t">Techniques, hygiène et pratique</b>
          <div>Dans les conditions de l’examen, puis la correction question par question.</div>
          <div class="ui-chips"><span>45 min</span><span>19 questions</span><span>réussi à 60 %</span></div>
          <span class="ui-bouton">Commencer l’examen blanc</span>
        </div><figcaption>Deux examens blancs pour le CAP Cuisine, comme le jour J.</figcaption></figure>'''

ECRANS = '''<div class="meth-ecrans" aria-label="La plateforme de Cook, l’école déjà ouverte">
        <figure class="rv"><div class="ui" data-ui>
          <div class="ui-haut"><i></i>CAP Cuisine · leçon 4.2</div>
          <b class="ui-t">Les taillages de base</b>
          <div>Objectif&nbsp;: tailler régulièrement, vite et en sécurité.</div>
          <div class="ui-bloc"><b>À retenir</b><ul><li>Régularité avant vitesse</li><li>Tronçons, tranches, bâtonnets, dés&nbsp;: une progression</li><li>La taille du morceau dépend du temps de cuisson</li></ul></div>
          <div class="ui-bloc piege"><b>Le piège à éviter</b>Une macédoine à la place d’une brunoise&nbsp;: une erreur technique relevée par le jury.</div>
        </div><figcaption>Une leçon&nbsp;: l’essentiel, le piège, puis la mise en pratique.</figcaption></figure>
        <figure class="rv"><div class="ui" data-ui>
          <div class="ui-haut"><i></i>Quiz · question 3 sur 16</div>
          <b class="ui-t">L’épreuve EP1 en forme ponctuelle est&nbsp;:</b>
          <span class="ui-opt">Un oral de 20 minutes</span>
          <span class="ui-opt ok">Un écrit de 2 heures</span>
          <span class="ui-opt">Une pratique de 5 heures</span>
          <div class="ui-expl">Une étude de cas écrite de 2 heures, coefficient 4.</div>
        </div><figcaption>Un quiz à chaque étape, corrigé tout de suite.</figcaption></figure>
        <figure class="rv"><div class="ui" data-ui>
          <div class="ui-haut"><i></i>Votre itinéraire · CAP Cuisine</div>
          <div class="ui-barre"><span style="width:30%"></span></div>
          <ol>
            <li class="fait"><i>1</i>Le diplôme et l’examen<small>5</small></li>
            <li class="fait"><i>2</i>Pôle 1<small>2</small></li>
            <li class="fait"><i>3</i>Poste et hygiène<small>2</small></li>
            <li class="ici"><i>4</i>Techniques culinaires<small>12</small></li>
            <li><i>5</i>Dresser, goûter, communiquer<small>3</small></li>
            <li><i>6</i>Sciences, gestion, PSE<small>4</small></li>
            <li><i>7</i>L’épreuve EP2<small>2</small></li>
          </ol>
        </div><figcaption>Sept stations, trente leçons&nbsp;: on voit toujours le prochain arrêt.</figcaption></figure>
      </div>'''



def nettoyer(css):
    """Retire de la feuille d'origine les ombres, flous, dégradés et filets d'un pixel que ce passage remplace."""
    css = re.sub(r'(-webkit-)?backdrop-filter:[^;}]*;?', '', css)
    css = re.sub(r'box-shadow:[^;}]*;?', '', css)
    css = re.sub(r'filter:\s*drop-shadow\([^)]*\)\s*;?', '', css)
    css = re.sub(r'background(-image)?:\s*(linear|radial)-gradient\((?:[^()]|\([^()]*\))*\)[^;}]*;?', '', css)
    css = re.sub(r'border(-top|-bottom|-left|-right)?:\s*1px solid[^;}]*;?', '', css)
    return css
