from random import randint
class NegativeParamError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class Pokemon:
    def __init__(self, id, abilities, name, health, defense, normal_attack, types, special_attack, special_defense, weakness_against_types, speed, generation) -> None:
        """
        Constructor of Pokemon
        """
        self.id = id
        self._name = name
        if (health < 0 or defense < 0 or normal_attack < 0 or generation < 0 or speed < 0):
            raise NegativeParamError("Those parameters must be non-negative")
        else:
            pass
        self._health = health
        self._abilities = abilities
        self._defense = defense
        self._normal_attack = normal_attack
        self._types = types
        self._special_attack = special_attack
        self._weakness_against_types = weakness_against_types
        self._generation = generation
        self._special_defense = special_defense
        self._speed = speed

    def weakness_multiplier(self, attack_type, enemy):
        """
        Calculating damage multiplier against given enemy type
        :attack_type: type of attack
        :enemy: current enemy fighter
        """
        multiplier = 1
        for against_type in enemy._weakness_against_types:
            enemy_type = against_type[8:]
            if (attack_type == enemy_type):
                multiplier = enemy._weakness_against_types[against_type]
                break
        return float(multiplier)

    def defense(self):
        """
        Pokemon increases his defense
        """
        self._defense = round(self._defense*1.10, 2)
        return self._defense

    def attack(self, attack_type, enemy):
        """
        Pokemon attacks enemy with chosen attack type
        :attack_type: type of attack
        :enemy: current enemy fighter
        """
        damage_dealt = self.calculate_damage(attack_type, enemy)
        enemy._health = round(enemy._health - damage_dealt, 2)
        if (enemy._health < 0):
            enemy._health = 0
        return damage_dealt, enemy._health

    def critical(self):
        """
        Calculating if critical hit will occur
        """
        threshold = self._speed/2
        if (threshold > randint(0, 255)):
            return 2
        return 1

    def calculate_damage(self, attack_type, enemy):
        """
        Calculates damage dealt to enemy with certain attack_type
        :attack_type: type of attack
        :enemy: current enemy fighter
        """
        critical = self.critical()
        attack_to_defense = self._normal_attack/enemy._defense
        weakness_multiplier = self.weakness_multiplier(attack_type, enemy)
        random_multiplier = randint(217, 255)/255
        damage = round(((((2*1*critical)/5 + 2)*attack_to_defense)/50+2)*weakness_multiplier*random_multiplier, 2)
        return damage