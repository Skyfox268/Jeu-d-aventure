"""
Jeu d'aventure dans la console.
Contraintes : variables en espagnol et interdit d'utiliser des listes

"""

class Objeto:
    def __init__(self, nombre, cantidad, descripcion):
        self.nombre = nombre
        self.cantidad = cantidad
        self.descripcion = descripcion
    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"
    
class Pocion(Objeto):
    def __init__(self, cantidad):
        super().__init__("Potion de soin", cantidad, "Restaure 50 points de vie.")




class Inventario:
    def __init__(self):
        self.objetos = []

    def agregar_objeto(self, objeto):
        self.objetos.append(objeto)
    
    def mostrar_inventario(self):
        for objeto in self.objetos:
            print(f"- {objeto}")

class Jugador:
    def __init__(self, vida = "Non-défini", ataque = "Non-définie", seudonimo = "Joueur"):
        self.vida = vida
        self.ataque = ataque
        self.seudonimo = seudonimo
        self.inventario = Inventario()

    def eleccion_clase(self):
        print("Choisissez une classe de personnage :")
        print("1. Pluma (Vie: 75, Attaque: 125)")
        print("2. Promedio (Vie: 100, Attaque: 100)")
        print("3. Pesado (Vie: 125, Attaque: 75)")
        eleccion = input("Entrez le numéro de votre choix : ")
        if eleccion == "1":
            return Pluma(75, 125, "Agile")
        elif eleccion == "2":
            return Promedio(100, 100, "Équilibré")
        elif eleccion == "3":
            return Pesado(125, 75, "Fort")
        else:
            print("Choix invalide, réessayez.")
            return self.eleccion_clase()

    def atacar(self, objetivo):
        objetivo.sufrir(self.ataque)
        nombre_objetivo = getattr(objetivo, 'nombre', getattr(objetivo, 'seudonimo', 'Inconnu'))
        if objetivo.vida <= 0 :
            print(f"Vous avez infligé {self.ataque} dégâts à {nombre_objetivo}, il est mort.")
        else:
            print(f"Vous avez infligé {self.ataque} dégâts à {nombre_objetivo}, il lui reste {objetivo.vida} PVs.")
    
    def sufrir(self, cantidad):
        if self.vida - cantidad <= 0 :
            self.vida = 0
        else:
            self.vida -= cantidad
    
    def cambiar_seudonimo(self):
        nuevo_seudonimo = input("Entrez votre nouveau pseudo : ")
        self.seudonimo = nuevo_seudonimo
        print(f"Votre nouveau pseudo est {self.seudonimo}.")

    def __str__(self):
        return f"Joueur {self.seudonimo} - Vie: {self.vida} - Attaque: {self.ataque} - Classe: {self.__class__.__name__}."
    
    def agregar_objeto(self, objeto):
        self.inventario.agregar_objeto(objeto)
        print(f"Tu as ajouté {objeto.nombre} (x{objeto.cantidad}) à ton inventaire.")
    
    def mostrar_inventario(self):
        print(f"Inventaire de {self.seudonimo}:")
        self.inventario.mostrar_inventario()
    
    def usar_pocion(self):
        # Chercher une potion dans l'inventaire
        for i, objeto in enumerate(self.inventario.objetos):
            if isinstance(objeto, Pocion) and objeto.cantidad > 0:
                vida_anterior = self.vida
                self.vida = min(self.vida + 50, 125)  # Max 125 PV
                vida_recuperada = self.vida - vida_anterior
                objeto.cantidad -= 1
                print(f"Vous avez utilisé une potion et récupéré {vida_recuperada} PV. Vie actuelle: {self.vida}")
                if objeto.cantidad == 0:
                    self.inventario.objetos.pop(i)
                return True
        print("Vous n'avez pas de potion dans votre inventaire.")
        return False


class Pluma(Jugador):
    def __init__(self, vida, ataque, clase):
        super().__init__(75, 125, seudonimo="Pluma")
        self.clase = clase

class Promedio(Jugador):
    def __init__(self, vida, ataque, clase):
        super().__init__(100, 100, seudonimo="Promedio")
        self.clase = clase

class Pesado(Jugador):
    def __init__(self, vida, ataque, clase):
        super().__init__(125, 75, seudonimo="Pesado")
        self.clase = clase
    



