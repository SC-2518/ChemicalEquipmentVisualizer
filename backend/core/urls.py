from django.urls import path
from .views import UploadView, SummaryView, HistoryListView, HistoryDetailView, PDFReportView, ApiRootView

urlpatterns = [
    path('', ApiRootView.as_view(), name='api_root'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('history/', HistoryListView.as_view(), name='history_list'),
    path('history/<uuid:pk>/', HistoryDetailView.as_view(), name='history_detail'),
    path('report/<uuid:pk>/', PDFReportView.as_view(), name='pdf_report'),
]
