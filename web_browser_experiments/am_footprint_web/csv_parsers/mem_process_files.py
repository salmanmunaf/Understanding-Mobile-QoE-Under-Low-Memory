import os,sys
import pandas as pd

path_to_files = sys.args[1]

total_allocation = {}
browser_process_alloc = {}
gpu_process_alloc = {}
renderer_processes_alloc = {}

web_cache_alloc= {}
blink_gc_alloc={}
cc_alloc= {}
font_size_alloc= {}
gpu_alloc= {}
java_heap_alloc= {}
malloc_alloc= {}
partition_alloc= {}
shared_mem_alloc= {}
v8_alloc= {}
discardable_alloc= {}
skia_alloc= {}
v8_heap = {}

def add_entry_to_rend_dict(webpage_name, value):
    renderer_processes_alloc[webpage_name] = value
    if webpage_name not in web_cache_alloc.keys():
        web_cache_alloc[webpage_name] = 0
    if webpage_name not in blink_gc_alloc.keys():
        blink_gc_alloc[webpage_name] = 0
    if webpage_name not in cc_alloc.keys():
        cc_alloc[webpage_name] = 0
    if webpage_name not in gpu_alloc.keys():
        gpu_alloc[webpage_name] = 0
    if webpage_name not in java_heap_alloc.keys():
        java_heap_alloc[webpage_name] = 0
    if webpage_name not in malloc_alloc.keys():
        malloc_alloc[webpage_name] = 0
    if webpage_name not in partition_alloc.keys():
        partition_alloc[webpage_name] = 0
    if webpage_name not in shared_mem_alloc.keys():
        shared_mem_alloc[webpage_name] = 0
    if webpage_name not in v8_alloc.keys():
        v8_alloc[webpage_name] = 0
    if webpage_name not in discardable_alloc.keys():
        discardable_alloc[webpage_name] = 0
    if webpage_name not in skia_alloc.keys():
        skia_alloc[webpage_name] = 0
    if webpage_name not in skia_alloc.keys():
        v8_heap[webpage_name] = 0


    




def main():
    # files_to_process = map( (lambda x : path_to_files+x), os.listdir(path_to_files))
    # files_to_process.sort()
    # count = 0
    # for csv_file in files_to_process:
    #     print csv_file
    #     data = pd.read_csv(csv_file)
    #     for _,row in data.iterrows():
    #         name_parsed = row["name"].split(":")
    #         #print name_parsed
    #         try: 
    #             if name_parsed[2] == "all_processes":
    #                 if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "effective_size":
    #                     web_page_name = ".".join(row["stories"].split("_"))     
    #                     total_allocation[web_page_name] = int(row["max"])
                    
    #             elif name_parsed[2] == "browser_process":
    #                 if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "effective_size":
    #                     web_page_name = ".".join(row["stories"].split("_"))     
    #                     browser_process_alloc[web_page_name] = int(row["max"])

    #             elif name_parsed[2] == "gpu_process":
    #                 if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "effective_size":
    #                     web_page_name = ".".join(row["stories"].split("_"))     
    #                     gpu_process_alloc[web_page_name] = int(row["max"])
            
    #             elif name_parsed[2] == "renderer_processes":
    #                 if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "effective_size":
    #                     web_page_name = ".".join(row["stories"].split("_"))     
    #                     renderer_processes_alloc[web_page_name] = int(row["max"])
    #         except:
    #             print name_parsed

    #     print total_allocation

    #     ds = [total_allocation,browser_process_alloc, gpu_process_alloc, renderer_processes_alloc]
    #     d = {}
    #     print ds

    #     for k in renderer_processes_alloc.iterkeys():
    #         try:
    #             d[k] = tuple(d[k] for d in ds)
    #         except KeyError:
    #            print "error"
    #     df = pd.DataFrame.from_dict(d, orient='index')
    # # df.to_csv("processes.csv".format(csv_file), sep=',', encoding='utf-8')
    #     df.to_csv("{}_processed.csv".format(csv_file), sep=',', encoding='utf-8')


    files_to_process = map( (lambda x : path_to_files+x), os.listdir(path_to_files))
    files_to_process.sort()
    count = 0
    
    for csv_file in files_to_process:

        print csv_file
        data = pd.read_csv(csv_file)
        for _,row in data.iterrows():
            name_parsed = row["name"].split(":")
            try: 
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        add_entry_to_rend_dict(web_page_name, float(row["max"]) ) 
                        renderer_processes_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "web_cache" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        web_cache_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "blink_gc" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        blink_gc_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "cc" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        cc_alloc[web_page_name] = float(row["max"])

                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "font_caches" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        font_size_alloc[web_page_name] = float(row["max"])

                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "gpu" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        gpu_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "java_heap" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        java_heap_alloc[web_page_name] = float(row["max"])

                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "malloc" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        malloc_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "partition_alloc" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        partition_alloc[web_page_name] = float(row["max"])

                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "shared_memory" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        shared_mem_alloc[web_page_name] = float(row["max"])

                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "v8" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        v8_alloc[web_page_name] = float(row["max"])
                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "discardable" and name_parsed[5] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        discardable_alloc[web_page_name] = float(row["max"])

                
                if name_parsed[2] == "renderer_processes":
                    if name_parsed[3] == "reported_by_chrome" and name_parsed[4] == "v8" and name_parsed[5] == "heap" and name_parsed[6] == "effective_size":
                        web_page_name = ".".join(row["stories"].split("_"))
                        v8_heap[web_page_name] = float(row["max"])

                
                
            except IndexError:
                print name_parsed

        ds = [renderer_processes_alloc, web_cache_alloc, blink_gc_alloc, cc_alloc,font_size_alloc,gpu_alloc, java_heap_alloc, malloc_alloc, partition_alloc, shared_mem_alloc,v8_alloc,discardable_alloc, skia_alloc,v8_heap]
        d = {}
        
        print renderer_processes_alloc
        for k in renderer_processes_alloc.iterkeys():
            try:
                d[k] = tuple(d[k] for d in ds)
                print d[k]
            except KeyError:
                print "error"
        print(d)
        df = pd.DataFrame.from_dict(d, orient='index')
        df.to_csv("{}_processed.csv".format(csv_file), sep=',', encoding='utf-8')   
