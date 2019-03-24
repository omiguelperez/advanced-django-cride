from django.http import JsonResponse

from cride.circles.models import Circle


def list_circles(request):
	"""List public circles."""
	public_circles = Circle.objects.filter(is_public=True)
	data = [{
		'name': circle.name,
		'slug_name': circle.slug_name,
		'rides_offered': circle.rides_offered,
		'rides_taken': circle.rides_taken,
		'members_limit': circle.members_limit
	} for circle in public_circles]
	return JsonResponse(data, safe=False)
