from SharedMethod import calculate_tat_wt, is_done, build_status
from FCFS import find_next_process

# this method find the index of next process that want to execute in RR algorithm
def next_process_RR(process_list):
    l1 = process_list[1:]
    l1.append(process_list[0])
    return l1, l1[-1]


# this method implement Round Robin algorithm or 'RR' with time quantum 5
def RR(arrival_time_o, burst_time_1_o, io_time, burst_time_2_o):
    burst_time_1 = burst_time_1_o.copy()
    burst_time_2 = burst_time_2_o.copy()
    arrival_time = arrival_time_o.copy()
    io_finished_at = list()
    process_list = list()
    complete_time = list()
    response_time = list()
    status = build_status(arrival_time)
    cpu_time = 0
    process_turn = 0
    for i in range(len(io_time)):
        process_list.append(i)
        io_finished_at.append(-1)
        complete_time.append(-1)
        response_time.append(-1)
    process_turn = process_list[0]
    while not is_done(status):
        process_turn_o = find_next_process(arrival_time, io_finished_at)
        if process_turn_o == process_turn:
            process_turn_o = process_list[0]
        else:
            process_turn = process_list[0]

        while process_turn_o != process_turn:  # try to find next process to execute
            process_list, process_turn = next_process_RR(process_list)

        # this condition is true when process want to execute 'cpu time 1'
        if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time and arrival_time[process_turn] != -1:
            if burst_time_1[process_turn] <= 5:  # when burst time is lower than time quantum
                temp = cpu_time - arrival_time[process_turn]
                response_time[process_turn] = temp
                cpu_time += burst_time_1[process_turn]
                burst_time_1[process_turn] = 0
                status[process_turn] = 'IO'  # change status to 'IO Operation'
                arrival_time[process_turn] = -1
                io_finished_at[process_turn] = cpu_time + io_time[process_turn]

            else:  # when burst time is greater than time quantum
                temp = cpu_time - arrival_time[process_turn]
                response_time.append(temp)
                cpu_time += 5
                burst_time_1[process_turn] -= 5

        # this condition is true when process want to execute 'cpu time 2'
        elif (status[process_turn] == 'IO' or status[process_turn] == 'CP2') and io_finished_at[
            process_turn] <= cpu_time and io_finished_at[
            process_turn] != -1:
            if burst_time_2[process_turn] <= 5:  # when burst time is lower than time quantum
                cpu_time += burst_time_2[process_turn]
                burst_time_2[process_turn] = 0
                status[process_turn] = 'Done'  # change status to 'Done'
                io_finished_at[process_turn] = -1
                complete_time[process_turn] = cpu_time
            else:  # when burst time is greater than time quantum
                cpu_time += 5
                burst_time_2[process_turn] -= 5
                status[process_turn] = 'CP2'  # change status to 'CP2' to execute remaining burst time
        else:
            cpu_time += 1

    # calculate turn around time and waiting time
    turn_around_time, waiting_time = calculate_tat_wt(arrival_time_o, complete_time, burst_time_1_o, burst_time_2_o,
                                                      io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, cpu_time