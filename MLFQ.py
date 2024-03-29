from FCFS import find_next_process
from RoundRobin import next_process_RR
from SharedMethod import build_status, is_done, calculate_tat_wt


def MLFQ(arrival_time_o, burst_time_1_o, io_time, burst_time_2_o):
    burst_time_1 = burst_time_1_o.copy()
    burst_time_2 = burst_time_2_o.copy()
    arrival_time = arrival_time_o.copy()
    io_finished_at = list()
    complete_time = list()
    response_time = list()
    process_list_level_1 = list()
    process_list_level_2 = list()
    process_list_level_3 = list()
    status = build_status(arrival_time)
    cpu_time = 0
    counter = 0
    for i in range(len(io_time)):
        io_finished_at.append(-1)
        complete_time.append(-1)
        response_time.append(-1)
        process_list_level_1.append(i)  # at first all processes are in level 1 queue

    process_turn = process_list_level_1[0]

    while not is_done(status):
        if len(process_list_level_1) > 0:  # if there is a process in level 1 this block execute
            # block 1 in this multi level feedback queue is Rand Robin with time quantum 4
            process_turn_o = find_next_process(arrival_time, io_finished_at)
            flag_1 = False
            if process_turn_o == process_turn:
                process_turn_o = process_list_level_1[0]
            else:
                process_turn = process_list_level_1[0]

            while process_turn_o != process_turn:  # try to find next process to execute
                process_list_level_1, process_turn = next_process_RR(process_list_level_1)
                flag_1 = True

            # this condition is true when process want to execute 'cpu time 1'
            if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time and arrival_time[
                process_turn] != -1:
                if burst_time_1[process_turn] <= 4:  # when burst time is lower than time quantum
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
                    cpu_time += 4
                    burst_time_1[process_turn] -= 4
                    if not flag_1:
                        a = process_list_level_1.pop(0)
                    else:
                        a = process_list_level_1.pop(-1)
                    process_list_level_2.append(a)

            # this condition is true when process want to execute 'cpu time 2'
            elif (status[process_turn] == 'IO' or status[process_turn] == 'CP2') and io_finished_at[
                process_turn] <= cpu_time and io_finished_at[
                process_turn] != -1:
                if burst_time_2[process_turn] <= 4:  # when burst time is lower than time quantum
                    cpu_time += burst_time_2[process_turn]
                    burst_time_2[process_turn] = 0
                    status[process_turn] = 'Done'  # change status to 'Done'
                    io_finished_at[process_turn] = -1
                    process_list_level_1.pop(-1)
                    complete_time[process_turn] = cpu_time
                else:  # when burst time is greater than time quantum
                    cpu_time += 4
                    burst_time_2[process_turn] -= 4
                    status[process_turn] = 'CP2'  # change status to 'CP2' to execute remaining burst time
                    if not flag_1:
                        a = process_list_level_1.pop(0)
                    else:
                        a = process_list_level_1.pop(-1)
                    process_list_level_2.append(a)
            else:
                cpu_time += 1

        elif len(process_list_level_2) > 0:  # if there is a process in level 2 this block execute
            # block 2 in this multi level feedback queue is Rand Robin with time quantum 16
            flag_2 = False
            if counter == 0:
                process_turn = process_list_level_2[0]
                counter += 1
            process_turn_o = find_next_process(arrival_time, io_finished_at)
            if process_turn_o == process_turn:
                process_turn_o = process_list_level_2[0]
            else:
                process_turn = process_list_level_2[0]

            while process_turn_o != process_turn:  # try to find next process to execute
                flag_2 = True
                process_list_level_2, process_turn = next_process_RR(process_list_level_2)

            # this condition is true when process want to execute 'cpu time 1'
            if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time and arrival_time[
                process_turn] != -1:
                if burst_time_1[process_turn] <= 16:  # when burst time is lower than time quantum
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
                    cpu_time += 16
                    burst_time_1[process_turn] -= 16
                    if not flag_2:
                        a = process_list_level_2.pop(0)
                    else:
                        a = process_list_level_2.pop(-1)

                    process_list_level_3.append(a)

            # this condition is true when process want to execute 'cpu time 2'
            elif (status[process_turn] == 'IO' or status[process_turn] == 'CP2') and io_finished_at[
                process_turn] <= cpu_time and io_finished_at[
                process_turn] != -1:
                if burst_time_2[process_turn] <= 16:  # when burst time is lower than time quantum
                    cpu_time += burst_time_2[process_turn]
                    burst_time_2[process_turn] = 0
                    status[process_turn] = 'Done'  # change status to 'Done'
                    io_finished_at[process_turn] = -1
                    complete_time[process_turn] = cpu_time
                    process_list_level_2.pop(-1)
                else:  # when burst time is greater than time quantum
                    cpu_time += 16
                    burst_time_2[process_turn] -= 16
                    status[process_turn] = 'CP2'  # change status to 'CP2' to execute remaining burst time
                    if not flag_2:
                        a = process_list_level_2.pop(0)
                    else:
                        a = process_list_level_2.pop(-1)
                    process_list_level_3.append(a)
            else:
                cpu_time += 1

        elif len(process_list_level_3) > 0:  # if there is a process in level 3 this block execute
            # block 3 in this multi level feedback queue is First Come First Serve

            process_turn = find_next_process(arrival_time, io_finished_at)  # find the next process that should execute

            # this condition is true when process want to execute 'cpu time 1'
            if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time:
                temp = cpu_time - arrival_time[process_turn]
                response_time[process_turn] = temp
                cpu_time += burst_time_1[process_turn]
                status[process_turn] = 'IO'  # change status to 'IO Operation'
                arrival_time[process_turn] = -1
                io_finished_at[process_turn] = cpu_time + io_time[process_turn]

            # this condition is true when process want to execute 'cpu time 2'
            elif status[process_turn] == 'IO' and io_finished_at[process_turn] <= cpu_time:
                cpu_time += burst_time_2[process_turn]
                status[process_turn] = 'Done'  # change status to 'Done'
                io_finished_at[process_turn] = -1
                complete_time[process_turn] = cpu_time
                process_list_level_3.pop(-1)
            else:

                cpu_time += 1

    # find turn around time and waiting time with 'calculate_tat_wt' function
    turn_around_time, waiting_time = calculate_tat_wt(arrival_time_o, complete_time, burst_time_1_o, burst_time_2_o,
                                                      io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, cpu_time