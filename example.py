import sisyphe
import pickle
import tempfile

categories = ['Russian', 'English']

def render(row):
    return f'<p>{row}</p>'

# a few examples to display in the UI the last one
# is to make sure the content is displayed correctly
features = {
    2: 'Thanks for your feedback God bless you',
    4: 'EARN $110,000.00 96 HOURS INVESTMENT I',
    6: 'When your payment is due, send your name',
    32: 'Amount (USD) $4,481.33 BITBRON successfully paid',
    43: 'Во Владимирской области объявили оранжевый уровень опасности',
    54: 'Общее число инфицированных коронавирусом жителей – 24 390 человек',
    23: "Who's the best defender in Champions League history?",
    42: "хотя были явными фаворитами , так что должны играть с полной отдачейа русичи",
    51: "Наш «любимый» проститутбайка и его оппо-колежанки, как и обещали многократно, врубились в Сеть",
    66: "Ceci est une phrase en français",
    12: "The one problem with vh is when you scroll on mobile and its address bar hides",
    13: "Thanks! I'll try to repro and add a note to the article.",
    94: """Pepe the Frog [ˈpɛpeɪ ðə fɹɑɡ]1 (« Pepe la grenouille ») est un personnage de fiction représentant une grenouille verte, 
    créé par Matt Furie dans le comics Boy's Club paru en 2005. À partir de 2008, il devient un mème Internet. À partir de 2016, il 
    est parfois utilisé comme symbole raciste, utilisé par l'alt-right pro-Donald Trump et l'extrême droite : cela n'est toutefois 
    pas généralisé. Pepe la grenouille apparaît en 2005, dans les pages de la bande dessinée Boy's Club de Matt Furie. Pepe est un 
    adolescent à tête de grenouille qui aime jouer aux jeux vidéo, manger des pizzas et traîner avec ses amis. Dans une page publiée, 
    Pepe urine aux toilettes, debout et le short baissé jusqu'aux chevilles. Un de ses amis s'exclame « Hey Pepe, il paraît que tu 
    baisses complètement ton froc quand tu pisses ? » Pepe répond avec un sourire béat « feels good man » (c'est trop cool, mec). En 
    2008, le visage béat de Pepe la grenouille est réutilisé sur 4chan où il acquiert une petite popularité auprès des utilisateurs 
    de 4chan, au point de devenir un mème. Puis Pepe la grenouille est décliné en de nombreuses versions qui expriment les sentiments 
    des internautes, et devient le symbole d'une génération revendiquant une certaine exclusion de la société, avec leurs propres codes.
    Vers 2014, Pepe commence à être vu sur d'autres réseaux, comme Reddit ou 9GAG. Puis un jour, Katy Perry2 et Nicki Minaj font 
    apparaître Pepe la grenouille dans leurs tweets, ce qui agace les utilisateurs de Pepe. Le journal Le Figaro compare ce rejet « à 
    celui du fan d'un groupe de rock indépendant qui verrait sa chanson préférée reprise dans une publicité pour de la lessive » et 
    ajoute : « une fois qu'une blague entre copains fait aussi rire ses parents, des stars de la pop ou des marques, elle n'est plus 
    drôle »3. Élection présidentielle américaine de 2016 Pour reprendre la main sur leur mème, les 4channers adeptes du lulz 
    (le versant méchant du lol) qui n'ont aucune limite dans l'offense, ni dans le harcèlement, ni dans les sujets de plaisanterie, 
    fabriquent des Pepe moustachues à croix gammées, « le nazisme étant un sujet tabou très apprécié à 4chan » comme le rappelle 
    7sur74. Puis en juillet 2015, le premier Pepe associé à Donald Trump publié sur 4chan5 est un personnage cartoonesque anti-establishment 
    et bien-pensance. En octobre 2015, Donald Trump partage un tweet où apparaît Pepe devant un podium présidentiel. Un tweetos 
    pensant que Donald Trump n'a jamais entendu parler de Pepe la grenouille écrit que « c'est sans doute le meilleur tweet de 2015 
    et vous ne saurez même pas pourquoi »3. Le 8 janvier 2016, Cheri Jacobus, consultante républicaine qui a porté plainte contre 
    Donald Trump pour diffamation, est harcelée en ligne par des supporters pro-Trump qui l'inondent de Pepe. Cheri Jacobus 
    déclare que « la grenouille verte est le symbole qu'utilisent les suprémacistes blancs dans leur propagande ». Des j
    ournalistes se questionnent sur les liens entre cette grenouille verte et l'alt-right, ce qui leur vaudra à leur tour des 
    attaques sous forme de Pepe nazis de toutes sortes4.
    En août 2016, lors d'un discours donné par Hillary Clinton, un utilisateur de 4chan hurle « Pepe ! » pour perturber le 
    meeting. Cet évènement est diffusé en direct sur YouTube3. Le journal Le Figaro rappelle que les valeurs morales ou politiques 
    des membres de 4chan, 8chan ou Reddit « sont souvent conservatrices, voire extrêmes » et qu'il est donc normal que l'un de 
    leurs memes préférés soit devenu le symbole d'une certaine extrême droite3. Enfin, Le Figaro rappelle l'amour pour l'absurde 
    des 4channers qui trouvent « drôle de voir un dessin de grenouille s'afficher dans des médias très sérieux », de provoquer la 
    perplexité des journalistes ou la crainte de l'équipe de campagne d'Hillary Clinton. En mai 2016, à un journaliste de Politico 
    qui se demande « Qui est ce personnage et pourquoi est-il associé aux fans de Trump ? », un internaute répond « ton pire cauchemar »3."""""
}

def save_callback(labels):
    with open('labels.pickle', 'wb') as f:
        f.write(pickle.dumps(labels))

labeller = sisyphe.Sisyphe(features,
                           categories,
                           'log.tsv',
                           save_callback,
                           render_callback=render)
sisyphe.run(labeller)