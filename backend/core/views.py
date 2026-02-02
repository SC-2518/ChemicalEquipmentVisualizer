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
        if not serializer.is_valid():
            # Return first error message for frontend simplicity
            error_msg = str(next(iter(serializer.errors.values()))[0]) if serializer.errors else "Invalid file data"
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            
        file = serializer.validated_data['file']
        try:
            try:
                df = pd.read_csv(file)
                
                # Normalize columns: lowercase, replace _ with space, strip units
                original_cols = df.columns.tolist()
                df.columns = [c.split('(')[0].strip().replace('_', ' ').title() for c in df.columns]
                
                # Validation of normalized columns
                required_cols = {'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'}
                if not required_cols.issubset(set(df.columns)):
                    missing = required_cols - set(df.columns)
                    return Response({"error": f"Missing columns. Required: {list(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({"error": f"CSV Processing Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Server Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SummaryView(APIView):
    def get(self, request):
        # Get latest dataset by default
        latest_dataset = Dataset.objects.first() # Ordered by -upload_date in Meta
        if not latest_dataset:
            return Response({"message": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        # Type distribution and stats per type
        type_dist = list(latest_dataset.equipment.values('equipment_type').annotate(
            count=Count('equipment_type'),
            avg_flow=Avg('flowrate'),
            avg_press=Avg('pressure'),
            avg_temp=Avg('temperature')
        ))

        # Raw data points for scatter plot (limit to 50 for performance)
        raw_data = list(latest_dataset.equipment.all()[:50].values('equipment_name', 'flowrate', 'pressure', 'temperature'))

        return Response({
            "dataset_id": latest_dataset.id,
            "filename": latest_dataset.filename,
            "total_count": latest_dataset.total_records,
            "avg_flowrate": latest_dataset.avg_flowrate,
            "avg_pressure": latest_dataset.avg_pressure,
            "avg_temperature": latest_dataset.avg_temperature,
            "type_distribution": type_dist,
            "raw_data_points": raw_data
        })

class HistoryListView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetListSerializer

class HistoryDetailView(generics.RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

class PDFReportView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            equipment = dataset.equipment.all()
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        elements = []
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#0ea5e9"), # Primary Blue
            spaceAfter=12,
            fontName="Helvetica-Bold"
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor("#64748b"), # Gray 500
            spaceAfter=24,
        )
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor("#334155"), # Slate 800
            spaceBefore=20,
            spaceAfter=10,
            fontName="Helvetica-Bold"
        )

        # 1. Header Section
        elements.append(Paragraph("ChemVisualizer Analytics Report", title_style))
        elements.append(Paragraph(f"Dataset: {dataset.filename}", subtitle_style))
        elements.append(Paragraph(f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}", subtitle_style))
        elements.append(Spacer(1, 0.2 * inch))

        # 2. Executive Summary (Card-like table)
        elements.append(Paragraph("Executive Summary", section_header_style))
        summary_data = [
            [Paragraph("<b>Total Records</b>", styles['Normal']), Paragraph("<b>Avg Flowrate</b>", styles['Normal']), Paragraph("<b>Avg Pressure</b>", styles['Normal']), Paragraph("<b>Avg Temp</b>", styles['Normal'])],
            [f"{dataset.total_records}", f"{dataset.avg_flowrate:.1f} L/m", f"{dataset.avg_pressure:.1f} PSI", f"{dataset.avg_temperature:.1f} °C"]
        ]
        summary_table = Table(summary_data, colWidths=[1.5*inch]*4)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('FONTSIZE', (0, 1), (-1, 1), 14),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.4 * inch))

        # 3. Equipment Detailed Logs
        elements.append(Paragraph("Detailed Equipment Logs", section_header_style))
        
        # Table Header
        data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for eq in equipment:
            data.append([
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.1f}",
                f"{eq.pressure:.1f}",
                f"{eq.temperature:.1f}"
            ])

        table = Table(data, hAlign='LEFT', colWidths=[2.2*inch, 1.4*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#334155")),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.1, colors.HexColor("#cbd5e1")),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ]))
        
        elements.append(table)

        # Build PDF
        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Report_{dataset.filename}.pdf"'
        return response
