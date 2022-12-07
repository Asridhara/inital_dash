from app import server as application

import sys

path = '/******/******/******'
if path not in sys.path:
    sys.path.append(path)

if __name__ == "__main__":
    application.run(debug=True)