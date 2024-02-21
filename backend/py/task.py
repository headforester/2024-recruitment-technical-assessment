from dataclasses import dataclass

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


"""
Task 1
"""
def leafFiles(files: list[File]) -> list[str]:
    files_dict = {file.id:file.name for file in files}
    name_files = [file.name for file in files]

    # Remove the Parent file from pool
    for file in files:
        if file.parent != -1 and files_dict[file.parent] in name_files:  
            name_files.remove(files_dict[file.parent])

    return name_files


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:
    # the dict [category_name, count]
    categories_list = {}
    for file in files:
        for category in file.categories:
            if category in categories_list.keys():
                categories_list[category] += 1
            else:
                categories_list[category] = 1

    sorted_category_list = sorted(sorted(categories_list.items(), key = lambda x : x[0]), key = lambda x : x[1],reverse=True)  
    sorted_category_list = [category[0] for category in sorted_category_list]
    
    if len(sorted_category_list) < k:
        return sorted_category_list
    else: 
        return sorted_category_list[:k]


"""
Task 3
"""
def largestFileSize(files: list[File]) -> int:
    road_map = []
    files_name_dict = {file.name: file for file in files}
    files_id_dict = {file.id: file for file in files}
    leaf_files = [files_name_dict[name] for name in leafFiles(files)]
    
    # Find Every path to the root from the leaf nodes
    for file in leaf_files:
        pointer = file
        road = [pointer.name]
        while pointer.parent != -1:
            pointer = files_id_dict[pointer.parent]
            road.append(pointer.name)
        if road != []: road_map.append(road)        
    
    # Merge paths containing the same root
    merged_roads = {}
    for road in road_map:
        if road[-1] not in merged_roads.keys():
            merged_roads[road[-1]] = road
        else:
            merged_roads[road[-1]] = list(set(merged_roads[road[-1]]) | set(road[:-1]))

    # Count the size of every path
    max_num = 0
    for road in merged_roads.values():
        num = sum(files_name_dict[pointer].size for pointer in road)
        if max_num < num: 
            max_num = num 

    return max_num


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992
