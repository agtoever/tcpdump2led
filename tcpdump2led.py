import threading
import time
import sys

SND_HUB_ON = (0, .2)    # sending hub led wait time + on time in sec
RCV_HUB_ON = (.2, .2)  # reveiving hub led wait time + on time in sec
LINK_ON = (0, .4)       # link led wait time + on time in sec
STATES = ('off', 'on')


def state_flip(state: str):
    return STATES[(STATES.index(state) + 1) % len(STATES)]


def signal_item(item: str, timing: tuple) -> None:
    cur_state = STATES[0]
    for t in timing:
        time.sleep(t)
        cur_state = state_flip(cur_state)
        print(f'{item} switched to {cur_state}')


def signal(from_id: str, to_id: str) -> None:
    for args in (
            (from_id, SND_HUB_ON),
            (from_id + ' > ' + to_id, LINK_ON),
            (to_id, RCV_HUB_ON)):
        threading.Thread(target=signal_item, args=args).start()


def process_line(line: str) -> tuple:
    # Skip IP6 lines
    if 'IP6' in line:
        return

    if 'IP' in line and ' > ' in line:
        start_src_ip = end_src_ip = line.find('IP ') + 3
        for _ in range(4):
            end_src_ip = line.find('.', end_src_ip + 1)
        start_dst_ip = end_dst_ip = line.find(' > ') + 3
        for _ in range(4):
            end_dst_ip = line.find('.', end_dst_ip + 1)
        return (line[start_src_ip:end_src_ip], line[start_dst_ip:end_dst_ip])


def main():
    with sys.stdin as input_stream:
        while True:
            line = input_stream.readline()
            if 'IP6' not in line and 'IP' in line and ' > ' in line:
                hub_in, hub_out = process_line(line)
                signal(hub_in, hub_out)


if __name__ == "__main__":
    main()
