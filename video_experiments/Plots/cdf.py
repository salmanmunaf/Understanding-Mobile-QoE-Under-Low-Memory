import matplotlib.pyplot as plt
import matplotlib as mp
import numpy as np
import csv

###############################################################
####################### CLEAN CPU DATA ########################
###############################################################

# controlling constants
cpu_data = 'cpu_data.txt'
scale_processes = True

# initialize arrays to store parsed data
jiffies_us = []
jiffies_sy = []
jiffies_id = []
jiffies_io = []
jiffies_other = []
intr = []
ctx = []
browser = []
media = []
surface = []
media_server = []
time_cpu = [] # in seconds
procs_num = []

with open(cpu_data, 'r') as infile:
    for line in infile:

        # get cumulative number of jiffies spent in all cores
        if line.startswith('cpu  '):
            jiff = 0
            edited_line = line[5:].strip().split(' ')
            jiffies_us.append(int(edited_line[0]) + int(edited_line[1]))
            jiffies_sy.append(int(edited_line[2]))
            jiffies_id.append(int(edited_line[3]))
            jiffies_io.append(int(edited_line[4]))
            jiffies_other.append(int(edited_line[5]) + int(edited_line[6]))

        # get cumulative number of interrupts
        elif line.startswith('intr '):
            intr.append(int(line[5:].strip().split(' ')[0]))

        # get cumulative number of context switches
        elif line.startswith('ctxt '):
            ctx.append(int(line[5:].strip()))

        # get number of processes running
        elif line.startswith('procs_running '):
            procs_num.append(int(line.strip()[14:]))

        else:
            edited_line = line.strip().split(' ')

            if len(edited_line) > 1:

                # get cumulative number of jiffies spent running firefox:media
                if edited_line[1].find('firefox:media') >= 0:
                    media.append(int(edited_line[13]) + int(edited_line[14]))

                # get cumulative number of jiffies spent running firefox
                elif edited_line[1].find('firefox') >= 0:
                    browser.append(int(edited_line[13]) + int(edited_line[14]))

                # get cumulative number of jiffies spent running surfaceflinger
                elif edited_line[1].find('surface') >= 0:
                    surface.append(int(edited_line[13]) + int(edited_line[14]))

                # get cumulative number of jiffies spent running mediaserver
                elif edited_line[1].find('mediaserver') >= 0:
                    media_server.append(int(edited_line[13]) + int(edited_line[14]))

            elif len(edited_line[0]) >= 10 :
                #get timestamps in seconds
                time_cpu.append(float(edited_line[0]))

# assertions
assert len(jiffies_us) == len(jiffies_sy) == len(jiffies_id) == len(jiffies_io) == len(jiffies_other) == len(intr) == len(ctx)
assert len(browser) == len(media) == len(surface) == len(media_server) == len(time_cpu)

# convert to numpy arrays
jiffies_us = np.array(jiffies_us)
jiffies_sy = np.array(jiffies_sy)
jiffies_id = np.array(jiffies_id)
jiffies_io = np.array(jiffies_io)
jiffies_other = np.array(jiffies_other)
jiffies_total = jiffies_us + jiffies_sy + jiffies_id + jiffies_io + jiffies_other
intr = np.array(intr)
ctx = np.array(ctx)
browser = np.array(browser)
media = np.array(media)
surface = np.array(surface)
media_server = np.array(media_server)
time_cpu = np.array(time_cpu) # in seconds
procs_num = np.array(procs_num)

# calculate cpu stats
jiffies_total_diff = np.diff(jiffies_total)
cpu_us = np.diff(jiffies_us) / jiffies_total_diff.astype(float) # time spent in user space
cpu_sy = np.diff(jiffies_sy) / jiffies_total_diff.astype(float) # time spent in kernel space
cpu_id = np.diff(jiffies_id) / jiffies_total_diff.astype(float) # time spent idle
cpu_io = np.diff(jiffies_io) / jiffies_total_diff.astype(float) # time spent in io wait
cpu_other = np.diff(jiffies_other) / jiffies_total_diff.astype(float) # time spent in other tasks (irq, softirq)
cpu_good = cpu_us + cpu_sy

# calculate interrupts and context switches
intr_diff = np.diff(intr)
ctx_diff = np.diff(ctx)

