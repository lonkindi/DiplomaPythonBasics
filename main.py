import requests
import time
from pprint import pprint

access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

class BaseUser:
    def __init__(self, vk_token, user_id):
        self.token = vk_token
        self.user_id = user_id
        self.friend_set = self.get_friends()
        self.groups_set = self.get_groups(0)

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.89'
        )

    def get_user_info(self):
        params = self.get_params()
        params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/users.get', params)
        return response.json()

    def get_friends(self):
        time.sleep(1 / 3)
        print('*', end='')
        params = self.get_params()
        params['user_id'] = self.user_id
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_list = set(response.json()['response']['items'])
        return friend_list

    def get_groups(self, extended):
        params = self.get_params()
        params['user_id'] = self.user_id
        params['extended'] = extended
        response = requests.get('https://api.vk.com/method/groups.get', params)
        # pprint(response.json())
        groups_list = set(response.json()['response']['items'])
        return groups_list


# class UserVK(BaseUser):
#     def __init__(self, vk_token, user_id):
#         self.token = vk_token
#         self.user_id = user_id
#         self.groups_set = self.get_groups(0)
#         self.friend_set = self.get_friends()

if __name__ == '__main__':
    user_id = 24863449#input('Введите id пользователя ВК или его имя: ')
    test_user = UserVK(access_token, user_id)
    print(test_user.friend_set)
    print(test_user.groups_set)

# print('Задача №1')
# user_1 = UserVK(access_token, user_id=24863449)
# user_2 = UserVK(access_token, user_id=327379059)
# print(
#     f'\nПользователь ВК id={user_1.user_id}, фамилия: {user_1.last_name}, имя: {user_1.first_name}, в друзьях: {len(user_1.friend_set)} чел. ')
# print(
#     f'Пользователь ВК id={user_2.user_id}, фамилия: {user_2.last_name}, имя: {user_2.first_name}, в друзьях: {len(user_2.friend_set)} чел. ')
# mutual_list = user_1.get_mutual(327379059)
# m_dict = {}
# for m_friend in mutual_list['response']:
#     m_dict[m_friend] = UserVK(access_token, m_friend)
# print(
#     f'\nПо данным функции API BK у пользователей {user_1.first_name} {user_1.last_name} и {user_2.first_name} {user_2.last_name} общих друзей - {len(mutual_list["response"])}, вот они:')
# for friend in m_dict:
#     cur_friend = m_dict.get(friend)
#     print(f'- {cur_friend.first_name} {cur_friend.last_name}')
# print(f'\nЗадача №2')
# mutual_list = user_1 & user_2
# print(
#     f'\nСогласно результата вычисления "user_1 & user_2" у пользователей {user_1.first_name} {user_1.last_name} и {user_2.first_name} {user_2.last_name} общих друзей - {len(mutual_list)}, вот они:')
# for friend in mutual_list:
#     print(f'- {friend.first_name} {friend.last_name}')
# print(f'\nЗадача №3')
# print(user_1)
# print(user_2)
# 'af9c7f37dc361ad97***e979d4be8143d4e6bc1c2466a4722c1f3fefc185e107719ebaa66a8ff92cdf3d8'
