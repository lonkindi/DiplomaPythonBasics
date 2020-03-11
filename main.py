import requests
import json

vk_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class UserVK:
    banned_friends = 0
    friends_total = 0

    def __init__(self, vk_token, uid):
        self.token = vk_token
        self.user_id = uid
        self.friends_set = self.get_friends()
        self.groups_set = self.get_groups()
        self.groups_heap = self.get_groups_heap(self.friends_set)
        self.groups_diff = self.groups_set - self.groups_heap

    def get_params(self):
        return dict(
            user_id=self.user_id,
            access_token=self.token,
            v='5.103'
        )

    def get_friends(self):
        friend_set = set()
        params = self.get_params()
        params['fields'] = 'deactivated'
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friend_dict = response.json()['response']['items']
        self.friends_total = len(friend_dict)
        for friend in friend_dict:
            if friend.get('deactivated'):
                self.banned_friends += 1
            elif not friend.get('is_closed'):
                friend_set.add(friend['id'])
            else:
                self.banned_friends += 1
        return friend_set

    def get_groups_heap(self, f_list):
        friends_groups_set = set()
        counter = 0
        t_counter = len(f_list)
        temp_list = list()
        params = self.get_params()
        response_list = list()
        for friend in f_list:
            counter += 1
            t_counter -= 1
            temp_list.append(friend)
            if counter == 25 or t_counter == 0:
                params[
                    'code'] = f'var a = 0; var b =  {temp_list}; var s = ""; while (a != 25)' + '{s = s + API.groups.get({"user_id":b[a]}).items + ","; a = a + 1;}; return s;'
                response = requests.get('https://api.vk.com/method/execute', params)
                resp_list = response.json()['response'].split(',')
                response_list = response_list + resp_list
                counter = 0
                temp_list.clear()
                print('*', end='')
        response_set = set()
        for str_item in response_list:
            if str_item != '':
                response_set.add(int(str_item))
        friends_groups_set = friends_groups_set | response_set
        print()
        return friends_groups_set

    def get_groups(self, uid=None):
        params = self.get_params()
        if not uid:
            uid = self.user_id
        params['user_id'] = uid
        response = requests.get('https://api.vk.com/method/groups.get', params)
        groups_set = set(response.json()['response']['items'])
        return groups_set

    def output_diff(self):
        result_list = list()
        params = self.get_params()
        params['fields'] = 'members_count'
        groups_diff_str = str(self.groups_diff)
        groups_diff_str = groups_diff_str.replace('{', '')
        groups_diff_str = groups_diff_str.replace('}', '')
        params['group_ids'] = groups_diff_str
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        resp = response.json()['response']
        for g_item in resp:
            name = g_item['name']
            gid = g_item['id']
            try:
                members_count = g_item['members_count']
            except KeyError:
                members_count = 0
            result_list.append({'name': name, 'gid': gid, 'members_count': members_count})
        with open('groups.json', 'w', encoding='utf-8') as data_file:
            json.dump(result_list, data_file, ensure_ascii=False, indent=2)
            print('Сведения о "секретных" группах пользователя записаны в файл groups.json')


def users_search(uid):
    result_id = None
    params = dict(
        access_token=vk_token,
        v='5.103'
    )
    if str(uid).isnumeric():
        params['user_id'] = int(uid)
        response = requests.get('https://api.vk.com/method/users.get', params)
        resp = response.json()
        user_deactivated = resp['response'][0].get('deactivated')
        try:
            # user_deactivated =
            result_id = resp['response'][0]['id']
        except IndexError:
            result_id = None
        except TypeError:
            result_id = None
        except KeyError:
            result_id = None
        if user_deactivated != None:
            result_id = user_deactivated
    else:
        params['q'] = uid
        response = requests.get('https://api.vk.com/method/users.search', params)
        resp = response.json()['response']
        if resp['count'] == 1:
            if len(resp['items']) == 0:
                result_id = 'banned'
            else:
                result_id = resp['items'][0]['id']
        elif resp['count'] > 1:
            result_id = 'many'
    return result_id


if __name__ == '__main__':  # 'armo.appacha' 24863449 27406252 10754162 d.lonkin o.sevostyanova77 eshmargunov
    input_id = input('Введите id пользователя ВК или его имя: ')
    user_id = users_search(input_id)
    if user_id == None:
        print(f'Пользователь "{input_id}" не найден. Проверьте вводимые данные.')
    elif user_id == 'many':
        print(f'По вашему запросу: "{input_id}" найдено несколько пользователей. Уточните имя.')
    elif user_id == 'banned':
        print(f'Пользователь "{input_id}" заблокирован. Анализ невозможен.')
    elif user_id == 'deleted':
        print(f'Пользователь "{input_id}" удалён либо не существует. Анализ невозможен.')
    else:
        print(f'Пользователь "{input_id}" (id{user_id}) доступен для анализа ...')
        test_user = UserVK(vk_token, user_id)
        print('Друзей у пользователя: ', test_user.friends_total)
        print('Заблокированных или приватных профилей друзей:', test_user.banned_friends)
        print('Количество групп, в которых пользователь является участником: ', len(test_user.groups_set))
        print('Общее количество групп всех друзей пользователя: ', len(test_user.groups_heap))
        print('Количество групп пользователя, в которых не состоит ни один из его друзей: ', len(test_user.groups_diff))
        test_user.output_diff()
