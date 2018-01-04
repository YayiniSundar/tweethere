from django.core.exceptions import ValidationError

# Create your models here.
def validate_content(value):         #//Validation for Content
		content = value
		if content == "abc":
			raise ValidationError("Content Cannot be ABC")
		return value