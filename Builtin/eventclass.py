# 自助查类，查到返回类对象，查不到返回None
def find_event_class(data: dict):
    if 'post_type' not in data:
        return None
    elif data['post_type'] == 'meta_event':
        if data['meta_event_type'] == 'heartbeat':
            return HeartBeat(data)
        elif data['meta_event_type'] == 'lifecycle':
            return LifeCycle(data)
        else:
            return None
    elif data['post_type'] == 'request':
        if data['request_type'] == 'friend':
            return FriendRequest(data)
        elif data['request_type'] == 'group':
            return GroupRequest(data)
        else:
            return None
    elif data['post_type'] == 'message':
        if data['message_type'] == "group":
            return GroupMessage(data)
        elif data['message_type'] == 'private':
            return PrivateMessage(data)
        else:
            return None
    elif data['post_type'] == 'notice':
        if data['notice_type'] == 'friend_recall':
            return FriendRecall(data)
        elif data['notice_type'] == 'group_recall':
            return GroupRecall(data)
        elif data['notice_type'] == 'group_increase':
            return GroupIncrease(data)
        elif data['notice_type'] == 'group_decrease':
            return GroupDecrease(data)
        elif data['notice_type'] == 'group_admin':
            return GroupAdmin(data)
        elif data['notice_type'] == 'group_upload':
            return GroupUpload(data)
        elif data['notice_type'] == 'group_ban':
            return GroupBan(data)
        elif data['notice_type'] == 'friend_add':
            return FriendAdd(data)
        elif data['notice_type'] == 'notify':
            if data['sub_type'] == 'poke' and 'group_id' in data:
                return GroupPoke(data)
            elif data['sub_type'] == 'poke' and 'sender_id' in data:
                return FriendPoke(data)
            elif data['sub_type'] == 'lucky_king':
                return LuckyKing(data)
            elif data['sub_type'] == 'honor':
                return GroupHonor(data)
            elif data['sub_type'] == 'title':
                return GroupTitle(data)
            else:
                return None
        elif data['notice_type'] == 'group_card':
            return GroupCard(data)
        elif data['notice_type'] == 'offline_file':
            return OfflineFile(data)
        elif data['notice_type'] == 'client_status':
            return ClientStatus(data)
        elif data['notice_type'] == 'essence':
            return Essence(data)
        else:
            return None
    else:
        return None


# 所有event的基类
class EventBase:
    # Moco自己定义的, 表示最详细的event类型
    type = ""
    # 时间戳
    time = 0
    # QQ号
    self_id = 0
    # event的类型, 只可能是 message, message_sent, request, notice, meta_event
    post_type = ""

    def __init__(self, data: dict):
        self.time = data['time']
        self.self_id = data['self_id']
        self.post_type = data['post_type']


# 所有请求(request)的基类
class Request(EventBase):
    request_type = ""

    def __init__(self, data):
        EventBase.__init__(self, data)
        self.request_type = data['request_type']


# 好友请求类
class FriendRequest(Request):
    user_id = 0
    comment = ""
    flag = ""

    def __init__(self, data):
        Request.__init__(self, data)
        self.user_id = data['user_id']
        self.comment = data['comment']
        self.flag = data['flag']


# 群请求
class GroupRequest(Request):
    sub_type = ''
    group_id = 0
    user_id = 0
    comment = ''
    flag = ''

    def __init__(self, data):
        Request.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.comment = data['comment']
        self.flag = data['flag']


# 通知基类
class Notice(EventBase):
    notice_type = ""

    def __init__(self, data):
        EventBase.__init__(self, data)
        self.notice_type = data['notice_type']


# 私聊消息撤回
class FriendRecall(Notice):
    user_id = 0
    message_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.user_id = data['user_id']
        self.message_id = data['message_id']


# 群消息撤回
class GroupRecall(Notice):
    user_id = 0
    group_id = 0
    operator_id = 0
    message_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.user_id = data['user_id']
        self.group_id = data['group_id']
        self.operator_id = data['operator_id']
        self.message_id = data['message_id']


# 群成员增加
class GroupIncrease(Notice):
    sub_type = ""
    group_id = 0
    operator_id = 0
    user_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.operator_id = data['operator_id']
        self.user_id = data['group_id']


# 群成员减少
class GroupDecrease(Notice):
    sub_type = ""
    group_id = 0
    operator_id = 0
    user_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.operator_id = data['operator_id']
        self.user_id = data['group_id']


# 群管理员变动
class GroupAdmin(Notice):
    sub_type = ""
    group_id = 0
    user_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.user_id = data['group_id']


# 群文件上传
class GroupUpload(Notice):
    group_id = 0
    user_id = 0
    file = {
        'id': '',
        'name': '',
        'size': 0,
        'busid': 0
    }

    def __init__(self, data):
        Notice.__init__(self, data)
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.file = data['file']


