from pathlib import Path
import arrow
# funzione aggiunta il 27/01/20
def check_time_file(UPLOAD_FOLDER):
	criticalTime = arrow.now().shift(hours=+5).shift(days=-7)
	for item in Path(UPLOAD_FOLDER).glob('*'):
		if item.is_file():
			itemTime = arrow.get(item.stat().st_mtime)
			if itemTime < criticalTime:
				#remove it
				pass
