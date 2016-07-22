from functools import partial

from coremod import overloadmethod

from core.terraform.helper import plantOrganicAction, placeTiles, placeTilesInArea
from core.terraform.stamps import createStampColor, loadStamps

from siege import game
from siege.util import WorldRandom, RangeUint, Sizes, TileRect, TileVector, Vector
from siege.worldgen import Biome, FillMode, Terraform
from siege.world.realm import Layer, UnderwaterSupport


class PlainsBiome(Biome):
    def __init__(self):
        Biome.__init__(self)
        self.name = "Plains"
        self.layer = "surface"
        self.frequency = 50
        self.width = RangeUint(8, 12)
        self.height = RangeUint(30, 50)
        self.heightTolerance = 3
        self.widthIncrement = 32
        self.groundId = game.content.get('dirt').id
        self.wallId = self.groundId
        self.sky = 'mods/core/environment/sky.png'
        self.back1.images.append('mods/core/environment/plains/back1.png')
        self.back1.offset = Vector(0, 360)
        self.back1.scroll = Vector(0.5, 0.1)
        self.back2.images.append('mods/core/environment/plains/back2.png')
        self.back2.offset = Vector(0, 100)
        self.back2.scroll = Vector(0.3, 0.075)
        self.back3.images.append('mods/core/environment/plains/back3.png')
        self.back3.offset = Vector(0, 30)
        self.back3.scroll = Vector(0.1, 0.05)
        self.crystalIcon = 'mods/core/environment/plains/crystal_icon.png'
        # Define stamps
        self.hillStamps = loadStamps('plains/hill')
        self.tunnelStamps = loadStamps('plains/tunnel')

    def isCompatible(self, biome, distanceFromStart):
        return biome.name is not "Volcano"

    def getOccurrences(self, realmSize):
        return RangeUint(1, 9999)

    def reset(self, area):
        self.isHilly = WorldRandom.get(5) > 1
        if self.isHilly:
            self.count = WorldRandom.get(1, 3)
        else:
            self.count = WorldRandom.get(3, 4)

    def getStamps(self, remainingSpace, surfaceLevel, previousStamp=None):
        # Two different types of stamps - Flat/Hilly stamps and tunnel stamps
        if self.count == 0:
            self.reset(None)
        self.count -= 1
        return list(self.hillStamps) if self.isHilly else list(self.tunnelStamps)

    def getRules(self):
        tileRules = {}
        stoneId = game.content.get('stone').id
        tileRules[createStampColor(140, 140, 140)] = (stoneId, stoneId)
        tileRules[createStampColor(100, 80, 60)] = (self.groundId, 0)
        tileRules[createStampColor(80, 60, 40)] = (self.groundId, self.wallId)
        tileRules[createStampColor(154, 126, 98)] = (0, self.wallId)
        tileRules[createStampColor(255, 246, 0)] = (0, self.groundId)  # fill our special underground connectors with wall
        tileRules[createStampColor(48, 141, 255)] = (self.groundId, self.wallId)  # This is to fill cave entrances with with solid tile
        tileRules[createStampColor(0, 0, 255)] = (0, 0)
        return tileRules

    def getActions(self, biomeData):
        frequency = 1 / 10000.0
        actions = []
        actions.append(partial(placeTiles, Layer.Ground, '', 3 * frequency, (2, 3), (2, 4), (0.25, 1.0), FillMode.SOLID_ONLY, "holes"))
        actions.append(partial(placeTiles, Layer.Ground, '', 2 * frequency, (4, 10), (4, 10), (0.0, 1.0), FillMode.SOLID_ONLY, "holes"))
        actions.append(partial(placeTiles, Layer.Ground, 'clay', 5 * frequency, (3, 8), (3, 8), (0.2, 1.0), FillMode.SOLID_ONLY, "tile_small"))
        actions.append(partial(placeTiles, Layer.Ground, 'clay', 2 * frequency, (3, 12), (3, 12), (0.4, 1.0), FillMode.SOLID_ONLY, "tile_medium"))
        actions.append(partial(placeTiles, Layer.WallAndGround, 'stone', 6 * frequency, (2, 5), (2, 5), (0.0, 1.0), FillMode.SOLID_ONLY, "tile_small"))
        actions.append(partial(placeTiles, Layer.WallAndGround, 'stone', 4 * frequency, (5, 10), (5, 10), (0.2, 1.0), FillMode.SOLID_ONLY, "tile_medium"))
        actions.append(partial(placeTiles, Layer.Ground, 'copper_ore', 2 * frequency, (2, 4), (2, 4), (0.4, 1.0), FillMode.SOLID_ONLY, "tile_small"))
        actions.append(partial(placeTiles, Layer.Ground, 'copper_ore', 2 * frequency, (2, 5), (2, 5), (0.7, 1.0), FillMode.SOLID_ONLY, "tile_medium"))
        actions.append(partial(placeTiles, Layer.Ground, 'iron_ore', 1 * frequency, (2, 5), (2, 5), (0.9, 1.0), FillMode.SOLID_ONLY, "tile_small"))
        return actions

    @overloadmethod
    def getPostActions(self, biomeData):
        return [
            partial(self.placePots, biomeData.uid),
            self._spreadGrass,
            self.plantTrees,
            self.plantCrops
        ]

    def plantCrops(self, area, ratio, game, world, realm, data):
        plantOrganicAction('apple_tree', Layer.Back, (2, 3), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        plantOrganicAction('tomato_plant', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        plantOrganicAction('carrot_plant', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        plantOrganicAction('lettuce_plant', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        plantOrganicAction('onion_plant', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        plantOrganicAction('potato plant', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)

    def getFinalActions(self, biomeData):
        return []

    def _spreadGrass(self, area, ratio, game, world, realm, data):
        Terraform.fillGrassFoliage(realm, Layer.Ground, game.content.get('grass').entity.foliage, TileRect(area.x, area.y, area.width, area.height + Sizes.SEGMENT_TILE * 5))

    def plantTrees(self, area, ratio, game, world, realm, data):
        if 'zebra_trees' not in data:
            treeType = 1
            data['zebra_trees'] = True
        else:
            treeType = WorldRandom.get(3)
        if treeType == 0:
            plantOrganicAction('oak_tree', Layer.Back, (55, 65), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        elif treeType == 1:
            plantOrganicAction('zebra_tree', Layer.Back, (45, 55), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
            plantOrganicAction('old_zebra_tree', Layer.Back, (3, 6), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)
        else:
            plantOrganicAction('marshmallow_tree', Layer.Back, (55, 65), True, False, UnderwaterSupport.Disallow, area, ratio, game, world, realm, data)

    def placePots(self, uid, area, ratio, game, world, realm, data):
        ground = realm.layers[Layer.Ground]
        potsTileId = game.content.get('pots').id
        stamps = data['biomeStamps'][uid]
        for placed in stamps:
            if 'tunnel' in placed.stamp.image:
                rand = WorldRandom.get(100)
                count = 0 if rand < 20 else (1 if rand < 85 else 2)
                for _ in xrange(count):
                    amount = [WorldRandom.get(3, 5)] * 2
                    area = placed.getArea()
                    position = TileVector(area.x + WorldRandom.get(area.width), area.bottom - 1, realm.size.loopTileWidth)
                    placeTilesInArea(ground, potsTileId, position, area.height, -1, area, amount)