# calculate share of processes on cpu
browser_cpu = np.diff(browser) / jiffies_total_diff.astype(float) # browser
media_cpu = np.diff(media) / jiffies_total_diff.astype(float) # media
surface_cpu = np.diff(surface) / jiffies_total_diff.astype(float) # surface
media_server_cpu = np.diff(media_server) / jiffies_total_diff.astype(float) # mediaserver

# scale cpu utilization figures if they add up to greater than one
# this can happen since snapshots of jiffies is taken sequentially
if scale_processes:
    scale = np.maximum(np.array([1.0] * len(browser_cpu)), browser_cpu + media_cpu + surface_cpu + media_server_cpu)
    browser_cpu = browser_cpu / scale # scale browser
    media_cpu = media_cpu / scale # scale media
    surface_cpu = surface_cpu / scale # scale surface
    media_server_cpu = media_server_cpu / scale # scale mediaserver

# cumulative of all the tracked processes
cumulative_processes = browser_cpu + media_cpu + surface_cpu + media_server_cpu

###############################################################
################## CLEAN CHUNK & FRAME DATA ###################
###############################################################

# controlling constants
chunk_data = 'chunk_data.txt'

# initialize arrays to store parsed data
parsed_data = [[], [], [], [], [], [], []]
bitrate = []
device_time = []
rebuffer = []
decoded = []
presented = []
painted = []
video = [] # in seconds
decoded_time = [] # in milliseconds
presented_time = [] # in milliseconds
painted_time = [] # in milliseconds
bitrates_run = []
device_times_run = [] # in milliseconds
rebuffers_run = []
line_num = 0

# helper function
def num_from_right(string):
    num = 0
    for i in range(len(string)-1,-1,-1):
        if string[i] in '. 0123456789':
            num += 1
        else:
            break
    return num

# helper function
def num_from_left(string):
    num = 0
    for i in string:
        if i in '. 0123456789':
            num += 1
        else:
            break
    return num

# helper function
def negatives(seq):
    count = 0
    for i in seq:
        if i < 0:
            count += 1
        else:
            break
    return count

# helper function
def num_bigger(seq, num):
    index = -1
    for i in seq:
        if i <= num:
            index += 1
        else:
            break
    return index

with open(chunk_data, 'r') as infile:
    
    for line in infile:

        line_num += 1

        # last line is empty
        if line.strip() == '':
            break

        # frame data
        elif line_num % 50 == 0:

            parsed_data = [[], [], [], [], [], [], []]
            bitrates_run.append(np.array(bitrate))
            bitrate = []
            device_times_run.append(np.array(device_time))
            device_time = []
            rebuffers_run.append(np.array(rebuffer))
            rebuffer = []
            
            edited_line = line.split(',')
            size = len(edited_line) / 7

            for i in range(7):
                section = edited_line[i*size:(i+1)*size]

                # get data type number
                if section[0].find('decodedSeries') >= 0:
                    index = 0
                elif section[0].find('presentedSeries') >= 0:
                    index = 1
                elif section[0].find('fpsSeries') >= 0:
                    index = 2
                elif section[0].find('videoSeries') >= 0:
                    index = 3
                elif section[0].find('decodedTime') >= 0:
                    index = 4
                elif section[0].find('presentedTime') >= 0:
                    index = 5
                elif section[0].find('fpsTime') >= 0:
                    index = 6

                # store first entry
                if index == 3: # video
                    parsed_data[index].append(float(section[0][-num_from_right(section[0]):]))
                else:
                    parsed_data[index].append(int(section[0][-num_from_right(section[0]):]))

                # store second to second-last entry
                if index == 3:
                    for i in section[1:-1]:
                        parsed_data[index].append(float(i))
                else:
                    for i in section[1:-1]:
                        parsed_data[index].append(int(i))

                # store last entry
                if index == 3:
                    parsed_data[index].append(float(section[-1][:num_from_left(section[-1])]))
                else:
                    parsed_data[index].append(int(section[-1][:num_from_left(section[-1])]))

            # convert parsed data to numpy arrays
            decoded.append(np.array(parsed_data[0]))
            presented.append(np.array(parsed_data[1]))
            painted.append(np.array(parsed_data[2]))
            video.append(np.array(parsed_data[3]))
            decoded_time.append(np.array(parsed_data[4]))
            presented_time.append(np.array(parsed_data[5]))
            painted_time.append(np.array(parsed_data[6]))

        # chunk data
        else:
            edited_line = line.split("'")
            bitrate_index = edited_line.index('lastquality') + 1
            bitrate.append(int(edited_line[bitrate_index].split(",")[0].split(":")[1]))
            device_time_index = edited_line.index('deviceTime') + 1
            device_time.append(int(edited_line[device_time_index].split(",")[0].split(":")[1]))
            rebuffer_index = edited_line.index('RebufferTime') + 1
            rebuffer.append(int(edited_line[rebuffer_index].split(",")[0].split(":")[1]))


