from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from backend.infer_data_types import process_data_frame
from .serializers import FileUploadSerializer

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                # Read the uploaded file into a DataFrame
                df = pd.read_csv(file)  # Adjust as needed for Excel files

                # Process the data using the script function
                processed_df = process_data_frame(df)

                # Convert the processed DataFrame to JSON and return
                return Response(processed_df.to_dict(orient='records'), status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
