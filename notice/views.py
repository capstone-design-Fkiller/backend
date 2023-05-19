from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from notice.models import Notice  
from notice.serializers import NoticeSerializer
# from rest_framework import viewsets
from rest_framework import generics
from django.core.paginator import Paginator

class NoticeView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request):
        try:
            notices = Notice.objects.all()
            if request.GET.get('page'):
                page = request.GET.get('page')
                paginator = Paginator(notices, 10)
                page_obj = paginator.page(page)
            serializer = NoticeSerializer(notices, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = NoticeSerializer(data = request.data) # json을 변환하게 된다.
        if serializer.is_valid():
            Notice = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeSerializer

    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            raise Http404
    
    # Notice의 detail 보기
    def get(self, request, pk, format=None):
        notice = self.get_object(pk)
        serializer = NoticeSerializer(notice)
        return Response(serializer.data)

    # Notice 수정하기
    def put(self, request, pk, format=None):
        notice = self.get_object(pk)
        serializer = NoticeSerializer(notice, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Notice 삭제하기
    def delete(self, request, pk, format=None):
        notice = self.get_object(pk)
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)