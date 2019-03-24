from rest_framework.decorators import api_view
from rest_framework.response import Response

from cride.circles.models import Circle


@api_view(['GET'])
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
	return Response(data)


@api_view(['POST'])
def create_circle(request):
	"""Create circle."""
	name = request.data['name']
	slug_name = request.data['slug_name']
	about = request.data.get('about', '')
	circle = Circle.objects.create(name=name, slug_name=slug_name, about=about)
	data = {
		'name': circle.name,
		'slug_name': circle.slug_name,
		'rides_offered': circle.rides_offered,
		'rides_taken': circle.rides_taken,
		'members_limit': circle.members_limit
	}
	return Response(data)
