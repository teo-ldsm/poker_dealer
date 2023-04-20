class Joueur:
    def __init__(self, cagnotte, nom_joueur):
        self.__cagnotte = cagnotte
        self.__mise = 0
        self.__folded = False
        self.__nom = nom_joueur
        self.__call = False
        self.__all_in = False

    def __repr__(self):
        retour = f"{self.get_nom()} possède {self.get_cagnotte() - self.get_mise()}€"

        if self.est_fold():
            retour += " mais il s'est couché"

        if self.a_all_in():
            retour += " et il a all in"

        if self.__mise > 0:
            retour += f" et sa mise et de {self.__mise}€"

        return retour

    # Setters

    def set_fold(self, state: bool):
        self.__folded = state

    def set_call(self, state: bool):
        self.__call = state

    def set_all_in(self, state: bool):
        self.__all_in = state

    def ajouter_cagnotte(self, montant):
        self.__cagnotte += montant

    def retirer_cagnotte(self, montant):
        self.__cagnotte -= montant

    def clear_mise(self):
        self.__mise = 0

    # Getters

    def est_fold(self):
        return self.__folded

    def a_call(self):
        return self.__call

    def a_all_in(self):
        return self.__all_in

    def get_nom(self):
        return self.__nom

    def get_cagnotte(self):
        return self.__cagnotte

    def get_mise(self):
        return self.__mise

    # Methods

    def miser(self, mise) -> int:
        if mise < self.__cagnotte:
            self.__mise = mise

        else:
            self.__mise = self.__cagnotte
            self.set_all_in(True)

        return mise

    def all_in(self) -> int:
        self.set_all_in(True)
        return self.miser(self.__cagnotte)


def blinds(j1, j2):
    global mise_prec

    choix_valide = False
    blind = None
    while not choix_valide:
        try:
            blind = eval(input("\nEntrez le montant de la petite blind"))
            if not isinstance(blind, int):
                raise TypeError("La variable blind doit être de type int")
            choix_valide = True

        except:
            print("\n\nRéponse invalide, entrez un chiffre")
            choix_valide = False

    j1.miser(blind)
    j2.miser(blind * 2)
    j2.set_call(True)
    mise_prec = blind * 2


def tour_de_mise():
    global mise_prec

    print("\n" * 5)
    for i in joueurs:
        print(i)
    print("\n" * 5)

    for joueur in joueurs:
        if not joueur.est_fold() and not joueur.a_call() and not joueur.a_all_in():
            print(f"{joueur}, c'est a lui de jouer, que veut tu faire ?\n")
            choix_valide = False
            choix = ""

            demande_choix_user = f"C : Call ({mise_prec}€) \t M : Miser \t A : All in \t F : Fold"
            if mise_prec == 0:
                demande_choix_user = "C : Check \t M : Miser \t A : All in \t F : Fold"

            while not choix_valide:
                choix = input(demande_choix_user).upper()
                if choix in ("C", "M", "A", "F"):
                    choix_valide = True
                else:
                    print("Veuillez rentrer une lettre parmi C, M, A et F")

            if choix == "C":
                mise_prec = joueur.miser(mise_prec)
                print(f"\n{joueur.get_nom()} a call {mise_prec}€, il lui reste "
                      f"{joueur.get_cagnotte() - joueur.get_mise()}€\n\n\n\n")

            elif choix == "M":
                montant = -1

                choix_valide = False
                while not choix_valide:
                    try:
                        montant = eval(input(f"\nEntrez un montant à miser. Il doit être supérieur a {mise_prec}€"))
                        if not isinstance(montant, int):
                            raise TypeError("La variable blind doit être de type int")
                        if montant < mise_prec:
                            raise ValueError("Valeur trop petite")
                        choix_valide = True
                    except:
                        print(f"\n\nRéponse invalide, entrez un chiffre supérieur a {mise_prec}")
                        choix_valide = False

                print(f"\n{joueur.get_nom()} a misé {mise_prec}€, il lui reste "
                      f"{joueur.get_cagnotte() - joueur.get_mise()}€\n\n\n\n")
                mise_prec = joueur.miser(montant)

            elif choix == "A":
                print(f"\n{joueur.get_nom()} a all in (Il possède un charisme digne de Partick Bruel)\n\n\n\n")
                mise_prec = joueur.all_in()

            else:
                joueur.set_fold(True)
                print(f"{joueur.get_nom()} s'est couché\n\n\n\n")


def tour_de_mise_complet(j1, j2):
    for joueur in joueurs:
        joueur.set_call(False)

    blinds(j1, j2)

    call_general = False

    while not call_general:
        tour_de_mise()
        list_call_general = []

        for joueur in joueurs:
            if joueur.get_mise() == mise_prec:
                joueur.set_call(True)
                list_call_general.append(True)

            elif joueur.est_fold() or joueur.a_all_in():
                list_call_general.append(True)

            else:
                list_call_general.append(False)

        if False in list_call_general:
            call_general = False

        else:
            call_general = True


def vainqueur(pot):
    choix_possibles = []
    for i in range(len(joueurs)):
        print(f"{i+1} : {joueurs[i].get_nom()}")
        choix_possibles.append(i+1)

    choix_valide = False
    choix_user = None
    while not choix_valide:
        try:
            choix_user = eval(input("\nQui est le vainqueur de la partie ? \nEntrez le numéro du joueur"))
            if choix_user in choix_possibles:
                choix_valide = True

            else:
                raise TypeError("Rep invalide")
        except:
            print("\n\nRéponse invalide, entrez un chiffre")

    winner = joueurs[choix_user-1]
    winner.ajouter_cagnotte(pot)
    print(f"\n\n{winner.get_nom()} à gagné, il remporte {pot}€ et sa cagnotte est de {winner.get_cagnotte()}€")


