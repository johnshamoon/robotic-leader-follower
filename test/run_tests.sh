echo "Running Camera tests"
python -m unittest discover -s camera -p '*_test.py'

echo "Running Follower tests"
python -m unittest discover -s follower -p '*_test.py'

echo "Running InputController tests"
python -m unittest discover -s inputcontroller -p '*_test.py'

echo "Running Leader tests"
python -m unittest discover -s leader -p '*_test.py'

echo "Running Main tests"
python -m unittest discover -s main -p '*_test.py'

echo "Running TagRecognition tests"
python -m unittest discover -s tagrec -p '*_test.py'