# assertions
for i in range(len(decoded)):
    #print [len(decoded[i]), len(presented[i]), len(painted[i]), len(video[i]), len(decoded_time[i]), len(presented_time[i]), len(painted_time[i])]
    assert len(decoded[i]) == len(presented[i]) == len(painted[i]) == len(video[i]) == len(decoded_time[i]) == len(presented_time[i]) == len(painted_time[i])

for i in bitrates_run:
    assert len(i) == 49

assert len(bitrates_run) == len(decoded)

# calculate stats for each run
# runs
runs = len(decoded)

# timelines
time_frames = painted_time
timeline_frames = [] # in milliseconds
for i in painted_time:
    timeline_frames.append(i[1:] - i[0])

# fps
fps_run = []
for i in range(len(painted)):
    fps_norm = (np.diff(painted[i]).astype(float) / np.diff(time_frames[i])) * 1000 / 25.0
    # smoothening
    for i in range(1,len(fps_norm)):
        if fps_norm[i] > 1.0 and fps_norm[i-1] < 1.0:
            excess = fps_norm[i] - 1.0
            space = 1.0 - fps_norm[i-1]
            if space >= excess:
                fps_norm[i-1] += excess
                fps_norm[i] -= excess
            else:
                fps_norm[i-1] += space
                fps_norm[i] -= space
    # capping at 1
    scale_fps = np.maximum(np.array([1.0] * len(fps_norm)), fps_norm)
    fps_norm = fps_norm / scale_fps
    fps_run.append(fps_norm)

# normalized bitrate
for i in range(len(bitrates_run)):
    bitrates_run[i] = bitrates_run[i] / 5.0

###############################################################
##################### CLEAN MEMORY DATA #######################
###############################################################

# controlling constants
memory_data = 'mem_data.txt'
prev_line = '0.0'

# initialize arrays to store parsed data
mem_free = []
time_mem = []

def first_three(string):
    result = []
    for i in string:
        if i != '':
            result.append(i)
    return [int(x) for x in result[:3]]

with open(memory_data, 'r') as infile:
    for line in infile:

        line = line.strip()

        # detect /proc/meminfo output
        if line.startswith('MemFree'):
            mem_free.append(int(line.strip()[8:23]))

        elif line.startswith('MemTotal'):
            time_mem.append(float(prev_line))

        # track previous line to get timestamps
        prev_line = line

# assertions
assert len(mem_free) == len(time_mem) - 1

# convert to numpy arrays
mem_free = np.array(mem_free)
time_mem = np.array(time_mem[1:])

###############################################################
###################### ANALYSIS & PLOTS #######################
###############################################################

relevant_fps_run = []
cumulative_drops = []

