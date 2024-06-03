from tortoise import fields, models


class Exercise(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    ex_numbers = fields.IntField()
    completely = fields.BooleanField(default=False)
    tries = fields.IntField(default=0)
    res = fields.CharField(max_length=255)

    class Meta:
        table = "exercises"
