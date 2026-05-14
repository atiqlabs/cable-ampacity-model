
class ConcreteDuctBank:

    def __init__(
        self,
        num_cables=3,
        width=0.9,
        height=1.2, # longer side of the duct bank in this case
        top_cover=0.8, # above duct bank
        concrete_resistivity=1.2,
        backfill_resistivity=1.0
    ):

        self.num_cables = num_cables

        self.width = width
        self.height = height

        self.top_cover = top_cover

        self.concrete_resistivity = concrete_resistivity
        self.backfill_resistivity = backfill_resistivity