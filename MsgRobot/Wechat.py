# coding: UTF-8
import pickle
import requests
import time
import json
import logging
# from MqSdk import AmqpConnector
from typing import List, Dict, Iterable
import traceback

logger = logging.getLogger(name="MsgRobot")


def send(*args, **kwargs) -> Dict[str, str]:
    """发送企业微信消息"""
    res = requests.post(*args, **kwargs).json()
    if res["errcode"] != 0:
        logger.critical(
            "fail to send http post:\n *args={}\n **kwargs={}\n response={}".format(
                args, kwargs, json.dumps(res)
            )
        )
    return res


class WechatGroupRobot(object):
    """企业微信群机器人"""

    def __init__(self, key: str):
        """初始化企业微信群机器人

        Args:
            key(str): 机器人创建时的密钥
        """
        self._key = key

    def send_msg(
        self,
        message: str,
        mentioned_list: List[str] = list(),
        mentioned_mobile_list: List[str] = list(),
    ) -> Dict[str, str]:
        """发送企业微信消息

        Args:
            message(str): 要发送的消息
            mentioned_list(List[str]): 要@的用户
            mentioned_list(List[str]): 要@的用户手机号
        
        Returns:
            (Dict[str, str]): 发送的返回结果
        """
        headers = {"Content-Type": "text/plain"}
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(
            self._key
        )
        send_data = {
            "msgtype": "text",  # 消息类型，此时固定为text
            "text": {
                "content": message,  # 文本内容，最长不超过2048个字节，必须是utf8编码
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list,
            },
        }
        return send(url=send_url, headers=headers, json=send_data)

    def send_md(
        self,
        message: str,
        mentioned_list: List[str] = list(),
        mentioned_mobile_list: List[str] = list(),
    ) -> Dict[str, str]:
        """发送企业微信markdown消息

        Args:
            message(str): 要发送的markdown消息
            mentioned_list(List[str]): 要@的用户
            mentioned_list(List[str]): 要@的用户手机号

        Returns:
            (Dict[str, str]): 发送的返回结果
        """
        headers = {"Content-Type": "text/plain"}
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(
            self._key
        )
        send_data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": message,  # 文本内容，最长不超过2048个字节，必须是utf8编码
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list,
            },
        }
        return send(url=send_url, headers=headers, json=send_data)


class WechatRobot(object):
    """企业微信发送消息接口,可以通过python给企业微信用户发送消息"""

    def __init__(self, app_config: Dict[str, str]):
        """初始化企业微信接口,读取配置文件

        Args:
            app_config(Dict[str, str]): 配置文件

                corp_id (str): 企业id

                secret_id (str): app密码id

                agent_id (str): app的agent id

        """
        self._config = app_config
        for key in ["corp_id", "secret_id", "agent_id"]:
            if key not in self._config.keys():
                raise ValueError("config配置错误,缺少{}字段".format(key))

    def _get_access_token(self):
        """获取token,如果超时就重新请求"""
        try:
            assert 0 < time.time() - float(self._config["token_time"]) < 7260 and self._config["token"]
        except Exception:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            values = {
                "corpid": self._config["corp_id"],
                "corpsecret": self._config["secret_id"]
            }
            req = requests.post(url, params=values)
            data = json.loads(req.text)
            self._config["token"] = data["access_token"]
            self._config["token_time"] = str(time.time())
        return self._config["token"]

    def send_msg(self, message: str, receiver: Iterable[str]) -> Dict[str, str]:
        """特定给用户发送信息

        Args:
            message(str):要发送的信息
            receiver(str/list):
                收件人,如果是str则不同收件人名字用|隔开,例如chongdanpan|yifanyang|qifangsu。

        Returns:
            Dict[str, str]:发送结果
        """
        if isinstance(receiver, Iterable) and not isinstance(receiver, str):
            receiver = "|".join(list(receiver))
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self._get_access_token()
        )
        send_values = {
            "touser": receiver,
            "msgtype": "text",
            "agentid": self._config["agent_id"],
            "text": {"content": message},
            "safe": "0",
        }
        send_data = bytes(json.dumps(send_values), "utf-8")
        return send(url=send_url, data=send_data)

# class WechatClient(object):
#     def __init__(self):
#         """企业微信客户端,负责将消息投递到rabbitmq里并通过server发送"""
#         self._conn = DBEncrypt.get_mysql_conn(sql_account)
#         self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
#         sql = "SELECT * FROM wechat_config.amqp_config limit 1;"
#         self._cursor.execute(sql)
#         self._config = self._cursor.fetchone()
#         amqp_config = {
#             "user": self._config["amqp_user"],
#             "password": self._config["amqp_pwd"],
#             "host": self._config["amqp_host"],
#             "port": self._config["amqp_port"],
#             "Exchange": self._config["exchange"],
#         }
#         self._sender = AmqpConnector(amqp_config, sender=True, exchange_type="topic")

#     def send_msg(self, msg: str, app: str, receiver=[]):
#         """发送消息给app指定接收者

#         Args:
#             msg(str):发送的消息
#             app(str):使用的app名字
#             receiver(list):接收者，如果为空就会用初始化时定义的接收者
#         """
#         data = pickle.dumps((msg, receiver))
#         self._sender.send(data, routing_key=app)


# class WechatServer(object):
#     def __init__(self, app):
#         """企业微信服务,负责从rabbitmq里接收企业微信消息并发送给对应用户

#         Args:
#             app(str): 用的app名字,需要在数据库中配置
#         """
#         self.app = app
#         self._conn = DBEncrypt.get_mysql_conn(sql_account)
#         self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
#         sql = "SELECT * FROM wechat_config.amqp_config;"
#         self._cursor.execute(sql)
#         config = self._cursor.fetchone()
#         amqp_config = {
#             "user": config["amqp_user"],
#             "password": config["amqp_pwd"],
#             "host": config["amqp_host"],
#             "port": config["amqp_port"],
#             "queue_name": app,
#             "exchange": config["exchange"],
#         }
#         self.wechat = Wechat(app)
#         self.receiver = AmqpConnector(amqp_config, sender=False, exchange_type="topic")

#     def serve(self):
#         """开始接收消息并转发到企业微信"""
#         self.receiver.start_recv(
#             callback=self._forward, auto_ack=True, routing_key="#.{}".format(self.app)
#         )

#     def _forward(self, data):
#         """从rabbitmq接收消息并转发给wechat app用户"""
#         self.wechat.send_msg(*pickle.loads(data))
