import random

class Ant:
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    def __init__(self, x, y, color, hp, speed, vision_range, strength, fertility, gender, mutation_rate):
        self.x = x
        self.y = y
        self.color = color          # Цвет муравья, определяет его фракцию
        self.hp = hp                # Здоровье муравья
        self.speed = speed          # Скорость муравья
        self.vision_range = vision_range  # Дальность зрения муравья
        self.strength = strength    # Сила муравья, определяет урон при атаке
        self.fertility = fertility  # Фертильность муравья, определяет вероятность успешного спаривания
        self.gender = gender        # Пол муравья
        self.mutation_rate = mutation_rate  # Вероятность мутации генов при создании потомства

    def decrease_hp(self, time_interval=10):
        """Уменьшает здоровье муравья каждые несколько секунд(вроде голода)"""
        self.hp -= time_interval

    def eat(self, food_amount):
        """Увеличивает здоровье муравья на количество съеденной еды."""
        self.hp += food_amount

    def attack(self, target):
        """Атакует другого муравья, уменьшая его здоровье на значение силы атакующего муравья."""
        target.hp -= self.strength

    def mate(self, partner):
        """
        Создает потомство с другим муравьем, если их полы разные.
        Гены потомка выбираются случайным образом от каждого родителя с вероятностью мутации.
        """
        if self.gender != partner.gender:
            child_genes = {}
            for gene in self.__dict__.keys():
                if random.random() < 0.5:
                    child_genes[gene] = getattr(self, gene)
                else:
                    child_genes[gene] = getattr(partner, gene)
                if random.random() < self.mutation_rate:
                    child_genes[gene] = self.mutate_gene(child_genes[gene])
            child = Ant(**child_genes)
            return child

    @staticmethod
    def mutate_gene(gene_value):
        """
        Мутирует значение гена путем добавления случайного числа в диапазоне [-0.1, 0.1].
        """
        return gene_value + random.uniform(-0.1, 0.1)
    def is_visible(self, location):
        """
        Проверка, находится ли местоположение в пределах области видимости муравья.
        """
        return self.distance_to(location) <= self.vision_range
    
    def distance_to(self, location):
        """
        Вычисление евклидово расстояние до местоположения.
        """
        dx = location[0] - self.x
        dy = location[1] - self.y
        return (dx**2 + dy**2)**0.5
    
    def direction_to(self, location):
        """
        Вычислите направление к местоположению.
        """
        dx = location[0] - self.x
        dy = location[1] - self.y
        distance = self.distance_to(location)
        return dx / distance, dy / distance

    def move_towards_food(self, food_locations):
        visible_food = [food for food in food_locations if self.is_visible(food)]

        if visible_food:
            closest_food = min(visible_food, key=lambda food: self.distance_to(food))
            direction = self.direction_to(closest_food)
        else:
            direction = random.choice(self.DIRECTIONS)

        self.x += direction[0] * self.speed
        self.y += direction[1] * self.speed

        return self.x, self.y
food_locations = []
food_increase_interval = 100
map_width = 20
map_height = 20
wall_row = 10
wall_col = 10

def spawn_food(current_time):
    food_spawn_time = 1
    initial_food_count = 10
    food_count = initial_food_count
    """
    Создает еду на карте в случайных местах. Количество появляющейся еды увеличивается каждые 100 секунд.
    """
    global food_locations

    if current_time - food_spawn_time >= food_increase_interval:
        food_count += 1
        food_spawn_time = current_time

    for _ in range(food_count):
        x = random.randint(0, map_width - 1)
        y = random.randint(0, map_height - 1)
        while True:
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)
            
            # Если координаты попали в стену, перезапускаем цикл и генерируем новые
            if x == wall_row or y == wall_col:
                continue
                
            food_locations.append((x, y))
            break