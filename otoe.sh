# get pwd

cur_dir = $pwd

echo cur_dir

source venv/bin/activate
export PYTHONPATH=.
python otoe/src/__init__.py
