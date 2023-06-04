from io import StringIO
from typing import List
from rest_framework.views import APIView
from rest_framework import status
from core.response import Response
from core.redis import get_report
import pandas as pd

from django.http import HttpResponse, StreamingHttpResponse
import uuid

from report.report import Report

report = Report()


class ReportView(APIView):

    def get(self, request, *args, **kwargs):
        report_id: str = uuid.uuid4().hex
        report.generate_report(report_id)
        return Response(
            status=status.HTTP_200_OK,
            message="test",
            data={
                "report_id": report_id,
            }
        )


class GetReportView(APIView):
    def get(self, request, id, *args, **kwargs):
        report = get_report(id)

        if report is None:
            return HttpResponse("Running")

        df = pd.DataFrame(report)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')

        response.write(csv_buffer.getvalue().encode('utf-8'))

        return response
