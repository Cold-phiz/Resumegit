import os
import shutil

#file types
images = [".jpg",".jpeg",".png",".tiff",".webp",".gif",".avif",".psd",".eps",".ai",".indd",".raw"]
documents = [".docx",".txt",".pdf",".doc",".xls",".ppt",".blend",".blend1"]
sounds = [".mp3",".aac",".ogg",".flac",".alac",".wav",".aiff",".dsd"]
videos = [".mp4",".mov",".avi",".wmv",".avchd",".webm",".flv"]
scripts = [".py",".js",".java",".cpp",".cs",".html",".css",".rb",".php",".swift",".vbs",".dll"]

comps = [".zip",".7z",".rar",".arc",".gzip",".arj",".lha"]

#fetching files NOT folders/dirs
files = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), f))]

#don't move itself, recycle bin or desktop.ini
files = [file for file in files if file != "desktop cleaner.py"]
files = [file for file in files if file != "Recycle Bin"]
files = [file for file in files if file != "desktop.ini"]

#shortcuts can stay
files = [file for file in files if not any(file.endswith(ext) for ext in [".lnk",".url",".exe"])]

#making folders if they don't exist
def init():
    os.makedirs("Images", exist_ok=True)
    os.makedirs("Documents", exist_ok=True)
    os.makedirs("Sounds", exist_ok=True)
    os.makedirs("Videos", exist_ok=True)
    os.makedirs("Scripts", exist_ok=True)

#moveing everything
def main():
    for file in files:
        if any(file.endswith(ext) for ext in images):
            shutil.move(file, "Images")
        elif any(file.endswith(ext) for ext in documents):
            shutil.move(file, "Documents")
        elif any(file.endswith(ext) for ext in sounds):
            shutil.move(file, "Sounds")
        elif any(file.endswith(ext) for ext in videos):
            shutil.move(file, "Videos")
        elif any(file.endswith(ext) for ext in scripts):
            shutil.move(file, "Scripts")
        elif any(file.endswith(ext) for ext in comps):
            shutil.move(file, "Recycle Bin")
        else:
            print("Error identifying file type of moving file: ",file)
    
#this is a script btw
if __name__ == "__main__":
    init()
    main()   