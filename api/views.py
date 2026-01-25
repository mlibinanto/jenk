from rest_framework.views import APIView
from rest_framework.response import Response
from Admin.models import Admin

class BankApiView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})
    
    def post(self, request):
        print(request.data)

        return Response({"message": "POST request received!"})

        # name = request.data.get("name", "Guest")
        # return Response({"message": f"Hello, {name}!"})
    