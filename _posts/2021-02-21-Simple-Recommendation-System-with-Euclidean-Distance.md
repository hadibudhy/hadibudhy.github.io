---
title: "Simple Recommendation System with Euclidean Distance"
date: 2021-02-21
tags: [recommendation system, data science]
header:
excerpt: "Recommendation System, Case Studies, Data Science"
mathjax: "true"
---

# Simple Recommendation System with Euclidean Distance

**Today I want to make a simple recommendation system using this streaming music app user data:**


| |Cherrybelle|Kangen Band|Netral|PAS Band|SM*SH|The Rain|Ungu|
|---|---|---|---|---|---|---|--|
|Agus|4.0|4.5|2.5||3.5||5.0|
|Andi||2.0|5.0|4.5||||
|Angga||||||4.5||
|Indah||3.5|4.5|5.0|||4.0|
|Siti|4.0|4.0||1.0|5.0||3.5|
|Solihah|4.0|4.0||1.0|5.0||3.5|

**Notes**:

---

1. There are some sections in the  task that have not been practiced in the references. But, Google is always ready to help you when difficulties and errors come.
2. Distance is only formed if both users rate the same musician. If user X does not have another user partner who has rated the same musician then that user X has no distance to
anyone.
3. If there are two or more people having the same distance to a particular user select the first
one to appear.
4. It's okay if the recommendation generates an empty list because the closest distance has rated the same musician.
5. It's okay if the recommendation produces an empty list because it doesn't have any distance to anyone.
---
**Euclidean Distance Formula:**

$d(x,y) = \sqrt{\sum \limits_{k=1} ^{n}(x_{k} - y_{k})^{2}}$


## Functional Programming

### Step 1: Input User Data


```python
users = {'Agus':{'Cherrybelle': 4.0,
                 'Kangen Band': 4.5,
                 'Netral': 2.5,
                 'SM*SH': 3.5,
                 'Ungu': 5.0},
         'Andi':{'Kangen Band':2.0,
                 'Netral':5.0,
                 'PAS Band':4.5},
         'Angga':{'The Rain':4.5},
         'Indah':{'Kangen Band':3.5,
                  'Netral':4.5,
                  'PAS Band':5.0,
                  'Ungu':4.0},
         'Siti':{'Cherrybelle':4.0,
                 'Kangen Band':4.0,
                 'PAS Band':1.0,
                 'SM*SH':5.0,
                 'Ungu':3.5},
         'Solihah':{'Cherrybelle':4.0,
                 'Kangen Band':4.0,
                 'PAS Band':1.0,
                 'SM*SH':5.0,
                 'Ungu':3.5}}
names = ['Agus','Andi','Angga','Indah','Siti','Solihah']
```

### Step 2: Euclidean Distance Code


```python
# Import Library
from math import sqrt

# Euclidean Distance
def euclidean(rating1, rating2):
    distance = 0.0
    key_available = False
    for key in rating1.keys():
        if key in rating2.keys():
            key_available = True
            distance += (rating1[key]-rating2[key])**2
    distance = sqrt(distance)
    if key_available == True:
        return distance
```


```python
# Check Distance Between User
print('Andi -> Agus: ', euclidean(users['Agus'],users['Andi']))
print('Indah -> Agus: ', euclidean(users['Agus'],users['Indah']))
print('Siti -> Agus: ', euclidean(users['Agus'],users['Siti']))
print('Angga -> Agus: ', euclidean(users['Agus'],users['Angga']))
```

    Andi -> Agus:  3.5355339059327378
    Indah -> Agus:  2.449489742783178
    Siti -> Agus:  2.179449471770337
    Angga -> Agus:  None


The distance result between Angga and Agus is **None**. It happens because distance is only formed if both users rate the same musician **(Note 2)**. In Angga and Agus case, both users didn't rate the same musician.

| |Cherrybelle|Kangen Band|Netral|PAS Band|SM*SH|The Rain|Ungu|
|---|---|---|---|---|---|---|--|
|Agus|4.0|4.5|2.5||3.5||5.0|
|Angga||||||4.5||

### Step 3: Nearest Neighbor with Euclidean Distance


```python
#Nearest Neighbor
def NN(username, data):
  distances = []
  for user in data:
    if user != username:
      distance = euclidean(data[username], data[user])
      if distance != None:
          distances.append((distance, user))
  distances.sort()
  return distances
```


```python
#Check All of Agus Neighbor
NN('Agus', users)
```




    [(2.179449471770337, 'Siti'),
     (2.179449471770337, 'Solihah'),
     (2.449489742783178, 'Indah'),
     (3.5355339059327378, 'Andi')]




