import urllib.request
import shutil
import subprocess
import os
import re
from tqdm import tqdm
import sys

html = urllib.request.urlopen("http://www.deeplearningbook.org").read()
html = html.decode("utf-8")
m = re.findall("href.*?>", html)
all_links = [x[6:-2] for x in m]
book_links = [x for x in all_links if "contents" in x]

#links = ['contents/TOC.html', 'contents/acknowledgements.html', 'contents/notation.html', 'contents/intro.html', 'contents/part_basics.html', 'contents/linear_algebra.html', 'contents/prob.html', 'contents/numerical.html', 'contents/ml.html', 'contents/part_practical.html', 'contents/mlp.html', 'contents/regularization.html', 'contents/optimization.html', 'contents/convnets.html', 'contents/rnn.html', 'contents/guidelines.html', 'contents/applications.html', 'contents/part_research.html', 'contents/linear_factors.html', 'contents/autoencoders.html', 'contents/representation.html', 'contents/graphical_models.html', 'contents/monte_carlo.html', 'contents/partition.html', 'contents/inference.html', 'contents/generative_models.html', 'contents/bib.html', 'contents/index-.html']
for l,fn,n  in tqdm(zip(book_links, [str(x)+".html" for x in range(len(book_links))], range(len(book_links))), total=len(book_links)):
    with urllib.request.urlopen("http://www.deeplearningbook.org/"+l) as response, open(fn, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
        subprocess.call(["/usr/bin/google-chrome", "--headless", "--disable-gpu", "--print-to-pdf", fn], stderr=subprocess.DEVNULL, )
        subprocess.call(["/bin/mv", "output.pdf", f"{l.split('/')[1].split('.')[0]}.pdf"])
        #subprocess.call(["/bin/rm", f"{out_file}"])

# Can be made simpler
folder = os.path.abspath(os.path.dirname(sys.argv[0]))
parts = [folder+"/"+x.split('/')[1].split('.')[0]+'.pdf' for x in book_links]

# Not working for some reason :| 
#   call(["/usr/bin/pdftk", "*.pdf", "output", "DeepLearningBook.pdf"], shell=True)
os.system(f"/usr/bin/pdftk {' '.join(parts)} output DeepLearningBook.pdf")

    