from usermanage import models
from usermanage.daka import main
import time
def getaddr(region,area,build):
    regionarr = ["东风校区", "科学校区", "禹州实习训练基地", "校外走读"]
    areaarr = [
        ["一区", "二区", "三区", "丰华区", "秋实区"],
        ["宿舍区"],
        ["宿舍区"],
        ["无"]
    ]
    buildarr = [
        [
            ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼"],
            ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼", "8号楼"],
            ["附1号楼", "附2号楼", "附3号楼"],
            ["北楼", "南楼"],
            ["5号楼", "7号楼", "8号楼"]
        ],
        [
            ["1号楼", "2号楼", "3号楼", "4号楼", "5号楼", "6号楼", "7号楼", "8号楼", "9号楼", "10号楼", "11号楼"]
        ],
        [
            ["一层：122-177", "二层：222-277", "三层：322-377", "四层：422-477", "五层：501-577", "六层：601-677"]
        ],
        [
            ["无"]
        ]
    ]
    regionstr = regionarr[int(region)]
    areastr = areaarr[int(region)][int(area)]
    buildstr = buildarr[int(region)][int(area)][int(build)]
    return regionstr,areastr,buildstr
def runs():
    datetime = time.strftime("%Y-%m-%d", time.localtime())
    count=models.User.objects.all().count()
    count=int(count)
    print(count)
    i=1
    while(i<=count):
        userobb=models.User.objects.get(id=i)
        schoolid = userobb.schoolid
        schoopassword = userobb.schoolpassword
        mobile = userobb.mobile
        homemobile = userobb.homemobile
        schoolgps = userobb.schoolgps
        dorm = userobb.dorm
        region = userobb.region
        area = userobb.area
        build = userobb.build
        schoollon = userobb.schoollon
        schoollat = userobb.schoollat
        addrstr=getaddr(region,area,build)
        region = addrstr[0]
        area = addrstr[1]
        build = addrstr[2]
        email= userobb.email
        reporttype="morn"
        gpslocation=""
        lat= 0
        lon= 0
        main.service(schoolid, schoopassword, mobile, homemobile, gpslocation, lat, lon, datetime, reporttype, region, area, build,
            dorm, schoolgps, schoollat, schoollon)
        i=i+1