```python
#Check The Closest Neighbor
for name in names:
    neighbor = NN(name, users)
    if not neighbor:
        print('Closest Neighbor for '+name+ ': Unavailable')
    else:
        print('Closest Neighbor for '+name+ ': ',neighbor[0])
```

    Closest Neighbor for Agus:  (2.179449471770337, 'Siti')
    Closest Neighbor for Andi:  (1.6583123951777, 'Indah')
    Closest Neighbor for Angga: Unavailable
    Closest Neighbor for Indah:  (1.6583123951777, 'Andi')
    Closest Neighbor for Siti:  (0.0, 'Solihah')
    Closest Neighbor for Solihah:  (0.0, 'Siti')


Siti and Solihah have the same distance to become Agus closest neighbor. However, it shows that Siti is the first one that appear **(Note 3).**

### Step 4: Recommendation Function


```python
# Recommend Function
def recommend(username, data):
  recommendations = []
  try:
      nearest = NN(username, data)[0][1]
      nearestRatings = data[nearest]
      userRatings = data[username]
      for artist in nearestRatings:
        if artist not in userRatings:
          recommendations.append((nearestRatings[artist], artist))
      recommendations.sort(reverse=True)
      if not recommendations:
            return 'Sorry, recommendation for '+username+' is unavailable.'
      else:
            return recommendations
  except:
    return 'Sorry, recommendation for '+username+' is unavailable.'
```


```python
# Check The Recommendation
for name in names:
    print('Recommendation for '+name+ ': ',recommend(name, users))
```

    Recommendation for Agus:  [(1.0, 'PAS Band')]
    Recommendation for Andi:  [(4.0, 'Ungu')]
    Recommendation for Angga:  Sorry, recommendation for Angga is unavailable.
    Recommendation for Indah:  Sorry, recommendation for Indah is unavailable.
    Recommendation for Siti:  Sorry, recommendation for Siti is unavailable.
    Recommendation for Solihah:  Sorry, recommendation for Solihah is unavailable.


Recommendation for Angga is unavailable because Angga doesn't have any distance to anyone **(Note 5)**.

Recommendation for Siti, Solihah, and Indah are unavailable because the closest distance has rated the same musician **(Note 4)**.

| |Cherrybelle|Kangen Band|Netral|PAS Band|SM*SH|The Rain|Ungu|
|---|---|---|---|---|---|---|--|
|Agus|4.0|4.5|2.5||3.5||5.0|
|Andi||2.0|5.0|4.5||||
|Angga||||||4.5||
|Indah||3.5|4.5|5.0|||4.0|
|Siti|4.0|4.0||1.0|5.0||3.5|
|Solihah|4.0|4.0||1.0|5.0||3.5|

## Object Oriented Programming


```python
#Object Oriented Programming Vers.
class recommender:
  def __init__(self, data):
    self.data = data

  from math import sqrt
  def euclidean(self, username1, username2):
    rating1 = self.data[username1]
    rating2 = self.data[username2]
    distance = 0.0
    key_available = False
    for key in rating1.keys():
        if key in rating2.keys():
            key_available = True
            distance += (rating1[key]-rating2[key])**2
    distance = sqrt(distance)
    if key_available == True:
        return distance

  def NN(self, username):
      distances = []
      for user in self.data:
        if user != username:
          distance = self.euclidean(username, user)
          if distance != None:
              distances.append((distance, user))
      distances.sort()
      return distances

  def recommend(self, username):
      recommendations = []
      try:
          nearest = self.NN(username)[0][1]
          nearestRatings = self.data[nearest]
          userRatings = self.data[username]
          for artist in nearestRatings:
            if artist not in userRatings:
              recommendations.append((nearestRatings[artist], artist))
          recommendations.sort(reverse=True)
          if not recommendations:
                return 'Sorry, recommendation for '+username+' is unavailable.'
          else:
                return recommendations
      except:
        return 'Sorry, recommendation for '+username+' is unavailable.'
```


```python
#Check The OOP Vers.
users_r = recommender(users)

for name in names:
    print("Recommendation for "+name+ ": ",users_r.recommend(name))
```

    Recommendation for Agus:  [(1.0, 'PAS Band')]
    Recommendation for Andi:  [(4.0, 'Ungu')]
    Recommendation for Angga:  Sorry, recommendation for Angga is unavailable.
    Recommendation for Indah:  Sorry, recommendation for Indah is unavailable.
    Recommendation for Siti:  Sorry, recommendation for Siti is unavailable.
    Recommendation for Solihah:  Sorry, recommendation for Solihah is unavailable.
