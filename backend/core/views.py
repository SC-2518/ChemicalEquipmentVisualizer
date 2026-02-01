from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, generics
from django.db.models import Count, Avg
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetListSerializer, FileUploadSerializer
import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime
from rest_framework.reverse import reverse

class ApiRootView(APIView):
    def get(self, request):
        return Response({
            "upload": reverse('upload', request=request),
            "summary": reverse('summary', request=request),
            "history": reverse('history_list', request=request),
        })

class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                df = pd.read_csv(file)
                # Validation of columns
                required_cols = {'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'}
                if not required_cols.issubset(df.columns):
                    return Response({"error": f"Missing columns. Required: {required_cols}"}, status=status.HTTP_400_BAD_REQUEST)

                # Create Dataset
                dataset = Dataset.objects.create(filename=file.name)
                
                # Bulk create equipment
                equipment_list = []
                for _, row in df.iterrows():
                    equipment_list.append(Equipment(
                        dataset=dataset,
                        equipment_name=row['Equipment Name'],
                        equipment_type=row['Type'],
                        flowrate=row['Flowrate'],
                        pressure=row['Pressure'],
                        temperature=row['Temperature']
                    ))
                Equipment.objects.bulk_create(equipment_list)

                # Calculate stats
                dataset.total_records = len(equipment_list)
                dataset.avg_flowrate = df['Flowrate'].mean() if not df.empty else 0
                dataset.avg_pressure = df['Pressure'].mean() if not df.empty else 0
                dataset.avg_temperature = df['Temperature'].mean() if not df.empty else 0
                dataset.save()

                # Maintain only last 5 datasets
                all_datasets = Dataset.objects.all().order_by('-upload_date')
                if all_datasets.count() > 5:
                    ids_to_keep = all_datasets[:5].values_list('id', flat=True)
                    Dataset.objects.exclude(id__in=ids_to_keep).delete()

                return Response(DatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SummaryView(APIView):
    def get(self, request):
        # Get latest dataset by default
        latest_dataset = Dataset.objects.first() # Ordered by -upload_date in Meta
        if not latest_dataset:
            return Response({"message": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        # Type distribution
        type_dist = list(latest_dataset.equipment.values('equipment_type').annotate(count=Count('equipment_type')))

        return Response({
            "dataset_id": latest_dataset.id,
            "filename": latest_dataset.filename,
            "total_count": latest_dataset.total_records,
            "avg_flowrate": latest_dataset.avg_flowrate,
            "avg_pressure": latest_dataset.avg_pressure,
            "avg_temperature": latest_dataset.avg_temperature,
            "type_distribution": type_dist
        })

class HistoryListView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetListSerializer

class HistoryDetailView(generics.RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class PDFReportView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, f"Report for {dataset.filename}")
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Summary Stats
        p.drawString(100, 700, f"Total Records: {dataset.total_records}")
        p.drawString(100, 680, f"Avg Flowrate: {dataset.avg_flowrate:.2f}")
        p.drawString(100, 660, f"Avg Pressure: {dataset.avg_pressure:.2f}")
        p.drawString(100, 640, f"Avg Temperature: {dataset.avg_temperature:.2f}")

        # Equipment Table (First 20 items)
        p.drawString(100, 600, "Details (First 20 items):")
        y = 580
        p.setFont("Courier", 10)
        p.drawString(50, y, f"{'Name':<20} {'Type':<15} {'Flow':<8} {'Press':<8} {'Temp':<8}")
        y -= 15
        
        for eq in dataset.equipment.all()[:20]:
            line = f"{eq.equipment_name[:20]:<20} {eq.equipment_type[:15]:<15} {eq.flowrate:<8.1f} {eq.pressure:<8.1f} {eq.temperature:<8.1f}"
            p.drawString(50, y, line)
            y -= 12
            if y < 50:
                p.showPage()
                y = 750
                p.setFont("Courier", 10)

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