# main()

# cpuTimeToFirstMeaningfulPaint = {}
# timeToFirstContentfulPaint= {}
# timeToFirstContentfulPaint_blocked_on_network={}
# timeToFirstContentfulPaint_composite= {}
# timeToFirstContentfulPaint_gc= {}
# timeToFirstContentfulPaint_idle= {}
# timeToFirstContentfulPaint_iframe_creation= {}
# timeToFirstContentfulPaint_imageDecode= {}
# timeToFirstContentfulPaint_input= {}
# timeToFirstContentfulPaint_layout= {}
# timeToFirstContentfulPaint_net= {}
# timeToFirstContentfulPaint_other= {}
# timeToFirstContentfulPaint_overhead= {}
# timeToFirstContentfulPaint_parseHTML= {}
# timeToFirstContentfulPaint_raster= {}
# timeToFirstContentfulPaint_record= {}
# timeToFirstContentfulPaint_renderer_misc= {}
# timeToFirstContentfulPaint_resource_loading= {}
# timeToFirstContentfulPaint_script_execute= {}
# timeToFirstContentfulPaint_script_parse_and_compile= {}
# timeToFirstContentfulPaint_startup= {}
# timeToFirstContentfulPaint_style= {}
# timeToFirstContentfulPaint_v8_runtime= {}
# timeToFirstCpuIdle={}
# timeToFirstMeaningfulPaint={}
# timeToFirstPaint={}
# timeToInteractive={}
# timeToOnload={}




# def main():
#     files_to_process = map( (lambda x : path_to_files+x), os.listdir(path_to_files))
#     files_to_process.sort()
#     count = 0
#     for csv_file in files_to_process:
#         print csv_file
#         data = pd.read_csv(csv_file)
#         for _,row in data.iterrows():
#             try:
#                 #print row['name'], ".".join(row["stories"].split("_")), int(row["avg"])
#                 web_page_name = ".".join(row["stories"].split("_"))
#                 if row['name'] == "cpuTimeToFirstMeaningfulPaint":
#                     cpuTimeToFirstMeaningfulPaint[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint":
#                     timeToFirstContentfulPaint[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:blocked_on_network":
#                     timeToFirstContentfulPaint_blocked_on_network[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:composite":
#                     timeToFirstContentfulPaint_composite[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:gc":
#                     timeToFirstContentfulPaint_gc[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:idle":
#                     timeToFirstContentfulPaint_idle[web_page_name] = float(row["max"])

