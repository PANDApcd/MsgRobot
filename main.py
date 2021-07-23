# encoding: utf-8
from MsgRobot import WechatGroupRobot, WechatRobot

if __name__ == "__main__":
    config = {"agent_id": "1000002", "secret_id": "7ykrpJXia3nSW0bWjG3R-w9M2HmBx0SOZNlvHhh8ocQ", "corp_id": "wwdf553e3840115c0c"}
    wechat = WechatRobot(config)
    # wechat.send_msg("hi", "PanChongDan")
    key = "7979b0e7-8ac2-4b1a-9ee6-436da920d231"
    robot = WechatGroupRobot(key)
    robot.send_msg("test")