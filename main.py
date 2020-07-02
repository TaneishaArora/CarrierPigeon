from make_call import send_joke

if __name__ == '__main__':

    methods = ['text']

    with open("hit_list.txt", 'r') as hit_list:
        targets = hit_list.readlines()
        send_joke(targets, methods)