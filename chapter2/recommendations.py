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
# sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')


# 为评论者打分
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # 排序
    scores.sort()
    scores.reverse()
    return scores[0:n]


# print toMatches(critics, 'Toby', n=3)

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result






def getRecommendations(prefs,person,similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other==person:
            continue
        sim=similarity(prefs,person,other)

        if sim<=0:
            continue
        for item  in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim

                simSums.setdefault(item,0)
                simSums[item]+=sim


    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

# print getRecommendations(critics,'Toby')
# print getRecommendations(critics,'Toby',similarity=sim_distance)

#coding= utf-8
def loadMovieLens(path='F:/cloud/ML/Collective_Intelligence/collective/chapter2/chapter2_last/ml-100k'):
    #获取影片标题
    movies = {}
    for line in open(path+'/u.item'):
        (id,title) = line.split('|')[0:2]
        movies[id] = title
        # print(movies)
# loadMovieLens()

#加载数据
    prefs={}
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts) = line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

prefs =loadMovieLens()
print getRecommendations(prefs,'87')[0:30]