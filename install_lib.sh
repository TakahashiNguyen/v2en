rm ./dist -fr
python3 -m build
pip install -r requirements.txt --force-reinstall
rm *.egg* -fr