for i in range(runs):

    time_frame = time_frames[i]
    timeline_frame = timeline_frames[i]
    bitrate = bitrates_run[i]
    fps = fps_run[i]
    video_time = video[i]

    # chunk timeline
    chunk_bitrate = np.array([bitrate[int(x/4)] for x in video_time]) # in milliseconds

    # get timeline for cpu data with frame timestamp start as reference point
    timeline_cpu = (time_cpu * 1000) - time_frame[0] # in milliseconds
    start_cpu = negatives(timeline_cpu)
    end_cpu = num_bigger(time_cpu * 1000, time_frame[-1])

    # get timeline for memory data with frame timestamp start as reference point
    timeline_mem = (time_mem * 1000) - time_frame[0] # in milliseconds
    start_mem = negatives(timeline_mem)
    end_mem = num_bigger(time_mem * 1000, time_frame[-1])

    # get relevant fps distribution - removing impact of rebuffering on fps
    rebuffer_series = rebuffers_run[i]
    device_time_series = device_times_run[i]
    no_rebuffer_times = []
        # get intervals between chunk downloads where no rebuffering occurred 
    for j in range(1,len(rebuffer_series)):
        if rebuffer_series[j] == rebuffer_series[j-1]:
            no_rebuffer_times.append((device_time_series[j-1],device_time_series[j]))
    relevant_timeline_indices = []
        # get timestamp indices for frame data which fall in no rebuffering intervals
    for k in range(len(time_frame)):
        for l in no_rebuffer_times:
            if l[0] <= time_frame[k] and l[1] >= time_frame[k]:
                relevant_timeline_indices.append(k)
                break
        # all timestamp indices after last chunk is downloaded
    end_point_chunk = device_time_series[-1]
    for k in range(len(time_frame)):
        if time_frame[k] > end_point_chunk:
            relevant_timeline_indices.append(k)
        # get the relevant fps numbers
    relevant_fps = []
    for k in range(1, len(relevant_timeline_indices)):
        if relevant_timeline_indices[k-1] + 1 == relevant_timeline_indices[k]:
            relevant_fps.append(fps[k-1])
    relevant_fps_run.append(relevant_fps)

    # calculate cumulative drops
    cumulative_drops.append((int(((painted_time[i][-1] - painted_time[i][0]) * 25.0 / 1000.0)), painted[i][-1] - painted[i][0], presented[i][-1] - presented[i][0], decoded[i][-1] - decoded[i][0]))

    # set font size
    mp.rcParams.update({'font.size': 28})

    # useful plots
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    #line1 = ax1.fill_between((video_time - video_time[0]) * 1000, chunk_bitrate, 0, label='Bitrate'dd, color='lightblue')
    line1 = ax1.bar((video_time - video_time[0]), chunk_bitrate, align='edge',edgecolor='lightblue',width=1.5, label='Bitrate', color='lightblue')
    line2 = ax1.plot(timeline_frame/1000, fps, label='FPS', color='red')
    #line3 = ax1.plot(timeline_cpu[start_cpu:end_cpu+1], cumulative_processes[start_cpu:end_cpu+1], label=' Browser + Video Processes')
    line4 = ax2.plot(timeline_cpu[start_cpu:end_cpu+1]/1000, cpu_good[start_cpu:end_cpu+1]*100, label='CPU Utilization')
    #line7 = ax2.plot(timeline_mem[start_mem:end_mem+1], mem_free[start_mem:end_mem+1], label='Free Memory', color='red')
    ax1.set_ylim(0, 1.1)
    ax1.set_ylabel('Normalized FPS', fontsize=28)	
    #ax2.set_ylim(0, 16000)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel('CPU Utilization (%)', fontsize=28)	
    #ax2.tick_params('y', colors='red')
    fig.tight_layout()
    #ax1.legend()
    #ax2.legend(loc='upper right')
    ax1.legend(loc='upper center', bbox_to_anchor=(0.3, 1.05),
          ncol=3, fancybox=True, shadow=True, prop={'size': 28})
    ax2.legend(loc='upper center', bbox_to_anchor=(0.8, 1.05),
          ncol=3, fancybox=True, shadow=True, prop={'size': 28})
    ax1.set_xlabel('Time Elapsed (s)', fontsize=28)
    ax1.set_xlim(0,200)
    plt.show()


    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    line1 = ax1.bar((video_time - video_time[0]), chunk_bitrate, align='edge',edgecolor='lightblue',width=1.5, label='Bitrate', color='lightblue')
    line2 = ax1.plot(timeline_frame/1000, fps, label='FPS', color='red')
    line7 = ax2.plot(timeline_mem[start_mem:end_mem+1]/1000, mem_free[start_mem:end_mem+1], label='Free Memory', color='blue')
    ax1.set_ylim(0, 1.15)
    ax1.set_ylabel('Normalized FPS', fontsize=28)	
    ax2.set_ylim(0, 25000)
    ax2.set_ylabel('Amount of Free Memory (KB)', fontsize=28)	
    fig.tight_layout()
    ax1.legend(loc='upper center', bbox_to_anchor=(0.3, 1.05),
          ncol=3, fancybox=True, shadow=True, prop={'size': 28})
    ax2.legend(loc='upper center', bbox_to_anchor=(0.8, 1.05),
          ncol=3, fancybox=True, shadow=True, prop={'size': 28})
    ax1.set_xlabel('Time Elapsed (s)', fontsize=28)
    ax1.set_xlim(0,200)
    plt.show()


    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    line1 = ax1.bar((video_time - video_time[0]), chunk_bitrate, align='edge', edgecolor='lightblue', width=1.5, label='Bitrate', color='lightblue')
    line2 = ax1.plot(timeline_frame/1000, fps, label='FPS',color='red')
    line3 = ax2.plot(timeline_cpu[start_cpu:end_cpu+1]/1000, browser_cpu[start_cpu:end_cpu+1]*100, label='Browser', color='green')
    line4 = ax2.plot(timeline_cpu[start_cpu:end_cpu+1]/1000, media_cpu[start_cpu:end_cpu+1]*100, label='ABR controller', color='brown')
    line5 = ax2.plot(timeline_cpu[start_cpu:end_cpu+1]/1000, surface_cpu[start_cpu:end_cpu+1]*100, label='Renderer', color='blue')
    line6 = ax2.plot(timeline_cpu[start_cpu:end_cpu+1]/1000, media_server_cpu[start_cpu:end_cpu+1]*100, label='Decoder', color='magenta')
    ax1.set_ylim(0.0, 1.15)
    ax1.set_ylabel('Normalized FPS', fontsize=28) 
    ax2.set_ylim(0, 115)
    ax2.set_ylabel('CPU Utilization (%)', fontsize=28)
    fig.tight_layout()
    ax1.legend(loc='upper center', bbox_to_anchor=(0.15, 1.09),
          ncol=1, fancybox=True, shadow=True, prop={'size': 26})
    ax2.legend(loc='upper center', bbox_to_anchor=(0.65, 1.09),
          ncol=2, fancybox=True, shadow=True, prop={'size': 26})
    ax1.set_xlabel('Time Elapsed (s)', fontsize=28)
    ax1.set_xlim(0,200) 
    plt.show()

    plt.bar((video_time - video_time[0]) * 1000, chunk_bitrate, align='edge', width=1500, label='Bitrate', color='lightblue')
    plt.plot(timeline_frame, fps, label='fps')
    plt.plot(timeline_cpu[start_cpu:end_cpu+1], (intr_diff / float(max(intr_diff)))[start_cpu:end_cpu+1], label='interrupts')
    plt.plot(timeline_cpu[start_cpu:end_cpu+1], (ctx_diff / float(max(ctx_diff)))[start_cpu:end_cpu+1], label='context switches')
    plt.ylim(0.0, 1.2)
    plt.legend()
    plt.show()


