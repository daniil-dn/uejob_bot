#echo off

call %~dp0vacancy_bot_parser/env/bin/activate

cd %~dp0vacancy_bot_parser

python main.py&

pause