# 群禁言
class GroupBan(Notice):
    sub_type = ''
    group_id = 0
    operator_id = 0
    user_id = 0
    duration = 0

    # user_id = == 0 and duration = -1
    # 这个是全员禁言

    def __init(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.operator_id = data['operator_id']
        self.user_id = data['user_id']
        self.duration = data['duration']


# 好友添加
class FriendAdd(Notice):
    user_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.user_id = data['user_id']


# 好友戳一戳
class FriendPoke(Notice):
    sub_type = ""
    sender_id = 0
    user_id = 0
    target_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.sender_id = data['sender_id']
        self.user_id = data['user_id']
        self.target_id = data['target_id']


# 群内戳一戳
class GroupPoke(Notice):
    sub_type = ''
    group_id = 0
    user_id = 0
    target_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.target_id = data['target_id']


# 群红包运气王提示
class LuckyKing(Notice):
    sub_type = ''
    group_id = 0
    user_id = 0
    target_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.target_id = data['target_id']


# 群成员荣誉变更提示
# TODO test
class GroupHonor(Notice):
    honor = ''
    group_id = 0
    user_id = 0
    honor_type = ""

    def __init__(self, data):
        Notice.__init__(self, data)
        self.honor = data['honor']
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.honor_type = data['honor_type']


# 群成员头衔变更
class GroupTitle(Notice):
    sub_type = ''
    group_id = 0
    user_id = 0
    title = ''

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.title = data['title']


# 群成员名片更新
# 此事件不保证时效性, 仅在收到消息时校验卡片
class GroupCard(Notice):
    group_id = 0
    user_id = 0
    card_new = ''
    card_old = ''

    def __init__(self, data):
        Notice.__init__(self, data)
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.card_new = data['card_new']
        self.card_old = data['card_old']


# 接收到离线文件
class OfflineFile(Notice):
    user_id = 0
    file = {
        'name': '',
        'size': 0,
        'url': ''
    }

    def __init__(self, data):
        Notice.__init__(self, data)
        self.user_id = data['user_id']
        self.file = data['file']


# 其他客户端在线状态变更
class ClientStatus(Notice):
    client = {
        'app_id': 0,
        'device_name': '',
        'device_kind': ''
    }
    online = True

    def __init__(self, data):
        Notice.__init__(self, data)
        self.client = data['client']
        self.online = data['online']


# 精华消息变更
class Essence(Notice):
    sub_type = ''
    group_id = 0
    sender_id = 0
    operator_id = 0
    message_id = 0

    def __init__(self, data):
        Notice.__init__(self, data)
        self.sub_type = data['sub_type']
        self.group_id = data['group_id']
        self.sender_id = data['sender_id']
        self.operator_id = data['operator_id']
        self.message_id = data['message_id']


# post_type 是 message 或者 message_send
# message_send 是自身信息回报
class Message(EventBase):
    # 信息类型
    message_type = ""
    # 私聊or群发
    sub_type = ""
    # 消息ID
    message_id = 0
    # 用户QQ
    user_id = 0
    # 消息
    message = ""
    # 原始消息
    raw_message = ""
    # 字体
    font = 0
    # 发送者详细信息
    sender = {
        # 年龄
        "age": 0,
        # 昵称
        "nickname": "",
        # 性别
        "sex": "",
        # 用户QQ号
        "user_id": 0
    }

    def __init__(self, data):
        EventBase.__init__(self, data)
        self.message_type = data['message_type']
        self.sub_type = data['sub_type']
        self.message_id = data['message_id']
        self.user_id = data['user_id']
        self.message = data['message']
        self.raw_message = data['raw_message']
        self.font = data['font']
        self.sender = data['sender']


# 群聊消息
class GroupMessage(Message):
    # QQ群号
    group_id = 0
    # 匿名字段，可能是None
    anonymous = {
        "id": 0,
        "name": "",
        "flag": ""
    }

    def __init__(self, data):
        Message.__init__(self, data)
        self.group_id = data['group_id']
        self.anonymous = data['anonymous']


# 私聊消息
class PrivateMessage(Message):
    # 接收者QQ
    target_id = 0

    # 临时会话来源，不用(有封号危险)
    # temp_source = 0
    def __init__(self, data):
        Message.__init__(self, data)
        self.target_id = data['target_id']


# post_type 是 meta_event
# go-cqhttp 元数据就基类
class MetaEvent(EventBase):
    # 元数据类型
    meta_event_type = ""

    def __init__(self, data):
        EventBase.__init__(self, data)
        self.meta_event_type = data['meta_event_type']


# 心跳包, 最常见也是最烦的包
class HeartBeat(MetaEvent):
    # status 是 Heartbeat 里的数据结构
    status = {
        # 程序是否可用
        "app_enabled": True,
        # 程序是否正常
        "app_good": True,
        # 程序是否初始化完毕
        "app_initialized": True,
        # 在Docs没出现?
        "good": True,
        # 是否在线
        "online": True,
        # 插件是否正常
        "plugins_good": None,
        # 统计信息
        "stat": {
            # 收包数
            "packet_received": 0,
            # 发包数
            "packet_sent": 0,
            # 丢包数
            "packet_lost": 0,
            # 信息接收数
            "message_received": 0,
            # 信息发送数
            "message_sent": 0,
            # 连接断开次数
            "disconnect_times": 0,
            # 连接丢失次数
            "lost_times": 0,
            # 最后一次消息时间
            "last_message_time": 0
        }
    }
    interval = 5000

    def __init__(self, data):
        MetaEvent.__init__(self, data)
        self.status = data['status']
        self.interval = data['interval']


# 生命周期
class LifeCycle(MetaEvent):
    sub_type = ''

    def __init__(self, data):
        EventBase.__init__(self, data)
        self.sub_type = data['sub_type']