def pli(j1, j2):
    global mise_prec
    input("Distribuez les cartes, appuyez sur \"Enter\" quand c'est fait")

    mise_prec = 0

    pot = 0
    tour_de_mise_complet(j1, j2)

    all_in_general = []

    for joueur in joueurs:
        pot += joueur.get_mise()
        joueur.retirer_cagnotte(joueur.get_mise())
        joueur.clear_mise()
        if joueur.a_all_in():
            all_in_general.append(True)
        else:
            all_in_general.append(False)

    if not (False in all_in_general):
        input("Le tour est terminé car tout le monde a all in, vous pouvez abattre toutes les cartes, appuyez sur "
              "\"Enter\" quand c'est fait")
        vainqueur(pot)
        pass
    else:
        input("Le premier tour est terminé, abattez 3 carte, appuyez sur \"Enter\" quand c'est fait")

    mise_prec = 0
    pot = 0
    tour_de_mise_complet(j1, j2)

    for joueur in joueurs:
        pot += joueur.get_mise()
        joueur.retirer_cagnotte(joueur.get_mise())
        joueur.clear_mise()
        if joueur.a_all_in():
            all_in_general.append(True)
        else:
            all_in_general.append(False)

    if not (False in all_in_general):
        input("Le tour est terminé car tout le monde a all in, vous pouvez abattre toutes les cartes, appuyez sur "
              "\"Enter\" quand c'est fait")
        vainqueur(pot)
        pass
    else:
        input("Le deuxième tour est terminé, abattez une carte, appuyez sur \"Enter\" quand c'est fait")

    mise_prec = 0
    pot = 0
    tour_de_mise_complet(j1, j2)

    for joueur in joueurs:
        pot += joueur.get_mise()
        joueur.retirer_cagnotte(joueur.get_mise())
        joueur.clear_mise()

    input("Le tour est terminé, abattez une dernière carte, appuyez sur \"Enter\" quand c'est fait")

    vainqueur(pot)


def partie():

    global mise_prec, nb_joueur, joueurs

    choix_valide = False
    cagnotte_depart = None
    while not choix_valide:
        try:
            nb_joueur = eval(input("Combien ya t'il de joueur ?"))
            cagnotte_depart = eval(input("Quelle est la cagnotte de départ ?"))
            choix_valide = True
            if not isinstance(nb_joueur, int) or not isinstance(cagnotte_depart, int):
                raise TypeError("Choix invalide")
            if nb_joueur <= 1:
                print("\nLe poker se joue a 2 minimum\n")
                choix_valide = False

        except:
            print("\nLa valeur est invalide, entrez un chiffre\n")
            choix_valide = False

    joueurs = []
    mise_prec = 0
    for i in range(nb_joueur):

        choix_valide = False
        nom = None
        while not choix_valide:
            nom = input(f"\nEntrer le nom du joueur {i + 1}")
            choix_valide = True
            if len(nom) == 0 or not isinstance(nom, str):
                choix_valide = False
                print("\nLa valeur est invalide\n")

        joueurs.append(Joueur(cagnotte_depart, nom))

    choix_possibles = []
    print("\n\n\n")
    for i in range(len(joueurs)):
        print(f"{i + 1} : {joueurs[i].get_nom()}")
        choix_possibles.append(i + 1)

    choix_valide = False
    choix_user = None
    while not choix_valide:
        try:
            choix_user = eval(input("\nQui commence a parler ? \nEntrez le numéro du joueur"))
            if choix_user in choix_possibles:
                choix_valide = True

            else:
                raise TypeError("Rep invalide")

        except:
            print("\n\nRéponse invalide, entrez un chiffre")

    dealer = joueurs[choix_user - 1]

    while joueurs[0] != dealer:
        temp = joueurs.pop()
        joueurs.insert(0, temp)

    pli(joueurs[-2], joueurs[-1])

    while len(joueurs) > 1:
        for joueur in joueurs:
            if joueur.get_cagnotte() == 0:
                print(f"\n{joueur.get_nom()} n'as plus d'argent, il est éliminé\n")
                joueurs.remove(joueur)
        joueurs.insert(0, joueurs.pop(0))
        pli(joueurs[-1], joueurs[0])

    print(f"\n\n\n\n\nLa partie est terminé\n\nBravo !! {joueurs[0].get_nom()} a gagné la partie\nIl gagne le "
          f"respect éternel de tous les membres de l'auditoire.")

    choix_valide = False
    choix = None
    while not choix_valide:
        choix = input("\n\n\nVoulez vous rejouer ? (Oui/Non)").upper()
        if choix in ("NON", "OUI"):
            choix_valide = True
        else:
            print("Veuillez répondre \"Oui\" ou \"Non\"")

    if choix == "OUI":
        print("\n\n\n\n\n\n\n\n\n------NOUVELLE PARTIE------\n\n\n")
        partie()

    else:
        print("Merci d'avoir joué, a bientôt")
        input("Appuyez sur \"Enter\" pour quitter")
        pass


partie()