class Enemigo:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def atacar(self, objetivo):
        objetivo.sufrir(self.ataque)
        nombre_objetivo = getattr(objetivo, 'seudonimo', getattr(objetivo, 'nombre', 'Inconnu'))
        if objetivo.vida <= 0 :
            print(f"L'ennemi a infligé {self.ataque} dégâts à {nombre_objetivo}, il est mort.")
        else:
            print(f"L'ennemi a infligé {self.ataque} dégâts à {nombre_objetivo}, il lui reste {objetivo.vida} PVs.")
    
    def sufrir(self, cantidad):
        if self.vida - cantidad <= 0 :
            self.vida = 0
        else:
            self.vida -= cantidad

    def __str__(self):
        return f"Ennemi {self.nombre} - Vie: {self.vida} - Attaque: {self.ataque}."
    
class Duende(Enemigo):
    def __init__(self):
        super().__init__("Duende", 50, 20)

class Esqueleto(Enemigo):
    def __init__(self):
        super().__init__("Squelette guerrier", 75, 35)

class Dragon(Enemigo):
    def __init__(self):
        super().__init__("Dragon", 120, 50)


def combate(jugador, enemigo):
    """Gère un combat entre le joueur et un ennemi"""
    print(f"\n🗡️  COMBAT! Vous affrontez {enemigo.nombre}!")
    print(f"Ennemi: Vie {enemigo.vida}, Attaque {enemigo.ataque}")
    print(f"Vous: Vie {jugador.vida}, Attaque {jugador.ataque}\n")
    
    while jugador.vida > 0 and enemigo.vida > 0:
        print("\n--- Votre tour ---")
        print("1. Attaquer")
        print("2. Utiliser une potion")
        print("3. Fuir")
        
        choix = input("Que voulez-vous faire? ")
        
        if choix == "1":
            jugador.atacar(enemigo)
            if enemigo.vida <= 0:
                print(f"✅ Victoire! Vous avez vaincu {enemigo.nombre}!")
                return True
        elif choix == "2":
            jugador.usar_pocion()
        elif choix == "3":
            print("Vous prenez la fuite!")
            return False
        else:
            print("Choix invalide!")
            continue
        
        if enemigo.vida > 0:
            print("\n--- Tour de l'ennemi ---")
            enemigo.atacar(jugador)
            if jugador.vida <= 0:
                print("💀 Game Over! Vous êtes mort...")
                return False
    
    return jugador.vida > 0


def juego_principal():
    """Fonction principale du jeu d'aventure"""
    print("=" * 50)
    print("🏰 BIENVENUE DANS LE JEU D'AVENTURE! 🏰")
    print("=" * 50)
    
    # Création du personnage
    j = Jugador()
    j = j.eleccion_clase()
    j.cambiar_seudonimo()
    
    # Ajouter une potion de départ
    j.agregar_objeto(Pocion(2))
    
    print(f"\n{j}\n")
    
    # Chapitre 1: La forêt
    print("\n" + "=" * 50)
    print("CHAPITRE 1: LA FORÊT SOMBRE")
    print("=" * 50)
    print("Vous vous réveillez dans une forêt sombre et mystérieuse...")
    print("Un petit goblin apparaît devant vous!")
    
    enemigo1 = Duende()
    if not combate(j, enemigo1):
        return
    
    # Récompense
    print("\n🎁 Vous trouvez une potion sur le corps du goblin!")
    j.agregar_objeto(Pocion(1))
    
    # Chapitre 2: Les ruines
    print("\n" + "=" * 50)
    print("CHAPITRE 2: LES RUINES HANTÉES")
    print("=" * 50)
    print("Vous continuez votre chemin et découvrez d'anciennes ruines...")
    print("Un squelette guerrier sort de l'ombre!")
    
    enemigo2 = Esqueleto()
    if not combate(j, enemigo2):
        return
    
    # Récompense
    print("\n🎁 Vous trouvez 2 potions dans les ruines!")
    j.agregar_objeto(Pocion(2))
    
    # Chapitre 3: Boss final
    print("\n" + "=" * 50)
    print("CHAPITRE 3: LE DRAGON ANCIEN")
    print("=" * 50)
    print("Vous arrivez devant une immense caverne...")
    print("Un rugissement terrifiant résonne!")
    print("🐉 UN DRAGON APPARAÎT!")
    
    enemigo3 = Dragon()
    if not combate(j, enemigo3):
        return
    
    # Victoire finale
    print("\n" + "=" * 50)
    print("🎉🎉🎉 FÉLICITATIONS! 🎉🎉🎉")
    print("=" * 50)
    print(f"Vous avez vaincu le dragon et sauvé le royaume!")
    print(f"Bravo {j.seudonimo}! Vous êtes un véritable héros!")
    print(f"Points de vie restants: {j.vida}")
    print("=" * 50)


# Lancer le jeu
if __name__ == "__main__":
    juego_principal()
