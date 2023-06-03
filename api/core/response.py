from rest_framework.response import Response as rest_response


class Response(rest_response):
    def __init__(self, status: int, message: str | None = None, data=None, **kwargs):
        response = {
            'status': "ok" if status in [200, 201, 204] else "error",
            'message': message,
            'data': data
        }

        super().__init__(data=response, status=status, **kwargs)
