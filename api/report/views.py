from rest_framework.views import APIView
from rest_framework import status
from core.response import Response
from django.http import StreamingHttpResponse
import uuid
from store.models import Store
from report.report import Report


report = Report()


class ReportView(APIView):
    def get(self, *args, **kwargs):
        report_id: str = uuid.uuid4().hex
        report.start_process()
        return Response(
            status=status.HTTP_200_OK,
            message="test",
            data={
                "report_id": report_id,
            }

        )

    def post(self, *args, **kwargs):
        response = StreamingHttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="test.csv"'
        return response
