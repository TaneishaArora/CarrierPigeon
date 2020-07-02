from make_call import joke_call

if __name__ == '__main__':
    with open("hit_list.txt", 'r') as hit_list:
        targets = hit_list.readlines()
        joke_call(targets)