#                 if row['name'] == "timeToFirstContentfulPaint:iframe_creation":
#                     timeToFirstContentfulPaint_iframe_creation[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:imageDecode":
#                     timeToFirstContentfulPaint_imageDecode[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:input":
#                     timeToFirstContentfulPaint_input[web_page_name] = float(row["max"])

#                 if row['name'] == "timeToFirstContentfulPaint:layout":
#                     timeToFirstContentfulPaint_layout[web_page_name] = float(row["max"])
        
#                 if row['name'] == "timeToFirstContentfulPaint:net":
#                     timeToFirstContentfulPaint_net[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:other":
#                     timeToFirstContentfulPaint_other[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:overhead":
#                     timeToFirstContentfulPaint_overhead[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:parseHTML":
#                     timeToFirstContentfulPaint_parseHTML[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:raster":
#                     timeToFirstContentfulPaint_raster[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:record":
#                     timeToFirstContentfulPaint_record[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:record":
#                     timeToFirstContentfulPaint_record[web_page_name] = float(row["max"])    

#                 if row['name'] == "timeToFirstContentfulPaint:renderer_misc":
#                     timeToFirstContentfulPaint_renderer_misc[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:resource_loading":
#                     timeToFirstContentfulPaint_resource_loading[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:script_execute":
#                     timeToFirstContentfulPaint_script_execute[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:script_parse_and_compile":
#                     timeToFirstContentfulPaint_script_parse_and_compile[web_page_name] = float(row["max"]) 
                
#                 if row['name'] == "timeToFirstContentfulPaint:startup":
#                     timeToFirstContentfulPaint_startup[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:style":
#                     timeToFirstContentfulPaint_style[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstContentfulPaint:v8_runtime":
#                     timeToFirstContentfulPaint_v8_runtime[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstCpuIdle":
#                     timeToFirstCpuIdle[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToFirstMeaningfulPaint":
#                     timeToFirstMeaningfulPaint[web_page_name] = float(row["max"])

#                 if row['name'] == "timeToFirstPaint":
#                     timeToFirstPaint[web_page_name] = float(row["max"])
                
#                 if row['name'] == "timeToInteractive":
#                     timeToInteractive[web_page_name] = float(row["max"])

#                 if row['name'] == "timeToOnload":
#                     timeToOnload[web_page_name] = float(row["max"])



#             except:
#                 a = 1
#                 #print "skipping row" 
#         ds = [  cpuTimeToFirstMeaningfulPaint, 
#                 timeToFirstContentfulPaint,
#                 timeToFirstContentfulPaint_blocked_on_network,
#                 timeToFirstContentfulPaint_composite,
#                 timeToFirstContentfulPaint_gc,
#                 timeToFirstContentfulPaint_idle,
#                 timeToFirstContentfulPaint_iframe_creation,
#                 timeToFirstContentfulPaint_imageDecode,
#                 timeToFirstContentfulPaint_input,
#                 timeToFirstContentfulPaint_layout,
#                 timeToFirstContentfulPaint_net,
#                 timeToFirstContentfulPaint_other,
#                 timeToFirstContentfulPaint_overhead,
#                 timeToFirstContentfulPaint_parseHTML,
#                 timeToFirstContentfulPaint_raster,
#                 timeToFirstContentfulPaint_record,
#                 timeToFirstContentfulPaint_renderer_misc,
#                 timeToFirstContentfulPaint_resource_loading,
#                 timeToFirstContentfulPaint_script_execute,
#                 timeToFirstContentfulPaint_script_parse_and_compile,
#                 timeToFirstContentfulPaint_startup,
#                 timeToFirstContentfulPaint_style,
#                 timeToFirstContentfulPaint_v8_runtime,
#                 timeToFirstCpuIdle,
#                 timeToFirstMeaningfulPaint,
#                 timeToFirstPaint,
#                 timeToInteractive,
#                 timeToOnload
#         ]
        
#         d = {}
        
#         for k in timeToFirstCpuIdle.iterkeys():
#             try:
#                 d[k] = tuple(d[k] for d in ds)
#             except KeyError:
#                 print "error"
#         df = pd.DataFrame.from_dict(d, orient='index')
#         df.to_csv("{}_processed.csv".format(csv_file), sep=',', encoding='utf-8')

main()