import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from blog.models import BlogPost
from comment.models import Comment
from message.models import Commentmessage
from user.models import Profile
# Create your views here.

prefix = "http://49.234.51.41/"

class CreateComment:
    @staticmethod
    # 发表评论
    def post_comment(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                blog_id = data.get('id')
                comment_body = data.get('text')
                # 尝试评论
                # 创建新的评论对象
                print(blog_id)
                print(request.user.id)
                profile = Profile.objects.get(user_id=request.user.id)
                comment = Comment.objects.create(user=profile, blog_id=blog_id)
                comment.body = comment_body
                # 保存后提交
                comment.save()
                blog = BlogPost.objects.get(id=blog_id)
                print(blog_id)
                blog.tipnum = blog.tipnum + 1
                blog.save(update_fields=['tipnum'])
                print(blog.tipnum)

                # 生成消息通知并保存
                print(blog.user.id)
                commentmessage = Commentmessage.objects.create(user_id=request.user.id, blog_id=blog_id, to_user_id=blog.user.user.id)
                # commentmessage.message = comment_body
                commentmessage.save()

                # 获取用户信息
                user_id = int(request.user.id)
                userprofile = Profile.objects.get(user_id=user_id)
                # if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                #     avatar = prefix + str(userprofile.avatar.url)
                # else:
                #     avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                avatar = profile.avatar
                return JsonResponse({
                        "error_code": 0,
                        "data": {
                          "status": 0,
                          "id": str(comment.id),
                          "userid": request.user.id,
                          "name": str(request.user),
                          "avatar": avatar
                        }
                    })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请登录后再评论！"
            })




