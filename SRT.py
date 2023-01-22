from SharedMethod import build_status, is_done, calculate_tat_wt


def SRT(arrival_time_o, burst_time_1, io_time, burst_time_2):
    
    def find_min_rt_arrived(CPU_time, lst):
        lst.sort(key=lambda x: x[1])
        for i in lst:
            if CPU_time >= i[0]:
                return i[2], True

    def all_done(lst):
        for i in lst:
            if i[1] != 0:
                return False
            return True

    def reduce_bt(indx, lst):
        for i in range(len(lst)):
            if lst[i][-1] == indx:
                lst[i][1] -= 1
                if lst[i][1] == 0:
                    del lst[i]
                    return lst, True
        return lst, False
    srtf = []
    indx = 0
    CPU_time = 0
    for dct in data:
        srtf.append([dct['at'], dct['bt'], indx])
        indx += 1
    srtf.sort()
    while not all_done(srtf):
        index, has_arrived = find_min_rt_arrived(CPU_time, srtf)
        if has_arrived:
            CPU_time += 1
            srtf, is_done = reduce_bt(index, srtf)
            if is_done:
                data[index]['ct'] = CPU_time
        return data

    # find turn around time and waiting time with 'calculate_tat_wt' function
    turn_around_time, waiting_time = calculate_tat_wt(
        arrival_time_o, complete_time, burst_time_1, burst_time_2, io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, CPU_time
