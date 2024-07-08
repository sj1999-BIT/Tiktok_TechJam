# AI-Tonal
A convenient tool that leverage the powerful capabilities of generative AI to generate
custom background music for your video. 
## Quick Start

Follow these steps to get the Suno API up and running on your local machine:

1. **prepare key to models**
   1. in file `.env`, add in your own suno_cookie and openai-key
   2. suno_cookie can be found using https://suno.gcui.art/
      1. Copy the cookie to `.env` file in format `SUNO_COOKIE=<your cookie>`
   3. openai-key can be found using https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key
      1. Copy the cookie to `.env` file in format `OPENAI_KEY=<your key>`
2. **setup environment**
   1. `git clone https://github.com/sj1999-BIT/Tiktok_TechJam.git`
   2. `conda env create -f environment.yml`
   3.  `conda activate AI-Tonal`
3. **run AI-Tonal locally**
   1. command prompt go to the directory of the repo
   2. `python server.py`
   3. go to `localhost:5000`
   4. Click `Choose File` to select your target video
   5. Add in your user prompt
   6. Click `submit`
   7. It will take a few minutes, a mp3 file of the music will be `automatically downloaded`
