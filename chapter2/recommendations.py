# coding=utf-8
# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

# 相似度评价值：欧几里德与皮尔逊
from math import sqrt


# 欧几里德距离评价
def sim_distance(prefs, person1, person2):
    si = {}
    # print(prefs[person1])
    for item in prefs[person1]:
        # print(person1,score)
        if item in prefs[person2]:
            si[item] = 1
            # print(item)
            # print(si)
    # 都没关系
    if len(si) == 0:
        return 0

    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# print sim_distance(critics,'Lisa Rose','Gene Seymour')
# sim_distance(critics,'Lisa Rose','Gene Seymour')

#  皮尔逊相关评价

def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
            # print(si)

    n = len(si)

    # 两者没有共同之处
    if n == 0:
        return 1

    # 偏好求和-->电影分求和
    sum1 = sum([prefs[p1][it] for it in si])
    # print(sum1)
    sum2 = sum([prefs[p2][it] for it in si])

    # 平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    # print(sum1Sq)
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 两人各自的电影评分做积
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # 皮尔逊计算法
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    # print(sum1Sq)
    # print(pow(sum1,2))
    if den == 0:
        return 0
    r = num / den
    return r


# print sim_distance(critics,'Lisa Rose','Gene Seymour')
sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')


# 为评论者打分
def toMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # 排序
    scores.sort()
    scores.reverse()
    return scores[0:n]


print toMatches(critics, 'Toby', n=3)
