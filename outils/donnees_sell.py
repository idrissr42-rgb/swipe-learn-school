"""Recopie depuis le dépôt de Sell (swipe-sell) ce que le site maître affiche de Sell : chiffres, formations,
diplômes préparés et métiers. Sortie : outils/source/formations-sell.json, lu par construire.py.

    python3 outils/donnees_sell.py /home/claude/swipe-sell
"""
import json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
SELL = 'https://sell.swipelearn.school'
DEB = {
    'vendeur': 'Commerces de détail, grandes surfaces spécialisées, boutiques indépendantes, enseignes en franchise.',
    'commercial': 'Entreprises de services, industrie, distribution, agences, travail indépendant.',
    'responsable-magasin': 'Magasins indépendants, enseignes, grandes et moyennes surfaces, réseaux de franchise.',
    'e-commerce': 'Boutiques en ligne, marques, vendeurs sur places de marché, agences.',
    'commercant': 'Commerce indépendant, artisanat, franchise, activité en ligne.',
    'relation-client': 'Services clients des entreprises, centres de relation client, banques, assurances, énergie, télécoms.',
}
PRINCIPALE = {'vendeur': 'vente', 'commercial': 'prospection_b2b', 'responsable-magasin': 'bts_mco', 'e-commerce': 'ecommerce', 'commercant': 'creer_commerce', 'relation-client': 'vente_telephone'}
VITRINE = ['bts_mco', 'vente', 'prospection_b2b', 'ecommerce']


def main(depot):
    js = open(os.path.join(depot, 'public/js/contenus-cours.js'), encoding='utf-8').read()
    E = json.loads(js.split('window.SW_ENRICHI=', 1)[1].rstrip().rstrip(';'))
    C = json.load(open(os.path.join(depot, 'outils/modele/catalogue.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(depot, 'outils/seo/metiers.json'), encoding='utf-8'))
    fd = os.path.join(depot, 'outils/modele/diplomes.json')
    DIP = json.load(open(fd, encoding='utf-8')) if os.path.exists(fd) else {}
    slug = lambda i: i.replace('_', '-')
    forms = [{'nom': E[f['id']]['titre'], 'niv': DIP[f['id']]['court'] if f['id'] in DIP else 'Courte', 'duree': 'environ %d h' % E[f['id']]['heures'], 'prix': 'Sur demande',
              'url': '%s/formations/%s.html' % (SELL, slug(f['id']))} for f in C['formations'] if f['id'] in E]
    met = [{'s': m['s'], 'nom': m['nom'], 'formation': E[PRINCIPALE[m['s']]]['titre'], 'pitch': m['intro'], 'missions': m['missions'], 'deb': DEB[m['s']]}
           for m in M if PRINCIPALE.get(m['s']) in E]
    out = {'source': 'dépôt swipe-sell : public/js/contenus-cours.js, outils/modele/catalogue.json et diplomes.json, outils/seo/metiers.json',
           'nb_formations': len(E), 'nb_lecons': sum(len(m['lecons']) for m in E.values()), 'nb_examens': sum(len(m['examens']) for m in E.values()),
           'nb_diplomes': len(DIP), 'vitrine': [E[i]['titre'] for i in VITRINE if i in E], 'formations': forms, 'metiers': met}
    json.dump(out, open(os.path.join(ICI, 'source', 'formations-sell.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(out['nb_formations'], 'formations,', out['nb_lecons'], 'leçons,', out['nb_examens'], 'examens,', out['nb_diplomes'], 'diplômes')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/swipe-sell')
