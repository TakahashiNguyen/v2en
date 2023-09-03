rm ./dist -fr
python3 -m pip install build
python3 -m build
pip install -r requirements.txt
pip install ./dist/v2enlib-0.0.1-py3-none-any.whl --force-reinstall
rm *.egg* -fr