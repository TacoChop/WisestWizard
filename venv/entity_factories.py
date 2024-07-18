from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(structure=30, temperature=0, coruption=0, defense=2, power=5),
)

custodial_bot = Actor(
    char='\u00A7',
    color=(0, 178, 89),
    name="Custodial Bot",
    ai_cls=HostileEnemy,
    fighter=Fighter(structure=5, temperature=0, coruption=0, defense=0, power=2),
)

security_bot = Actor(
    char='\u2665',
    color=(140, 70, 0),
    name="Security Bot",
    ai_cls=HostileEnemy,
    fighter=Fighter(structure=15, temperature=0, coruption=0, defense=1, power=4),
)