from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from .models import MyModel
from .graph import get_plot

from pickle import FALSE
from .camera import LiveWebCam
from .utils import get_value


def index(request):
    return render(request, 'opencv/index.html')

def gen(camera):
    while True:
        try:
            frame = camera.findFaces(draw=FALSE)
            get_value(camera)
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            break


@gzip.gzip_page
def livecam_feed(request):
    cam = LiveWebCam()

    return StreamingHttpResponse(gen(cam),content_type='multipart/x-mixed-replace; boundary=frame')


def next_page(request):
    qs=MyModel.objects.all()
    x=[x.time for x in qs]
    y=[x.people_count for x in qs]
    chart=get_plot(x,y)
    return render(request, 'opencv/next_page.html',{'chart':chart})