###############################################################
##################### RESULTS FOR PAPER #######################
###############################################################

# output fps distribution where no rebuffering took place
fps_together = []
for i in relevant_fps_run:
    fps_together += i
with open('fps_distribution.txt', 'wb') as outfile:
    wr = csv.writer(outfile)
    wr.writerow(fps_together)

# print cumulative drops in painted frames
print '(total frames to be shown under no losses, frames painted, frames presented to the rendering pipeline, frames decoded) ',
print cumulative_drops

### output the relevant data
##with open('relevant_data.txt', 'wb') as outfile:
##    wr = csv.writer(outfile)
##    wr.writerow(['>>> Bitrate timeline'])
##    wr.writerow((video_time - video_time[0]) * 1000)
##    wr.writerow(['... Bitrate'])
##    wr.writerow(chunk_bitrate)
##    wr.writerow(['-------------------------------------------------------------------------------------'])
##    wr.writerow(['>>> FPS timeline'])
##    wr.writerow(timeline_frame)
##    wr.writerow(['... Normalized FPS'])
##    wr.writerow(fps)
##    wr.writerow(['-------------------------------------------------------------------------------------'])
##    wr.writerow(['>>> CPU timeline'])
##    wr.writerow(timeline_cpu[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - our processes - Browser + Controller + Renderer + Decoder'])
##    wr.writerow(cumulative_processes[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - total'])
##    wr.writerow(cpu_good[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - browser'])
##    wr.writerow(browser_cpu[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - controller'])
##    wr.writerow(media_cpu[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - renderer'])
##    wr.writerow(surface_cpu[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU utilization - decoder'])
##    wr.writerow(media_server_cpu[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU interrupts'])
##    wr.writerow(intr_diff[start_cpu:end_cpu+1])
##    wr.writerow(['... CPU context switches'])
##    wr.writerow(ctx_diff[start_cpu:end_cpu+1])
##    wr.writerow(['-------------------------------------------------------------------------------------'])
##    wr.writerow(['>> Memory timeline'])
##    wr.writerow(timeline_mem[start_mem:end_mem+1])
##    wr.writerow(['... Free memory'])
##    wr.writerow(mem_free[start_mem:end_mem+1])
    
