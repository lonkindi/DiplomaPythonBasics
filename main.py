import requests
import time
import json
from pprint import pprint

access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
g_diff = {32653825, 31234561, 142573065, 101095054, 79851157, 115260441, 118840613, 55706674, 36220599, 102532920, 33587514, 68812734, 262340, 79798470, 123119686, 71888712, 38290762, 89931, 80650444, 131099725, 54012242, 111410132, 69786071, 124319704, 83460959, 28778720, 114735455, 148095071, 44150887, 31916136, 40567146, 136958443, 70905722, 92471547, 37735548, 32405757}


class UserVK:
    banned_friends = 0

    def __init__(self, vk_token, uid):
        self.token = vk_token
        self.user_id = uid
        self.friends_set = self.get_friends()
        self.groups_set = self.get_groups()
        #self.groups_heap = self.get_groups_heap(self.friends_set)
        self.groups_diff = g_diff #self.groups_set - self.groups_heap

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

    # def get_user_info(self):
    #     params = self.get_params()
    #     # params['user_id'] = self.user_id
    #     response = requests.get('https://api.vk.com/method/users.get', params)
    #     return response.json()

    def get_friends(self):
        time.sleep(1 / 3)
        # print('+', end='')
        params = self.get_params()
        # params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_set = set(response.json()['response']['items'])
        print('Всего друзей: ', len(friend_set))
        return friend_set

    def get_groups(self, uid=None):
        groups_set = ''
        params = self.get_params()
        if not uid:
            uid = self.user_id
        params['user_id'] = uid
        #params['extended'] = extended
        response = requests.get('https://api.vk.com/method/groups.get', params)
        resp_err = response.json().get('error')
        if not resp_err:
            groups_set = response.json()['response']['items']
        else:
            # pprint(response.json().get('error')['error_msg'])
            self.banned_friends += 1
            # groups_set = set(response.json().get('error')['error_msg'])
        # pprint(groups_list)
        # if extended == 0:
        #     groups_set = set(groups_set)
        return groups_set

    def output_diff(self):
        result_list = list()
        params = self.get_params()
        params['fields'] = 'members_count'
        groups_diff_str = str(self.groups_diff)
        params['group_ids'] = groups_diff_str
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        resp = response.json()['response']
        # pprint(resp)
        for g_item in resp:
            name = g_item['name']
            gid = g_item['id']
            try:
                members_count = g_item['members_count']
            except KeyError:
                members_count = 0
            result_list.append({'name': name, 'gid': gid, 'members_count': members_count})
        pprint(result_list)
        # diff_list = list()
        # for curr_group in self.groups_diff:
        #     print(curr_group)




if __name__ == '__main__':
    user_id = 327379059  # input('Введите id пользователя ВК или его имя: ')
    test_user = UserVK(access_token, user_id)

    # print('Заблокированных или приватных профилей друзей:', test_user.banned_friends)
    # print('Добавлено друзей: ', len(test_user.friends_set))
    # print('Количество групп, в которых пользователь является участником: ', len(test_user.groups_set))
    # print('Общее количество групп у всех друзей пользователя: ', len(test_user.groups_heap))
    print('Количество групп пользователя, в которых не состоит ни один из его друзей: ', len(test_user.groups_diff))

    test_user.output_diff()



# 'af9c7f37dc361ad97***e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
