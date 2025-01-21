from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from services.deep_seek import DeepSeekService


class GiftIdeaGenerator(APIView):
    def post(self, request):
        params = self.request.data
        service = DeepSeekService()
        try:
            return service.generate_gift_ideas(params)
            # ideas = service.generate_gift_ideas(params)
            # return Response({"ideas": ideas}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
