# 引入redirect重定向模块
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse, JsonResponse
# 引入刚才定义的ArticlePostForm表单类
from comment.models import Comment
from message.models import Starmessage
from user.models import Profile
from .forms import BlogPostForm
# 引入User模型
from django.contrib.auth.models import User
import json

from .models import BlogPost, Like, Collect

prefix = "http://49.234.51.41/"

class Blog:
    @staticmethod
    # 创建帖子
    def createBlog(request):
        # 判断用户是否提交数据
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 2,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            type = data.get("type")
            profile = Profile.objects.get(user_id=request.user.id)
            blog = BlogPost.objects.create(user=profile)
            blog.type = type
            blog.save()
            # 完成后返回到文章列表
            return JsonResponse({
                "status": 0,
                "message": "创建帖子成功",
                "blogid": blog.id
            })
        # 如果用户请求获取数据
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 删除帖子
    def deleteBlog(request):
        # 判断用户是否提交数据
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 2,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("blogid")
            profile = Profile.objects.get(user_id=request.user.id)
            try:
                blog = BlogPost.objects.filter(user=profile, id=blogid)
            except:
                # 不存在这样的帖子
                return JsonResponse({
                    "status": 2,
                    "message": "不存在该帖子",
                    "blogid": blogid,
                    "userid": profile.user_id
                })
            blog.delete()
            return JsonResponse({
                "status": 0,
                "message": "已删除该帖子",
                "userid": profile.user_id
            })
        # 如果用户请求获取数据
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 修改帖子
    def editBlog(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 4,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("id")
            title = data.get("name")
            content = data.get("textcontent")
            htmlcontent = data.get("htmlcontent")
            type = data.get("type")
            if blogid is not None and type is not None:
                try:
                    blog = BlogPost.objects.get(id=blogid)
                    blog.title = title
                    blog.content = content
                    blog.htmlcontent = htmlcontent
                    blog.type = type
                    blog.save()
                    return JsonResponse({
                        "status": 0,
                        "message": "帖子修改成功！"
                    })
                except:
                    return JsonResponse({
                        "status": 2,
                        "message": "帖子修改失败"
                    })
            else:
                return JsonResponse({
                    "status": 3,
                    "message": "blogid或type必填！"
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取帖子详情
    def getBlogInfo(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 3,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("id")
            print(blogid)
            print(0)
            if blogid is not None:
                blog = BlogPost.objects.get(id=blogid)
                blog.readnum = blog.readnum + 1
                blog.save(update_fields=['readnum'])
                comments = Comment.objects.filter(blog=blogid).order_by("-created")
                print(9)
                print(blogid)
                json_tiplist = []
                print(2)
                for comment in comments:
                    # 获取用户信息
                    user_id = int(comment.user.user_id)
                    userprofile = Profile.objects.get(user_id=user_id)
                    # if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                    #     avatar = prefix + str(userprofile.avatar.url)
                    # else:
                    #     avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                    avatar = userprofile.avatar
                    json_dict = {}
                    json_dict["user_id"] = user_id
                    json_dict["comment_id"] = comment.id
                    json_dict["name"] = userprofile.user.username
                    json_dict["img"] = avatar
                    json_dict["textcontent"] = comment.body
                    json_dict["htmlcontent"] = "<p>" + comment.body + "</p>"
                    json_tiplist.append(json_dict)
                blog.tipnum = len(json_tiplist)
                blog.save()
                profile = Profile.objects.get(user_id=request.user.id)
                if Like.objects.filter(liker=profile, liked_id=blogid).exists():
                    is_like = 0
                else:
                    is_like = 1
                if Collect.objects.filter(collector=profile, collectBlog_id=blogid).exists():
                    is_collect = 0
                else:
                    is_collect = 1
                return JsonResponse({
                    "status": 0,
                    "message": "帖子详情查看成功！",
                    "data": {
                        "title": str(blog.title),
                        "textcontent": str(blog.content),
                        "htmlcontent": blog.htmlcontent,
                        "type": blog.type,
                        "date": blog.created,
                        "readnum": blog.readnum,
                        "tipnum": blog.tipnum,
                        "likenum": blog.likenum,
                        "is_like": is_like,
                        "is_collect": is_collect,
                        "tiplist": json_tiplist
                    }
                })

            else:
                return JsonResponse({
                    "status": 2,
                    "message": "查看帖子失败"
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取用户所有帖子信息
    def getAllBlogs(request):
        if request.method == "POST":
            data = json.loads(request.body)
            userid = data.get('id')
            if userid == 0:
                userid = request.user.id
            profile = Profile.objects.get(user_id=userid)
            blogs = BlogPost.objects.filter(user=profile).order_by("-created")
            json_list = []
            for blog in blogs:
                is_like = 0
                profile = Profile.objects.get(user_id=request.user.id)
                if Like.objects.filter(liker=profile, liked_id=blog.id).exists():
                    is_like = 0
                else:
                    is_like = 1
                if Collect.objects.filter(collector=profile, collectBlog_id=blog.id).exists():
                    is_collect = 0
                else:
                    is_collect = 1
                json_dict = {}
                json_dict["blogid"] = blog.id
                json_dict["title"] = blog.title
                json_dict["textcontent"] = blog.content
                json_dict["htmlcontent"] = blog.htmlcontent
                json_dict["date"] = blog.created
                json_dict["readnum"] = blog.readnum
                json_dict["likenum"] = blog.likenum
                json_dict["tipnum"] = blog.tipnum
                json_dict["is_like"] = is_like
                json_dict["is_collect"] = is_collect
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data":{
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 点赞/取消点赞
    def setBlogLike(request):
        if request.method == "POST":
            data = json.loads(request.body)
            blogid = data.get("id")
            like = data.get("type")  # 0 点赞，1取消点赞
            blog = BlogPost.objects.get(id=blogid)
            if not blog:
                return JsonResponse({
                    "status": 2,
                    "message": "不存在该作者或者该帖子"
                })
            if like == 1:
                blog.is_like = 1
                blog.save()
                profile = Profile.objects.get(user_id=request.user.id)
                likes = Like.objects.filter(liker=profile, liked_id=blogid)
                for like in likes:
                    like.delete()
                    blog.likenum = blog.likenum - 1
                    blog.is_like = 1
                    blog.save()
                return JsonResponse({
                    "status": 0,
                    "message": "dislike success"
                })
            else:
                blog.is_like = 0
                blog.save()
                profile = Profile.objects.get(user_id=request.user.id)
                if Like.objects.filter(liker=profile, liked_id=blogid):
                    blog.is_like = 0
                    blog.save()
                    return JsonResponse({
                        "status": 2,
                        "isrepeat": "already like"
                    })
                else:
                    profile = Profile.objects.get(user_id=request.user.id)
                    like = Like.objects.create(liker=profile, liked_id=blogid)
                    like.save()
                    blog.likenum = blog.likenum + 1
                    blog.is_like = 0
                    blog.save()
                    return JsonResponse({
                        "status": 0,
                        "message": str(like),
                    })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 收藏/取消收藏
    def setBlogCollect(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 2,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("id")
            collect = data.get("type")  # 0收藏，1 取消收藏
            blog = BlogPost.objects.get(id=blogid)
            if not blog:
                return JsonResponse({
                    "status": 2,
                    "message": "不存在该作者或者该帖子"
                })
            if collect == 1: # 取消收藏
                profile = Profile.objects.get(user_id=request.user.id)
                collects = Collect.objects.filter(collector=profile, collectBlog_id=blogid)
                for collect in collects:
                    collect.delete()
                    blog.is_collect = 1
                    blog.save()
                return JsonResponse({
                    "status": 0,
                    "message": "discollect success"
                })
            else:
                profile = Profile.objects.get(user_id=request.user.id)
                if Collect.objects.filter(collector=profile, collectBlog_id=blogid):
                    return JsonResponse({
                        "status": 2,
                        "isrepeat": "already collect"
                    })
                else:
                    profile = Profile.objects.get(user_id=request.user.id)
                    collect = Collect.objects.create(collector=profile, collectBlog_id=blogid)
                    collect.save()
                    blog.is_collect = 0
                    blog.save()

                    # 生成消息通知并保存
                    starmessage = Starmessage.objects.create(user_id=request.user.id, blog_id=blog.id, to_user_id=blog.user.user.id)
                    # commentmessage.message = comment_body
                    starmessage.save()

                    return JsonResponse({
                        "status": 0,
                        "message": str(collect),
                    })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取用户的帖子论坛大致信息
    def getUserBlogInfo(requset):
        if requset.method == "POST":
            data = json.loads(requset.body)
            userid = data.get("id")
            if userid == 0:
                userid = requset.user.id
            try:
                user = User.objects.get(id=userid)
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "该用户不存在"
                })
            profile = Profile.objects.get(user_id=userid)
            blogs = BlogPost.objects.filter(user=profile)
            blogNum = 0
            likeNum = 0
            tipNum = 0
            # if profile.avatar:
            #     avatar = prefix + str(profile.avatar.url)
            # else:
            #     avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
            avatar = profile.avatar

            if user:
                for blog in blogs:
                    likeNum = likeNum + blog.likenum
                    tipNum = tipNum + blog.tipnum
                    blogNum = blogNum + 1
                return JsonResponse({
                    "avatar": avatar,
                    "username": str(user.username),
                    "blogNum": blogNum,
                    "likeNum": likeNum,
                    "tipNum": tipNum,
                })
            # else:
            #     return JsonResponse({
            #         "status": 2,
            #         "message": "该用户不存在"
            #     })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取热门帖子信息列表
    def getHotBlogs(request):
        if request.method == "POST":
            data = json.loads(request.body)
            type = data.get("type")
            if type == 0:
                blogs = BlogPost.objects.order_by("-readnum")
            else:
                blogs = BlogPost.objects.filter(type=type).order_by("-readnum")
            print(blogs)
            json_list = []
            for blog in blogs:
                json_dict = {}
                profile = blog.user
                # if profile.avatar and hasattr(profile.avatar, 'url'):
                #     avatar = prefix + str(profile.avatar.url)
                # else:
                #     avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                avatar = profile.avatar
                json_dict['blogname'] = blog.title
                json_dict['avatar'] = avatar
                json_dict['readnum'] = blog.readnum
                json_dict['likenum'] = blog.likenum
                json_dict['tipnum'] = blog.tipnum
                json_dict['userid'] = blog.user.user_id
                json_dict['textcontent'] = blog.content
                json_dict['htmlcontent'] = blog.htmlcontent
                json_dict['blogid'] = blog.id
                user = User.objects.get(id=profile.user_id)
                json_dict['username'] = user.username
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    def getUserHotBlog(request):
        if request.method == "POST":
            data = json.loads(request.body)
            userid = data.get('id')
            if userid == 0:
                userid = request.user.id
            user = User.objects.get(id=userid)
            print(user)
            if user:
                print(userid)
                profile = Profile.objects.get(user_id=userid)
                blogs = BlogPost.objects.filter(user=profile).order_by('-readnum')
                json_list = []
                i = 0
                for blog in blogs:
                    json_dict = {}
                    json_dict['blogname'] = blog.title
                    json_dict['blogid'] = blog.id
                    json_dict['readnum'] = blog.readnum
                    json_list.append(json_dict)
                    i = i + 1
                    if i >= 5:
                        break
                return JsonResponse({
                    "status": 0,
                    "data": {
                        "list": json_list
                    }
                }, safe=False)
            else:
                return JsonResponse({
                "status": 2,
                "message": "不存在该用户"
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })


    @staticmethod
    # 获取用户所有评论信息
    def getMyComment(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "massage": "请先登录"
                })
            userid = request.user.id
            profile = Profile.objects.get(user_id=userid)
            comments = Comment.objects.filter(user=profile).order_by("-created")
            json_list = []
            for comment in comments:
                json_dict = {}
                blog = comment.blog
                profile = blog.user
                # if profile.avatar and hasattr(profile.avatar, 'url'):
                #     avatar = prefix + str(profile.avatar.url)
                # else:
                #     avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                avatar = profile.avatar
                user = User.objects.get(id=profile.user_id)
                json_dict['date'] = comment.created
                json_dict['blogid'] = blog.id
                json_dict['blogname'] = blog.title
                json_dict['content'] = comment.body
                json_dict['img'] = avatar
                json_dict['username'] = user.username
                json_dict['userid'] = user.id
                json_dict['readnum'] = blog.readnum
                json_dict['likenum'] = blog.likenum
                json_dict['tipnum'] = blog.tipnum
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })


    @staticmethod
    # 搜索帖子
    def search_blog(request):
        if request.method == "POST":
            data = json.loads(request.body)
            text = data.get("text")
            type = data.get("type")
            if type == 0:
                blogs = BlogPost.objects.all().order_by("-created")
            else:
                blogs = BlogPost.objects.filter(type=type).order_by("-created")
            json_list = []
            for blog in blogs:
                if re.search(text, blog.title):
                    json_dict = {}
                    profile = blog.user
                    json_dict['blogname'] = str(blog.title)
                    json_dict['blogid'] = blog.id
                    json_dict['content'] = str(blog.content)
                    json_dict['htmlcontent'] = blog.htmlcontent
                    json_dict['date'] = blog.created
                    json_dict['username'] = str(profile.user.username)
                    json_dict['userid'] = profile.user_id
                    json_dict['readnum'] = blog.readnum
                    json_dict['likenum'] = blog.likenum
                    json_dict['tipnum'] = blog.tipnum
                    json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 列出收藏帖子列表
    def get_collect_blog_list(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('userid')
            profile = Profile.objects.get(user_id=userid)
            collects = Collect.objects.filter(collector=profile)
            print(collects)
            json_list = []
            for collect in collects:
                blogid = collect.collectBlog_id
                blog = BlogPost.objects.get(id=blogid)
                json_dict = {}
                json_dict["blogid"] = blogid
                json_dict["title"] = blog.title
                json_dict["content"] = blog.content
                json_dict["created"] = blog.created
                profile = blog.user
                json_dict["author"] = profile.user.username
                json_dict["userid"] = profile.user_id
                json_dict["bio"] = profile.bio
                # if Collect.objects.filter(collector_id=userid, collectBlog_id=blogid):
                #     json_dict["is_collect"] = 0
                # else:
                #     json_dict["is_collect"] = 1
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取他人收藏帖子列表
    def get_other_collect_blog(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('id')
            if userid == 0:
                userid = request.user.id
            profile = Profile.objects.get(user_id=userid)
            collects = Collect.objects.filter(collector=profile)
            print(collects)
            json_list = []
            for collect in collects:
                blogid = collect.collectBlog_id
                blog = BlogPost.objects.get(id=blogid)
                json_dict = {}
                json_dict["blogid"] = blogid
                json_dict["title"] = blog.title
                json_dict["content"] = blog.content
                json_dict["created"] = blog.created
                profile = blog.user
                json_dict["author"] = profile.user.username
                json_dict["authorid"] = profile.author_id
                json_dict["bio"] = profile.bio
                # if Collect.objects.filter(collector_id=userid, collectBlog_id=blogid):
                #     json_dict["is_collect"] = 0
                # else:
                #     json_dict["is_collect"] = 1
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })


