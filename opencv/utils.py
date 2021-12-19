from datetime import datetime
from .camera import LiveWebCam
from .models import MyModel


def get_value(frame):
    ext_time=datetime.now()
    ext_time=int(ext_time.strftime("%S"))
    if(ext_time%4==0):
        pep, tim=frame.time_people()
        MyModel.objects.create(people_count=pep, time=tim)

