# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:07:46 2022

@author: Ahmed EL-brawany
"""


data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}
       },
def FCFS (tracks):
    tracks2 = tracks.copy()
    for track in tracks2:
        try:
            if track > 50 or track < 1 :
                tracks.remove(track)
            elif tracks.count(track)>1:
                indices = [i for i, x in enumerate(tracks) if x == track]
                indices.pop(0)
                for i in indices:
                    tracks.pop(i)
                    
        except:
            pass
          
    headers = ["head path", "tracks traveled"]
    table = {}
    total  = 0
    for track in range(len(tracks)-1):
        tracksTraveled = abs(tracks[track+1]-tracks[track])
        total += tracksTraveled
        table[f"{track}"] = {"Head Path": f"{tracks[track]} to {tracks[track+1]}", "Tracks Traveled": tracksTraveled}
    
    
    table["70"] = {"Head Path": "total no.T", "Tracks Traveled": f"{total}ms"}
    table["100"] = {"Head Path": "avg no.Tt", "Tracks Traveled": f"{round(total/(len(table)-1),2)}"}
    
    return (table, tracks)

def SSTF(tracks):
    tracks2 = tracks.copy()
    for track in tracks2:
        try:
            if track > 50 or track < 1 :
                tracks.remove(track)
            elif tracks.count(track)>1:
                indices = [i for i, x in enumerate(tracks) if x == track]
                indices.pop(0)
                for i in indices:
                    tracks.pop(i)
                    
        except:
            pass
            
    tracks2 = tracks.copy()  
    tracks2.sort()
    headers = ["head path", "tracks traveled"]
    table = {}
    total  = 0
    start_index = tracks2.index(tracks[0])
    tracksOrder = [tracks[0]]
    for track in range(len(tracks)-1):
        if start_index != 0 and (start_index == len(tracks2)-1 or tracks2[start_index+1]-tracks2[start_index] > tracks2[start_index]-tracks2[start_index-1]):
             tracksTraveled = tracks2[start_index]-tracks2[start_index-1]
             total += tracksTraveled
             table[f"{track}"] = {"Head Path": f"{tracks2[start_index]} to {tracks2[start_index-1]}", "Tracks Traveled": tracksTraveled}
             tracksOrder.append(tracks2[start_index-1])
             tracks2.pop(start_index)
             start_index -= 1
             
        else:
             tracksTraveled = tracks2[start_index+1]-tracks2[start_index]
             total += tracksTraveled
             table[f"{track}"] = {"Head Path": f"{tracks2[start_index]} to {tracks2[start_index+1]}", "Tracks Traveled": tracksTraveled}
             tracksOrder.append(tracks2[start_index+1])
             tracks2.pop(start_index)

                
    
    table["70"] = {"Head Path": "total no.T", "Tracks Traveled": f"{total}ms"}
    table["100"] = {"Head Path": "avg no.Tt", "Tracks Traveled": f"{round(total/(len(table)-1), 2)}ms"}
    
    
    return (table, tracksOrder)

def SCAN(tracks):
    directional_bit = 0
    tracks2 = tracks.copy()
    for track in tracks2:
        try:
            if track > 50 or track < 1 :
                tracks.remove(track)
            elif tracks.count(track)>1:
                indices = [i for i, x in enumerate(tracks) if x == track]
                indices.pop(0)
                for i in indices:
                    tracks.pop(i)
                    
        except:
            pass
    
    headers = ["head path", "tracks traveled"]
    table = {}
    total  = 0
    
    if min(tracks) != 1 and max(tracks)!= tracks[0]:
        tracks.append(1)    
    
    scanStart = tracks.pop(0)
    scanTracks = [t for t in range(scanStart, 0, -1)]
    if scanStart < max(tracks):
        scanTracks.extend([t for t in range(2,max(tracks)+1)])
    scanOrder = [scanStart]
    for i in scanTracks:
        if tracks and (i in tracks):
            tracksTraveled = abs(scanStart - i)
            total += tracksTraveled
            table[f"{i+50}"] = {"Head Path": f"{scanStart} to {i}", "Tracks Traveled": tracksTraveled}
            tracks.remove(i)
            scanOrder.append(i)
            scanStart = i
        if i == 1:
            directional_bit = 1
            

    table["170"] = {"Head Path": "total no.T", "Tracks Traveled": f"{total}ms"}
    table["200"] = {"Head Path": "avg no.Tt", "Tracks Traveled": f"{round(total/(len(table)-1), 2)}ms"}
    
    
    return (table, scanOrder)
            
            
def LOOK(tracks):
    directional_bit = 1
    tracks2 = tracks.copy()
    for track in tracks2:
        try:
            if track > 50 or track < 1 :
                tracks.remove(track)
            elif tracks.count(track)>1:
                indices = [i for i, x in enumerate(tracks) if x == track]
                indices.pop(0)
                for i in indices:
                    tracks.pop(i)
                    
        except:
            pass
    
    headers = ["head path", "tracks traveled"]
    table = {}
    total  = 0
        
    tracksMax = max(tracks)
    scanStart = tracks.pop(0)
    scanTracks = [t for t in range(scanStart, tracksMax+1)]
    if scanStart > min(tracks):
        scanTracks.extend([t for t in range(tracksMax-1,min(tracks)-1,-1)])
        
    scanOrder = [scanStart]
    for i in scanTracks:
        if tracks and (i in tracks):
            tracksTraveled = abs(scanStart - i)
            total += tracksTraveled
            table[f"{i+50}"] = {"Head Path": f"{scanStart} to {i}", "Tracks Traveled": tracksTraveled}
            tracks.remove(i)
            scanOrder.append(i)
            scanStart = i
        if i == tracksMax:
            directional_bit = 1
            
    table["170"] = {"Head Path": "total no.T", "Tracks Traveled": f"{total}ms"}
    table["200"] = {"Head Path": "avg no.Tt", "Tracks Traveled": f"{round(total/(len(table)-1), 2)}ms"}
    
    
    return (table, scanOrder)
        

fc = FCFS([15,4,40,11,35,7,14])
    

    
