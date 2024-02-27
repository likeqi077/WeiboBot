from WeiboBot import Bot
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment
from zhipuai import ZhipuAI

from datetime import datetime

cookies = ""
myBot = Bot(cookies=cookies)
client = ZhipuAI(api_key='')


@myBot.onNewMsg  # 被私信的时候触发
async def on_msg(chat: Chat):
    for msg in chat.msg_list:  # 消息列表
        print("被私信\n")
        print(f"{msg.sender_screen_name}:{msg.text}")
        print(msg)
        await myBot.send_message(uid=msg.sender_id, content=msg.text)
        print("end")


@myBot.onNewWeibo  # 首页刷到新微博时触发
async def on_weibo(weibo: Weibo):
    if weibo.original_weibo is None:  # 是原创微博
        print("首页微博\n")
        print(f"{weibo.text}")
        messages = [{'role': 'user', 'content': weibo.text}]
        response = client.chat.completions.create(
            model="glm-3-turbo",  # 填写需要调用的模型名称
            messages=messages
        )
        print("---------")
        print(response.choices[0].message.content)
        print("---------")
        await myBot.comment_weibo(weibo.mid, response.choices[0].message.content)


@myBot.onMentionCmt  # 提及我的评论时触发
async def on_mention_cmt(cmt: Comment):
    print("被艾特\n")
    print(f"{cmt.text}")


@myBot.onTick  # 每次循环触发
async def on_tick():
    print(datetime.now())
    print("hello")


if __name__ == '__main__':
    myBot.run()
