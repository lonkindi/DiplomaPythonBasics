import requests
import time
from pprint import pprint

access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class UserVK:
    banned_friends = 0

    def __init__(self, vk_token, uid):
        self.token = vk_token
        self.user_id = uid
        self.friends_set = self.get_friends()
        self.groups_set = self.get_groups(0)
        self.groups_heap = self.get_groups_heap(self.friends_set)

    def get_params(self):
        return dict(
            user_id=self.user_id,
            access_token=self.token,
            v='5.89'
        )

    def get_groups_heap(self, f_list):
        friend_set = set()
        for friend in f_list:
            time.sleep(1 / 3)
            friend_set = friend_set | self.get_groups(uid=friend)
            print('*', end='')
        print()
        return friend_set

    def get_user_info(self):
        params = self.get_params()
        # params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/users.get', params)
        return response.json()

    def get_friends(self):
        time.sleep(1 / 3)
        # print('+', end='')
        params = self.get_params()
        # params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_set = set(response.json()['response']['items'])
        print('Всего друзей: ', len(friend_set))
        return friend_set

    def get_groups(self, uid=None, extended=0):
        groups_set = set()
        params = self.get_params()
        if not uid:
            uid = self.user_id
        params['user_id'] = uid
        params['extended'] = extended
        response = requests.get('https://api.vk.com/method/groups.get', params)
        resp_err = response.json().get('error')
        if not resp_err:
            groups_set = set(response.json()['response']['items'])
        else:
            # pprint(response.json().get('error')['error_msg'])
            self.banned_friends += 1
            # groups_set = set(response.json().get('error')['error_msg'])
        # pprint(groups_list)
        return groups_set


# class UserVK(BaseUser):
#     def __init__(self, vk_token, user_id):
#         self.token = vk_token
#         self.user_id = user_id
#         self.groups_set = self.get_groups(0)
#         self.friend_set = self.get_friends()

if __name__ == '__main__':
    user_id = 327379059  # input('Введите id пользователя ВК или его имя: ')
    test_user = UserVK(access_token, user_id)
    f_set = test_user.friends_set
    g_set = test_user.groups_set
    # for friend in f_set:
    #     pass
    print('Забаненых и приватных друзей:', test_user.banned_friends)
    print('Добавлено друзей: ', len(test_user.friends_set))
    print('Добавлено групп пользователя: ', len(test_user.groups_set))
    print('Всего групп у всех друзей: ', len(test_user.groups_heap))
    print('Группы пользователя, в которых не состоят его друзья: ', test_user.groups_set - test_user.groups_heap)


# 'af9c7f37dc361ad97***e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
