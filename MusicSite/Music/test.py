import subprocess
import os
path = '{}/static/documents/offer__vauvision__27102020-3.docx'.format(str(os.path.abspath('')))
output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,path])
os.rename('offer__vauvision__27102020-3.pdf','static/documents/offer__vauvision__27102020-3.pdf')
