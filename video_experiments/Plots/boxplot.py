import matplotlib.pyplot as plt
import matplotlib as mp
import numpy as np
import csv
import pandas as pd
from datetime import datetime
import seaborn as sns

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

def first_three(string):
    result = []
    for i in string:
        if i != '':
            result.append(i)
    return [int(x) for x in result[:3]]



line_num = 0


cat1_240 = [1,2,3,4,5]
cat2_240 = [1,2,3,4,5]
cat3_240 = [1,2,3,4,5]
cat1_1080 = [1,2,3,4,5]
cat2_1080 = [1,2,3,4,5]
cat3_1080 = [1,2,3,4,5]



all_combo = {"cat1_240":cat1_240, "cat2_240":cat2_240, "cat3_240":cat3_240, \
"cat1_1080":cat1_1080, "cat2_1080":cat2_1080, "cat3_1080":cat3_1080}


directories = {"cat1_240":"action/240p", "cat2_240":"documentary/240p", "cat3_240":"sports/240p", "cat1_1080":"action/1080p", "cat2_1080":"documentary/1080p", "cat3_1080":"sports/1080p"}
ending_times = {"cat1_240":[], "cat2_240":[], "cat3_240":[], "cat1_1080":[], "cat2_1080":[], "cat3_1080":[]}

#Map for different category-bitrates
br_map = {"cat1_240":"", "cat2_240":"", "cat3_240":"", "cat1_1080":"", "cat2_1080":"", "cat3_1080":""}
fn = {"240":"3", "1080":"7"}
cat_map = {"cat1":"Action", "cat2":"Documentary", "cat3":"Sports"}
all_fps = {"cat1_240":[], "cat2_240":[], "cat3_240":[], "cat1_1080":[], "cat2_1080":[], "cat3_1080":[]}
all_browser_pss = {"cat1_240":[], "cat2_240":[], "cat3_240":[], "cat1_1080":[], "cat2_1080":[], "cat3_1080":[]}

colors = {"cat1":"lightblue", "cat2":"lightgreen", "cat3":"tan"}

max_fps = 30.0
mp.rcParams.update({'font.size': 18, 'font.sans-serif':'Helvetica'})


dict_out = {"PSS (MB)":[], "Category":[], "Video Resolution":[]}

for x in sorted(all_combo.keys()):
    print(x)
    combo = all_combo[x]
    for n in combo:
        print(n)
        chunk_data = directories[x]+"/Run_"+str(n)+"/nexus5-"+fn[x.split("_")[1]]+".txt"
        frame_df = pd.read_csv(chunk_data)
        frame_df = frame_df[frame_df["Duration(s)"]<=300]
        frame_df['CumulativeDropped'] = 0*frame_df['DroppedFrames'].size
        frame_df['CumulativeTotalFrames'] = 0*frame_df['DroppedFrames'].size
        frame_df['CumulativeDropped'] = frame_df['DroppedFrames'].apply(lambda x: int(x.split('/')[0]))
        frame_df['CumulativeTotalFrames'] = frame_df['DroppedFrames'].apply(lambda x:int(x.split('/')[1]))
        frame_df['dropped'] = frame_df['CumulativeDropped'] - frame_df['CumulativeDropped'].shift(1)
        frame_df['FPS'] = (frame_df['CumulativeTotalFrames'] - frame_df['CumulativeTotalFrames'].shift(1) - frame_df['dropped'])/(frame_df['Duration(s)'] - frame_df['Duration(s)'].shift(1))
        frame_df["Norm_FPS"] = frame_df["FPS"]/max_fps

        fps_norm = np.array(frame_df["Norm_FPS"])
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

        frame_df["Scaled_Norm_FPS"] = fps_norm
        timeline_frame = np.array(frame_df["Timestamp(s)"])
        painted_time = timeline_frame - timeline_frame[0]

        # controlling constants
        memory_data = directories[x]+"/Run_"+str(n)+"/mem_data.txt"
        prev_line = '0.0'

        # initialize arrays to store parsed data
        mem_free = []
        buffers = []
        cached = []
        time_mem = []

        with open(memory_data, 'r') as infile:
            for line in infile:

                line = line.strip()

                # detect /proc/meminfo output
                if line.startswith('MemFree'):
                    mem_free.append(int(line.split(":")[1].strip()[:-3]))
                    #print(int(line.split(":")[1].strip()[:-3]))
                elif line.startswith("Buffers"):
                    buffers.append(float(line.split(":")[1].strip()[:-3]))
                elif line.startswith("Cached"):
                    cached.append(float(line.split(":")[1].strip()[:-3]))
                elif line.startswith('MemTotal'):
                    time_mem.append(float(prev_line))

                # track previous line to get timestamps
                prev_line = line
            time_mem.append(float(prev_line))

        # assertions
        assert len(mem_free) == len(time_mem) - 1

        # convert to numpy arrays
        mem_free = np.array(mem_free)
        time_mem = np.array(time_mem[1:])
        buffers = np.array(buffers)
        cached = np.array(cached)


        ###############################################################
        ##################### CLEAN PSS (MB) DATA #######################
        ###############################################################
        pss_data = directories[x]+"/Run_"+str(n)+"/pss_data.txt"
        pss = []
        time_pss = []
        prev_line = "0.0"
        with open(pss_data,"r") as infile:
            for line in infile:
                line = line.strip()
                if line.startswith('TOTAL:'):
                    line = line[9:].strip().split(" ")
                    pss.append(int(line[0]))


                # track previous line to get timestamps
                elif line.startswith("TOTAL"):
                    time_pss.append(float(prev_line))
                prev_line = line
            time_pss.append(float(prev_line))
                #print(len(pss), len(time_pss))

        pss = np.array(pss)
        time_pss = np.array(time_pss[1:])
        time_frame = timeline_frame[1:]

        time_frame = timeline_frame[1:]
        timeline_mem = (time_mem) - time_frame[0] # in milliseconds
        start_mem = negatives(timeline_mem)
        end_mem = num_bigger(time_mem, time_frame[-1])

        timeline_pss = (time_pss) - time_frame[0] # in milliseconds
        start_pss = negatives(timeline_pss)
        end_pss = num_bigger(time_pss, time_frame[-1])

        all_fps[x] = np.concatenate((all_fps[x], (fps_norm*max_fps)))

        all_browser_pss[x] = np.concatenate((all_browser_pss[x], pss[start_pss:end_pss+1]/1000))
        dict_out["PSS (MB)"] = np.concatenate((dict_out["PSS (MB)"],pss[start_pss:end_pss+1]/1000))
        dict_out["Category"] = np.concatenate((dict_out["Category"], [cat_map[x.split("_")[0]]]*(1+end_pss-start_pss)))
        dict_out["Video Resolution"] = np.concatenate((dict_out["Video Resolution"], [x.split("_")[1]+"p"]*(1+end_pss-start_pss)))
    print("Data Points in ",x, ": ", len(all_browser_pss[x]))
#print(len(dict_out["PSS (MB)"]), len(dict_out["Category"]), len(dict_out["Video Resolution"]))

fig3, ax3 = plt.subplots(figsize=(6.5,5))

data_out = pd.DataFrame(dict_out)

sns.boxplot(x="Video Resolution", y="PSS (MB)", data=data_out, hue="Category", palette = "Set1", whis='range', fliersize=1, width=0.6, ax=ax3)
ax3.legend(prop={'size':17})
fig3.tight_layout()
fig3.savefig("Boxplots_Different_Categories_min_max.png")
plt.show()
