from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import subprocess
import os
import re
class filter:
    def sample_recognize(self,local_file_path,filename,path):
        client = speech_v1.SpeechClient()
        language_code = "en-US"
        enable_word_time_offsets = True
        use_enhanced = True
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    
        config = {
        "language_code": language_code,
        
        "encoding": encoding,
        "enable_word_time_offsets": enable_word_time_offsets,
        "use_enhanced": use_enhanced,

        }
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        swears=['fuck','shit','ass','bitch','whore','dick','fuk',"bitches","sexual","anus","asshole",'fucking']

        response = client.recognize(config, audio)
        ts = []
        for result in response.results:
        
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
        
            for j in alternative.words:
                for key in swears:
                    if key in j.word:
                        start=j.start_time.nanos/(10**9)+j.start_time.seconds
                        end=j.end_time.nanos/(10**9)+j.end_time.seconds
                        print(j.word,start,end)
                        se = [start,end]
                        ts.extend(se)
                        print(ts)
    
        bl = ''
        for i in range(0,len(ts),2):
            bl+='between(t\,{0}\,{1})+'.format(ts[i],ts[i+1])
        if(len(bl)!=0):
            bl=bl[:-1]       
            os.system('''ffmpeg -i {0} -max_muxing_queue_size 1024 -c:v copy -af volume=0:enable='{1}' {2}'''.format(path+filename+".mp4",bl,path+filename+"filtered"+".mp4"))    
        else:
            print(path,filename)
            os.chdir("/Users/VAISHNAVI/Desktop/mini/uploadedfiles")            
            command = "copy {0} {1}".format(filename+".mp4",filename+"filtered"+".mp4")
            subprocess.call(command, shell=True)
        
        #os.system('''ffmpeg -i clip.mp4 -c:v copy -af volume=0:enable='{0}' clip_out.mp4'''.format(bl))




    def convert(self,path,filename):
        srcname=filename
        r=filename[:len(filename)-4]
        destname=filename[:len(filename)-4]+".wav"

        command = "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn {1}".format(path+srcname,path+destname)


        subprocess.call(command, shell=True)
        output = subprocess.check_output("ffprobe -i {} -show_streams -select_streams a:0".format(path+destname), shell=True)
        output=str(output)
        l=re.findall(r"\\r\\nchannels=[1-9]",output)

        if(l[0][-1]=='2'):
            command="ffmpeg -i {0} -map_channel 0.0.0 {1} -map_channel 0.0.1 {2}".format(path+destname,path+r+"_left.wav",path+r+"_right.wav")
            subprocess.call(command, shell=True)
            self.sample_recognize(path+r+"_left.wav",r,path)
        else:
            
            self.sample_recognize(path+destname,r,path)


