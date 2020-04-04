from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from download_video import Downloadvideo

# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Download(View):
    def post(self, request):
        key_name = request.POST.get('key_name')
        file_path = request.POST.get('file_path')
        try:
            download = Downloadvideo(key_name, file_path)
            results=download.run()
        except Exception as e:
            print(e)

        finally:
            results.append('下载完成')
            return HttpResponse(results)
