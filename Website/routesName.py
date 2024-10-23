from flask import Blueprint, render_template

routesPages = Blueprint("routes",__name__)

@routesPages.route('/',methods=['GET', 'POST'])
def index_page():
    return render_template("index.html")

@routesPages.route('/index',methods=['GET', 'POST'])
def home_page():
    return render_template("index.html")

@routesPages.route('/courses',methods=['GET', 'POST'])
def courses_page():
    return render_template("course.html")


@routesPages.route('/course',methods=['GET', 'POST'])
def course2_page():
    return render_template("course.html")

@routesPages.route("/bVids")
def bVids_page():
    videos = ["bus1.mp4","bus2.mp4","bus3.mp4"]  # list of video files
    return render_template("bVids.html", videos=videos)
    # return render_template("bVids.html")


@routesPages.route("/pVids")
def pVids_page():
    videos = ["prog1.mp4", "prog2.mp4"]  # list of video files
    return render_template("pVids.html", videos=videos)
    # return render_template("bVids.html")


@routesPages.route("/phyVids")
def phyVids_page():
    videos = ["phy1.mp4", "phy2.mp4"]  # list of video files
    return render_template("phyVids.html", videos=videos)
    # return render_template("bVids.html")


@routesPages.route("/jVids")
def jVids_page():
    videos = ["java1.mp4", "phy2.mp4"]  # list of video files
    return render_template("jVids.html", videos=videos)
    # return render_template("bVids.html")


@routesPages.route("/snippets")
def video_page():
    videos = ["vid1.mp4","vid2.mp4","bus4.mp4","vid3.mp4"]  # list of video files
    return render_template("snippets.html", videos=videos)
