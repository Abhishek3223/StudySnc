
class Room(models.Model):
    # host=
    # topic=
    name = models.CharField(max_length=200)
    discription = models.TextField(null=True, blank=True)
    # participants=
    updated = models.DateTimeField(auto_now=True)
    # ----auto now takes timestamp at evry momnet we updae the database where as auto now add does it when we create the data base
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)