from rest_framework import status
from rest_framework.response import Response
from rest_framework import status, permissions, views
from cms_app.models import *
from django.utils import timezone
from backend_gsip.permissions import PermissionMixin


class DashboardViewApi(PermissionMixin, views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        self.permission_check("system.view_dashboard")

        # Ambil parameter dari query params
        # Format: 'May 2021'
        start_month = request.query_params.get("start_month", None)
        # Format: 'October 2023'
        end_month = request.query_params.get("end_month", None)

        # Jika tidak ada rentang waktu diberikan, set default ke 6 bulan terakhir
        if not start_month or not end_month:
            end_date = timezone.now()
            start_date = end_date - timezone.timedelta(days=6 * 30)  # 6 bulan terakhir
        else:
            # Parsing bulan dan tahun dari input
            start_date = timezone.datetime.strptime(start_month, "%B %Y")
            end_date = timezone.datetime.strptime(end_month, "%B %Y")

        # Membuat list untuk grafik
        grafik_month = []
        grafik_visitors = []
        grafik_register = []
        current_date = start_date
        while current_date <= end_date:
            # Format bulan untuk tampilan
            month_name = current_date.strftime("%B %Y")
            grafik_month.append(month_name)
            # Menghitung total visitor dan meeting untuk bulan tersebut
            visitor_count = Visitor.objects.filter(
                created_at__year=current_date.year, created_at__month=current_date.month
            ).count()
            grafik_visitors.append(visitor_count)
            # Pindah ke bulan berikutnya
            current_date = (
                current_date.replace(day=1) + timezone.timedelta(days=31)
            ).replace(day=1)

        total_visitors = Visitor.objects.all().count()

        response = {
            "total_visitors": total_visitors,
            "grafik_month": grafik_month,
            "grafik_visitors": grafik_visitors,
            "grafik_register": grafik_register,
        }

        return Response(response, status=status.HTTP_200_OK)
