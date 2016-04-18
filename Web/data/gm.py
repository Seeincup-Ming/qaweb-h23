__author__ = '163'
# -*- coding: utf-8 -*-
path = 'robot.txt'
def txt2dic():
    with open(path, 'r') as f:
        g = f.readlines()
        for a in g:
            if a.startswith('\t'):

                print 1,a
        gm_cmd = unicode(f.read(), 'utf-8')
    #gm_cmd.
    #print gm_cmd


gmcom_pcontrol = [
    {"cmd":'red/blue A skill B C','dpi':'红方/蓝方A号玩家在下一回合释放B技能，技能等级为C'},
    {"cmd":'red/blue A buff B C D','dpi':'红方/蓝方A号玩家添加B buff，buff等级为C，buff持续回合为D'},
    {"cmd":'red/blue A passive B C','dpi':'红方/蓝方A号玩家添加B被动技能，被动技能等级为C'},
    {"cmd":'red/blue A hp B','dpi':'设置红方/蓝方A号玩家血量为B'},
    {"cmd":'red/blue A eng B','dpi':'设置红方/蓝方A号玩家能量为B'},
    {"cmd":'red/blue A kill red/blue B','dpi':'红方/蓝方A号玩家杀死红方/蓝方B号玩家'},
    {"cmd":'default *','dpi':'设置默认指令,比如default red 1 skill 1 1 就是将默认指令设置成red 1 skill 1 1,之后不需要设置指令直接点击command就会执行red 1 skill 1 1。要取消默认指令可以直接打一个default就行了'},
    {"cmd":'group red/blue token A B','dpi':'给红方或者蓝方阵营加上令牌A,B表示令牌编号和等级'},
    {"cmd":'red/blue A revive','dpi':'表示红方或者蓝方卡牌复活'},
]

gmcom_update = [
    {"cmd":'update data','dpi':'游戏运行时热更数据文件'},
    {"cmd":'update vfx name','dpi':'游戏运行时热更name特效'},
    ]

gmcom_code = [
    {"cmd":'code ***','dpi':'游戏运行时，可以运行简单代码，比如查看table内的值等'},
]

gmcom_gcontrol = [
    {"cmd":'code ***','dpi':'游戏运行时，可以运行简单代码，比如查看table内的值等'},
]