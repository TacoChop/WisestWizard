from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)
custodial_bot = Entity(char='\u00A7', color=(0, 178, 89), name="Custodial Bot", blocks_movement=True)
security_bot = Entity(char='\u2665', color=(140, 70, 0), name="Security Bot", blocks_movement=True)